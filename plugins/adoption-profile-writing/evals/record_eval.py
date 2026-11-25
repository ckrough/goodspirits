"""Record a summary of each model's `claude plugin eval` run in evals/history/, for committing.

Usage: python3 record_eval.py [--plugin DIR] [--model MODEL] [aggregate-result.json ...]
       python3 record_eval.py [--plugin DIR] --stamp SWEEP_DIR

`make eval` stamps each sweep directory with --stamp before it runs (the commit and any
uncommitted plugin changes), runs the suite once per writer model into
evals/results/<sweep>/<model>/, and marks the sweep complete when every model finished.
With no result named, this records every model's run in the newest sweep, one file each,
named <run-start>_<commit>_<model>.json. The result file does not name the writer model,
so it is read from the run's directory, or from --model for a single named result. Each
summary names the commit of the skill that ran, so it refuses a sweep that ran at another
commit, started with uncommitted plugin changes, or did not finish, and it refuses while
the plugin has uncommitted changes. Standard library only.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# Run output that changes without changing the skill under test.
IGNORED_DIRS = ("evals/results/", "evals/history/")
# Written into each sweep directory: the commit and changes it started with, and its completion.
STAMP = "source.json"
COMPLETE = "complete"


def git(cwd: Path, *args: str) -> str:
    return subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True, text=True).stdout


def newest_sweep(plugin: Path) -> list[Path]:
    """Each model's aggregate-result.json in the newest evals/results/<sweep>/<model>/."""
    found = sorted((plugin / "evals/results").glob("*/*/aggregate-result.json"))
    if not found:
        raise SystemExit(f"no <sweep>/<model>/aggregate-result.json under {plugin / 'evals/results'}; run make eval first")
    sweep = found[-1].parent.parent
    return [p for p in found if p.parent.parent == sweep]


def uncommitted_changes(plugin: Path) -> list[str]:
    """Porcelain lines for changed or untracked plugin files outside the run output."""
    lines = git(plugin, "status", "--porcelain", "--untracked-files=all", "--", ".").splitlines()
    prefix = git(plugin, "rev-parse", "--show-prefix").strip()
    blocking = []
    for line in lines:
        path = line[3:].split(" -> ")[-1].strip('"')
        rel = path.removeprefix(prefix)
        if not rel.startswith(IGNORED_DIRS):
            blocking.append(line)
    return blocking


def stamp_sweep(plugin: Path, sweep_dir: Path) -> None:
    """Record the commit a sweep starts at, and any uncommitted plugin changes it starts with."""
    sweep_dir.mkdir(parents=True, exist_ok=True)
    source = {"commit": git(plugin, "rev-parse", "HEAD").strip(), "uncommitted": uncommitted_changes(plugin)}
    (sweep_dir / STAMP).write_text(json.dumps(source, indent=2) + "\n", encoding="utf-8")


def sweep_problem(sweep_dir: Path, head: str) -> str | None:
    """Why a sweep cannot be recorded against HEAD, or None when it can."""
    stamp = sweep_dir / STAMP
    if not stamp.is_file():
        return f"{sweep_dir} has no record of the commit it ran at; run make eval, which stamps each sweep"
    source = json.loads(stamp.read_text(encoding="utf-8"))
    if source.get("uncommitted"):
        return f"{sweep_dir} had uncommitted changes when it started, so no commit names the skill that ran"
    if source.get("commit") != head:
        return f"{sweep_dir} ran at {source.get('commit')}, not HEAD {head}"
    if not (sweep_dir / COMPLETE).is_file():
        return f"{sweep_dir} did not finish: make eval writes {COMPLETE} only after every model's run"
    return None


def case_tags(plugin: Path, case_dir: str) -> list[str]:
    path = plugin / case_dir / "case.yaml"
    if not path.is_file():
        return []
    match = re.search(r"^tags:\s*\[(.*)\]\s*$", path.read_text(encoding="utf-8"), re.MULTILINE)
    return [t.strip() for t in match.group(1).split(",") if t.strip()] if match else []


