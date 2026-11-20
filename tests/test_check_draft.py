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

    def test_shelter_setting_hits(self):
        text = (
            "kennel door, kennels, kennel fence, playgroups, play yard, quiet room, intake, "
            "adoption floor, dog runs, runs, run, shelter, at the shelter, in a group of dogs"
        )
        self.assertEqual(
            sorted(CHECKER.shelter_setting_hits(text)),
            ["adoption floor", "dog run", "intake", "kennel", "kennel door", "kennel fence",
             "play yard", "playgroup", "quiet room"],
        )

    def test_shelter_setting_words_do_not_fail(self):
        card = example_card().replace(
            "ABOUT THIS PET\n",
            "ABOUT THIS PET\nShe naps in the quiet room by the kennel door.\n",
            1,
        )
        code, out = self.run_checker(card)
        self.assertEqual(code, 0, out)
        lines = [ln for ln in out.splitlines() if ln.startswith("Shelter-setting words (review:")]
        self.assertEqual(len(lines), 1, out)
        self.assertIn("'kennel door'", lines[0])
        self.assertIn("'quiet room'", lines[0])

    def test_example_card_has_no_shelter_setting_words(self):
        _, out = self.run_checker(example_card())
        self.assertIn(
            "Shelter-setting words (review: name the setting in adopter words): none", out
        )

    PROGRAM_BLOCK = (
        "Polly is part of the Senior Care Plan: Riverside waives the adoption fee and "
        "reimburses up to $1,500 in vet costs for her first year. "
        "Polly is supported by a grant from the Example Fund for senior dogs."
    )

    def card_with_program_block(self, block: str) -> str:
        marker = "Polly is a Riverside Diamond Dog"
        card = example_card()
        self.assertIn(marker, card)
        return card.replace(marker, block + "\n\n" + marker, 1)

    def test_program_block_with_funder_credit_passes(self):
        code, out = self.run_checker(self.card_with_program_block(self.PROGRAM_BLOCK))
        self.assertEqual(code, 0, out)
        self.assertNotIn("shares a line", out)

    def test_program_sentence_with_animal_sentence_fails(self):
        card = self.card_with_program_block(self.PROGRAM_BLOCK + " She loves car rides.")
        code, out = self.run_checker(card)
        self.assertEqual(code, 1, out)
        self.assertIn("shares a line", out)


if __name__ == "__main__":
    unittest.main()
