"""Check an adoption-profile draft against the rubric's mechanical rules.

Standard library only. Run from anywhere:

  python3 scripts/check_draft.py DRAFT.md

The draft is markdown with the four section headings (ABOUT THIS PET, HOUSEHOLD FIT,
TRAINING, GOOD TO KNOW), bold or ATX, with or without a trailing colon. Frontmatter, a
title, and any heading after the profile that is not one of the four (an "Open items" or
boilerplate block) are ignored.

Checks: all four headings, 175-250 narrative words, social/humanizing words, adopter
screening phrases, absolute claims, em-dashes, and a program-name sentence sharing a line
with other copy. Placement constraints are listed but never counted against the draft.
Exit status is 0 on PASS and 1 when there is something to fix.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

HEADINGS = ("ABOUT THIS PET", "HOUSEHOLD FIT", "TRAINING", "GOOD TO KNOW")

# Correlate with animals that did not get adopted (Markowitz 2020).
SOCIAL_WORDS = [
    "buddy", "best friend", "bestie", "companion", "sweetheart", "sweetie", "fur baby",
    "furbaby", "fur-baby", "baby boy", "baby girl", "soulmate", "soul mate", "cuddle bug",
    "cuddlebug", "snuggle bug", "lifelong friend", "forever friend", "little angel", "angel",
    "princess", "prince charming", "gentleman", "lady", "old soul", "love bug", "lovebug",
    "velcro dog", "shadow",
]

# Conditions on the applicant. They shrink the pool and say nothing about the animal.
ADOPTER_CONDITION_PHRASES = [
    "must have a fenced yard", "must have a fenced-in yard", "fenced yard required",
    "fenced-in yard required", "requires a fenced", "needs a fenced", "qualified adopters only",
    "experienced owners only", "experienced adopters only", "experienced home only",
    "no apartments", "serious inquiries only", "not for first-time owners", "must apply",
]

# Attributes of the animal. Reported so a reviewer can check provenance; never penalized.
PLACEMENT_CONSTRAINT_PHRASES = [
    "only dog", "only pet", "no children", "no kids", "no cats", "no other dogs",
    "adult-only home", "adults-only home", "without young children", "without small children",
    "without children",
]

# Narrative guarantees the record cannot back.
ABSOLUTE_CLAIM_PHRASES = [
    "great with all", "good with everyone", "loves everyone", "loves all", "gets along with all",
    "gets along with everyone", "guaranteed", "will love your", "will be great with",
    "perfect with kids", "perfect family dog", "the perfect", "will do great with",
    "always friendly", "never aggressive", "100%",
]

# Lines naming a program are often stripped as boilerplate by scoring tools.
PROGRAM_MARKERS = ("senior care plan", "grey muzzle", "waives the adoption fee", "reimburses up to")

_HEADING_LINE = re.compile(r"^\s*(?:#{1,6}\s*)?[*_]*\s*(.+?)\s*[*_:]*\s*$")
_MD_HEADING = re.compile(r"^\s*#{1,6}\s")
_IMAGE_MD = re.compile(r"!\[[^\]]*\]\([^)]*\)")
_LINK_MD = re.compile(r"\[([^\]]*)\]\([^)]*\)")
_BARE_URL = re.compile(r"https?://\S+|www\.\S+")


def heading_of(line: str) -> str | None:
    m = _HEADING_LINE.match(line)
    if not m:
        return None
    label = m.group(1).strip().upper()
    return label if label in HEADINGS else None


def extract_body(text: str) -> tuple[str, list[str]]:
    """Profile prose under the four headings, and the headings found."""
    text = re.sub(r"\A---\n.*?\n---\n", "", text, flags=re.DOTALL)
    out: list[str] = []
    found: list[str] = []
    started = False
    for line in text.splitlines():
        h = heading_of(line)
        if h:
            started = True
            found.append(h)
            continue
        if started and _MD_HEADING.match(line):
            break
        if started:
            out.append(line)
    return "\n".join(out), found


def strip_markup(text: str) -> str:
    text = _IMAGE_MD.sub(" ", text)
    text = _LINK_MD.sub(r"\1", text)
    return _BARE_URL.sub(" ", text)


def word_count(text: str) -> int:
    return len(re.findall(r"\b[\w'-]+\b", strip_markup(text)))


def hits(text: str, phrases: list[str]) -> list[str]:
    low = text.lower()
    return [p for p in phrases for _ in re.finditer(r"\b" + re.escape(p) + r"\b", low)]


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("draft", type=Path)
    args = ap.parse_args(argv)

    body, found = extract_body(args.draft.read_text())
    if not found:
        print("No ABOUT THIS PET / HOUSEHOLD FIT / TRAINING / GOOD TO KNOW headings found: nothing to check.")
        return 2

    # Program-name lines count as boilerplate, not profile copy.
    prose = "\n".join(ln for ln in body.splitlines() if not any(mk in ln.lower() for mk in PROGRAM_MARKERS))
    words = word_count(prose)
    problems: list[str] = []

    missing = [h for h in HEADINGS if h not in found]
    print(f"Headings missing: {', '.join(missing) or 'none'}")
    problems += [f"missing heading {h}" for h in missing]

    first = re.search(r"^(.*?[.!?])(\s|$)", prose.strip(), re.DOTALL)
    print(f"Opening sentence: {(first.group(1) if first else prose.strip()[:80])!r}")

    print(f"Narrative words: {words} (target 175-250)")
    if not 175 <= words <= 250:
        problems.append(f"word count {words} outside 175-250")

    for label, phrases in (
        ("Social/humanizing words", SOCIAL_WORDS),
        ("Adopter-screening phrases", ADOPTER_CONDITION_PHRASES),
        ("Absolute-claim phrases", ABSOLUTE_CLAIM_PHRASES),
    ):
        found_hits = hits(prose, phrases)
        print(f"{label}: {found_hits or 'none'}")
        problems += [f"{label.lower()} '{w}'" for w in found_hits]

    print(f"Placement constraints (listed, not penalized): {hits(prose, PLACEMENT_CONSTRAINT_PHRASES) or 'none'}")

    if "—" in body:
        problems.append("em-dash present")

    for ln in body.splitlines():
        if any(mk in ln.lower() for mk in PROGRAM_MARKERS) and len(ln.split()) > 25:
            print(f"Program name shares a line with other copy: {ln.strip()[:100]!r}")
            problems.append("give the support sentence its own paragraph")

    print("\nRESULT: " + ("PASS" if not problems else "FIX: " + "; ".join(problems)))
    return 0 if not problems else 1


if __name__ == "__main__":
    sys.exit(main())
