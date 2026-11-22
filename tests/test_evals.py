"""Structure and de-identification checks for the plugin's eval suite (evals/case-*/).

`claude plugin eval` runs the cases; this test checks only what a machine can check
without running them: each case's files, tags, graders, and the absence of calendar dates.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

EVALS = Path(__file__).resolve().parent.parent / "plugins/adoption-profile-writing/evals"
NOT_CASES = {"results", "history", "__pycache__"}

RULE_TAGS = {"bite", "placement-constraint", "changed-record"}
ALLOWED_TAGS = RULE_TAGS | {"ideal-pending"}
TECHNIQUES = ("pseudonymization", "generalization", "suppression")
HEADINGS = ("about-this-pet", "household-fit", "training", "good-to-know")
REQUIRED = (
    "case.yaml",
    "prompt.md",
    "fixture.sh",
    "ideal.md",
    "resources/record.md",
    "deidentification.md",
    "graders/matches-ideal.md",
    "graders/profile-saved.md",
    "graders/skill-fired.md",
    *(f"graders/heading-{h}.md" for h in HEADINGS),
)
# Graders that score the rubric's case-independent rules; every case carries the same copy.
SHARED_GRADERS = (
    "profile-saved",
    "skill-fired",
    *(f"heading-{h}" for h in HEADINGS),
    "rubric-first-person",
    "rubric-social-words",
    "rubric-screening",
    "rubric-absolute-claims",
)
# Run with --scaffold, as the operator: every case must carry exactly this copy-only script.
FIXTURE = """#!/usr/bin/env bash
# Copy the case's input files into the empty eval workspace.
set -euo pipefail
cp -R "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/resources" ./resources
"""
PROFILE_FILE = "{source: file, path: profile.md}"
DATE_PATTERNS = (
    re.compile(r"\b\d{4}-\d{2}-\d{2}\b"),
    re.compile(r"\b\d{1,2}/\d{1,2}/\d{2,4}\b"),
    re.compile(r"\b(?:199\d|20\d\d)\b"),
)


def cases() -> list[Path]:
    return sorted(p for p in EVALS.iterdir() if p.is_dir() and p.name not in NOT_CASES and not p.name.startswith("."))


def frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        raise AssertionError(f"{path} has no frontmatter")
    fields = {}
    for line in match.group(1).splitlines():
        key, _, value = line.partition(":")
        fields[key.strip()] = value.strip()
    return fields


def tags(case: Path) -> list[str]:
    match = re.search(r"^tags:\s*\[(.*)\]\s*$", (case / "case.yaml").read_text(encoding="utf-8"), re.MULTILINE)
    if not match:
        raise AssertionError(f"{case.name}/case.yaml has no flow-form tags list")
    return [t.strip() for t in match.group(1).split(",") if t.strip()]


class EvalSuiteTest(unittest.TestCase):
    def test_three_to_five_cases(self):
        self.assertTrue(3 <= len(cases()) <= 5, [c.name for c in cases()])

    def test_required_files(self):
        for case in cases():
            for rel in REQUIRED:
                self.assertTrue((case / rel).is_file(), f"{case.name} lacks {rel}")

    def test_case_yaml_runs_the_fixture(self):
        for case in cases():
            text = (case / "case.yaml").read_text(encoding="utf-8")
            self.assertIn('schema_version: "1.1"', text, case.name)
            self.assertRegex(text, r"(?m)^\s+scaffold_script: fixture\.sh$", case.name)
            self.assertEqual((case / "fixture.sh").read_text(encoding="utf-8"), FIXTURE, case.name)

    def test_tags_cover_the_rules(self):
        seen = set()
        for case in cases():
            case_tags = tags(case)
            self.assertTrue(set(case_tags) <= ALLOWED_TAGS, f"{case.name}: {case_tags}")
            seen |= set(case_tags)
        self.assertTrue(RULE_TAGS <= seen, f"no case covers {RULE_TAGS - seen}")

    def test_bite_cases_keep_the_incident_off_the_card(self):
        for case in cases():
            if "bite" in tags(case):
                for grader in ("no-incident-words", "history-review"):
                    self.assertTrue((case / f"graders/{grader}.md").is_file(), f"{case.name} lacks {grader}")

    def test_shared_graders_are_identical_in_every_case(self):
        first, *rest = cases()
        for name in SHARED_GRADERS:
            reference = first / f"graders/{name}.md"
            self.assertTrue(reference.is_file(), f"{first.name} lacks {name}")
            for case in rest:
                path = case / f"graders/{name}.md"
                self.assertTrue(path.is_file(), f"{case.name} lacks {name}")
                self.assertEqual(path.read_text(encoding="utf-8"), reference.read_text(encoding="utf-8"), f"{case.name}/{name}")

    def test_each_ideal_passes_its_regex_graders(self):
        for case in cases():
            ideal = (case / "ideal.md").read_text(encoding="utf-8")
            for path in sorted((case / "graders").glob("*.md")):
                fields = frontmatter(path)
                if fields.get("type") != "regex":
                    continue
                pattern = fields["pattern"].strip("'")
                flags = re.IGNORECASE if "i" in fields.get("flags", "") else 0
                flags |= re.MULTILINE if "m" in fields.get("flags", "") else 0
                found = re.search(pattern, ideal, flags)
                if fields.get("match") == "not_contains":
                    self.assertIsNone(found, f"{case.name}/{path.name}: {found and found.group(0)}")
                else:
                    self.assertIsNotNone(found, f"{case.name}/{path.name}")

    def test_matches_ideal_embeds_the_ideal(self):
        for case in cases():
            ideal = (case / "ideal.md").read_text(encoding="utf-8").strip()
            grader = (case / "graders/matches-ideal.md").read_text(encoding="utf-8")
            self.assertIn(ideal, grader, f"{case.name}: graders/matches-ideal.md is out of date with ideal.md")

    def test_scored_graders_read_the_saved_profile(self):
        for case in cases():
            for path in sorted((case / "graders").glob("*.md")):
                fields = frontmatter(path)
                kind = fields.get("type")
                if kind == "regex":
                    self.assertEqual(fields.get("target"), PROFILE_FILE, f"{case.name}/{path.name}")
                elif kind == "llm":
                    self.assertEqual(fields.get("focus"), PROFILE_FILE, f"{case.name}/{path.name}")

    def test_regex_graders_use_flags_not_inline_groups(self):
        for case in cases():
            for path in sorted((case / "graders").glob("*.md")):
                pattern = frontmatter(path).get("pattern", "")
                self.assertNotRegex(pattern, r"\(\?[a-z]+\)", f"{case.name}/{path.name}")
            for heading in HEADINGS:
                self.assertEqual(frontmatter(case / f"graders/heading-{heading}.md").get("flags"), "m", case.name)

    def test_deidentification_names_a_technique(self):
        for case in cases():
            text = (case / "deidentification.md").read_text(encoding="utf-8").lower()
            self.assertTrue(any(t in text for t in TECHNIQUES), case.name)

    def test_no_calendar_dates(self):
        for case in cases():
            for path in sorted(p for p in case.rglob("*") if p.is_file()):
                text = path.read_text(encoding="utf-8")
                for pattern in DATE_PATTERNS:
                    found = pattern.search(text)
                    self.assertIsNone(found, f"{path.relative_to(EVALS)}: {found and found.group(0)}")


if __name__ == "__main__":
    unittest.main()
