"""Tests for evals/record_eval.py, which commits a summary of each model's run in a make-eval sweep."""

from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

EVALS = Path(__file__).resolve().parent.parent / "plugins/adoption-profile-writing/evals"


def load_recorder():
    spec = importlib.util.spec_from_file_location("record_eval", EVALS / "record_eval.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


RECORDER = load_recorder()

RUN_START = "2026-01-02T10:00:00.000Z"
SWEEP = "2026-01-02T09-59-00Z"


def grader(name, passed, weight=1, scored=True, with_only=False):
    return {"name": name, "passed": passed, "scored": scored, "weight": weight, "withOnly": with_only}


def fixture_result() -> dict:
    with_runs = [
        {"score": 0.75, "graders": [grader("matches-ideal", True, 3), grader("heading", True), grader("skill-fired", True, scored=False, with_only=True)]},
        {"score": 0.25, "graders": [grader("matches-ideal", False, 3), grader("heading", True), grader("skill-fired", True, scored=False, with_only=True)]},
    ]
    without_runs = [
        {"score": 0.0, "graders": [grader("matches-ideal", False, 3), grader("heading", False)]},
        {"score": 0.25, "graders": [grader("matches-ideal", False, 3), grader("heading", True)]},
    ]
    return {
        "schemaVersion": 1,
        "claudeVersion": "9.9.9",
        "startedAt": RUN_START,
        "durationSeconds": 60,
        "costUsd": 1.5,
        "suite": {
            "ablation": "with-without",
            "judgeModel": "judge-x",
            "plugins": [{"name": "demo", "version": "1.2.3", "path": "/somewhere"}],
        },
        "aggregates": {"meanDelta": 0.375},
        "cases": [
            {
                "name": "case-a",
                "dir": "evals/case-a",
                "runsPerCase": 2,
                "aggregates": {"score": 0.5, "scoreWithout": 0.125, "delta": 0.375},
                "arms": {"with": with_runs, "without": without_runs},
            }
        ],
    }


def git(repo: Path, *args: str, date: str | None = None) -> str:
    env = dict(os.environ)
    if date:
        env["GIT_AUTHOR_DATE"] = env["GIT_COMMITTER_DATE"] = date
    out = subprocess.run(
        ["git", "-c", "commit.gpgsign=false", "-c", "user.name=t", "-c", "user.email=t@example.invalid", *args],
        cwd=repo, env=env, check=True, capture_output=True, text=True,
    )
    return out.stdout.strip()


class RecordEvalTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name)
        self.plugin = self.repo / "plugins/demo"
        case = self.plugin / "evals/case-a"
        case.mkdir(parents=True)
        (case / "case.yaml").write_text('schema_version: "1.1"\nname: case-a\ntags: [bite, ideal-pending]\n')
        (self.plugin / "SKILL.md").write_text("skill\n")
        git(self.repo, "init", "-q")
        git(self.repo, "add", ".")
        git(self.repo, "commit", "-q", "-m", "init", date="2026-01-01T00:00:00Z")
        self.result = self.write_result(SWEEP, "agent-y")

    def write_result(self, sweep: str, model: str) -> Path:
        path = self.plugin / "evals/results" / sweep / model / "aggregate-result.json"
        path.parent.mkdir(parents=True)
        path.write_text(json.dumps(fixture_result()))
        return path

    def tearDown(self):
        self.tmp.cleanup()

    def record(self, *extra: str) -> tuple[int, str]:
        out = io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
            code = RECORDER.main(["--plugin", str(self.plugin), *extra])
        return code, out.getvalue()

    def history(self) -> list[Path]:
        return sorted((self.plugin / "evals/history").glob("*.json"))

    def test_records_summary_of_newest_run(self):
        code, out = self.record()
        self.assertEqual(code, 0, out)
        [path] = self.history()
        head = git(self.repo, "rev-parse", "HEAD")
        self.assertEqual(path.name, f"2026-01-02T10-00-00Z_{head[:12]}_agent-y.json")
        summary = json.loads(path.read_text())
        self.assertEqual(summary["commit"], head)
        self.assertEqual(summary["model"], "agent-y")
        self.assertEqual(summary["sweep"], SWEEP)
        self.assertEqual(summary["claude_version"], "9.9.9")
        self.assertEqual(summary["judge_model"], "judge-x")
        self.assertEqual(summary["plugin_version"], "1.2.3")
        case = summary["cases"]["case-a"]
        self.assertEqual(case["tags"], ["bite", "ideal-pending"])
        self.assertEqual((case["score_with"], case["score_without"], case["delta"]), (0.5, 0.125, 0.375))
        self.assertEqual(case["graders"]["matches-ideal"], {"weight": 3, "scored": True, "with": 0.5, "without": 0.0})
        self.assertEqual(case["graders"]["heading"]["without"], 0.5)
        self.assertEqual(case["graders"]["skill-fired"], {"weight": 1, "scored": False, "with": 1.0, "without": None})

    def test_records_every_model_in_the_newest_sweep(self):
        self.write_result(SWEEP, "agent-z")
        self.write_result("2026-01-02T08-00-00Z", "agent-old")
        code, out = self.record()
        self.assertEqual(code, 0, out)
        models = sorted(json.loads(p.read_text())["model"] for p in self.history())
        self.assertEqual(models, ["agent-y", "agent-z"])

    def test_model_flag_names_the_model_of_a_named_result(self):
        code, out = self.record("--model", "agent-q", str(self.result))
        self.assertEqual(code, 0, out)
        [path] = self.history()
        self.assertEqual(json.loads(path.read_text())["model"], "agent-q")

    def test_refuses_uncommitted_plugin_change(self):
        (self.plugin / "SKILL.md").write_text("edited\n")
        code, out = self.record()
        self.assertEqual(code, 1)
        self.assertIn("uncommitted", out)
        self.assertEqual(self.history(), [])

    def test_ignores_results_and_history_changes(self):
        (self.plugin / "evals/history").mkdir()
        (self.plugin / "evals/history/old.json").write_text("{}")
        code, out = self.record()
        self.assertEqual(code, 0, out)

    def test_refuses_run_older_than_last_plugin_commit(self):
        (self.plugin / "SKILL.md").write_text("changed after the run\n")
        git(self.repo, "commit", "-q", "-am", "later", date="2026-01-03T00:00:00Z")
        code, out = self.record()
        self.assertEqual(code, 1)
        self.assertIn("before", out)

    def test_records_named_result(self):
        code, out = self.record(str(self.result))
        self.assertEqual(code, 0, out)
        self.assertEqual(len(self.history()), 1)


if __name__ == "__main__":
    unittest.main()
