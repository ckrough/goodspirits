"""Tests for the adoption-profile checker against the template's example card.

These tests depend on the heading, fence, and placeholders of the `## Example`
section in references/profile-template.md. Any change to that example lists this
test in its plan.
"""

from __future__ import annotations

import contextlib
import importlib.util
import io
import re
import tempfile
import unittest
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent / "plugins/adoption-profile-writing/skills/adoption-profile-writing"


def load_checker():
    spec = importlib.util.spec_from_file_location("check_draft", SKILL / "scripts/check_draft.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


CHECKER = load_checker()


def example_card() -> str:
    text = (SKILL / "references/profile-template.md").read_text(encoding="utf-8")
    _, found, section = text.partition("\n## Example\n")
    match = re.search(r"```\n(.*?)\n```", section, re.DOTALL)
    if not found or not match:
        raise AssertionError("profile-template.md has no fenced card under '## Example'")
    card = match.group(1)
    # The Diamond Dog matcher rejects square brackets; writers replace both placeholders.
    return card.replace("[Name]", "Polly").replace("[Shelter]", "Riverside")


class CheckDraftTest(unittest.TestCase):
    def run_checker(self, card: str) -> tuple[int, str]:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "draft.txt"
            path.write_text(card, encoding="utf-8")
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                code = CHECKER.main([str(path)])
        return code, out.getvalue()

    def test_example_card_passes(self):
        code, out = self.run_checker(example_card())
        self.assertEqual(code, 0, out)

    def test_missing_training_heading_fails(self):
        card = example_card().replace("TRAINING\n", "")
        code, out = self.run_checker(card)
        self.assertEqual(code, 1, out)
        self.assertIn("missing heading TRAINING", out)

    def test_first_person_fails(self):
        card = example_card().replace(
            "ABOUT THIS PET\n", "ABOUT THIS PET\nI think you will love her.\n", 1
        )
        code, out = self.run_checker(card)
        self.assertEqual(code, 1, out)
        self.assertIn("first person (", out)


if __name__ == "__main__":
    unittest.main()