def pass_rates(runs: list[dict]) -> dict[str, dict]:
    """Per grader: weight, whether it counts toward the score, and its share of passing runs."""
    rates: dict[str, dict] = {}
    for run in runs:
        for g in run.get("graders") or []:
            entry = rates.setdefault(g["name"], {"weight": g.get("weight", 1), "scored": g.get("scored", True), "passes": 0, "runs": 0})
            entry["runs"] += 1
            entry["passes"] += bool(g.get("passed"))
    return {name: {"weight": e["weight"], "scored": e["scored"], "rate": round(e["passes"] / e["runs"], 4)} for name, e in rates.items()}


def summarize(result: dict, commit: str, plugin: Path, model: str, sweep: str) -> dict:
    suite = result.get("suite", {})
    plugins = suite.get("plugins") or [{}]
    cases = {}
    for case in result.get("cases", []):
        arms = case.get("arms") or {}
        with_rates = pass_rates(arms.get("with") or [])
        without_rates = pass_rates(arms.get("without") or [])
        graders = {}
        for name in sorted(with_rates.keys() | without_rates.keys()):
            base = with_rates.get(name) or without_rates[name]
            graders[name] = {
                "weight": base["weight"],
                "scored": base["scored"],
                "with": with_rates[name]["rate"] if name in with_rates else None,
                "without": without_rates[name]["rate"] if name in without_rates else None,
            }
        agg = case.get("aggregates", {})
        cases[case["name"]] = {
            "tags": case_tags(plugin, case.get("dir", "")),
            "runs": case.get("runsPerCase"),
            "score_with": agg.get("score"),
            "score_without": agg.get("scoreWithout"),
            "delta": agg.get("delta"),
            "graders": graders,
        }
    return {
        "commit": commit,
        "started_at": result.get("startedAt"),
        "claude_version": result.get("claudeVersion"),
        "plugin_version": plugins[0].get("version"),
        "sweep": sweep,
        "model": model,
        "judge_model": suite.get("judgeModel"),
        "ablation": suite.get("ablation"),
        "duration_seconds": result.get("durationSeconds"),
        "cost_usd": result.get("costUsd"),
        "mean_delta": result.get("aggregates", {}).get("meanDelta"),
        "cases": cases,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("results", nargs="*", type=Path, help="aggregate-result.json files (default: every model's run in the newest sweep)")
    parser.add_argument("--plugin", type=Path, default=Path(__file__).resolve().parent.parent, help="plugin directory")
    parser.add_argument("--model", help="writer model of a single named result (default: the result's directory name)")
    parser.add_argument("--stamp", type=Path, metavar="SWEEP_DIR", help="record the commit and changes a sweep starts with, then exit")
    args = parser.parse_args(argv)
    plugin = args.plugin.resolve()

    if args.stamp:
        stamp_sweep(plugin, args.stamp)
        return 0

    changes = uncommitted_changes(plugin)
    if changes:
        print("refusing to record: the plugin has uncommitted changes, so no commit names the skill that ran:", file=sys.stderr)
        print("\n".join(changes), file=sys.stderr)
        return 1
    if args.model and len(args.results) != 1:
        print("refusing to record: --model names the writer of one named result only", file=sys.stderr)
        return 1

    commit = git(plugin, "rev-parse", "HEAD").strip()
    paths = [p.resolve() for p in args.results] or newest_sweep(plugin)
    runs = []
    for path in paths:
        if path.parent.parent.parent.name != "results":
            print(f"refusing to record: {path} is not in results/<sweep>/<model>/, so its sweep and model are unknown", file=sys.stderr)
            return 1
        problem = sweep_problem(path.parent.parent, commit)
        if problem:
            print(f"refusing to record: {problem}", file=sys.stderr)
            return 1
        result = json.loads(path.read_text(encoding="utf-8"))
        runs.append((path, result, datetime.fromisoformat(result["startedAt"])))

    for path, result, started in runs:
        model = args.model or path.parent.name
        summary = summarize(result, commit, plugin, model, path.parent.parent.name)
        out = plugin / "evals/history" / f"{started.strftime('%Y-%m-%dT%H-%M-%SZ')}_{commit[:12]}_{model}.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
        print(f"recorded {out}")
        for name, case in summary["cases"].items():
            print(f"  {name}: with {case['score_with']}  without {case['score_without']}  delta {case['delta']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
