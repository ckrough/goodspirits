"""Check an adoption-profile draft against the rubric's mechanical rules.

Standard library only. Run from anywhere:

  python3 scripts/check_draft.py DRAFT.md

The draft is markdown with the four section headings (ABOUT THIS PET, HOUSEHOLD FIT,
TRAINING, GOOD TO KNOW), bold or ATX, with or without a trailing colon. Frontmatter, a
title, and any heading after the profile that is not one of the four (an "Open items" or
boilerplate block) are ignored.

Checks: all four headings, 175-250 narrative words (and whether a miss is within 20% of
the band, 140-300, or past it, where the grader takes most of the length points),
struggle sentences over 20% of the card, negative trait words and traits named to deny
them (positive trait labels are listed for review, not failed), social/humanizing words, adopter screening phrases, absolute claims, platitudes,
em-dashes, a program-name sentence sharing a line with other copy, and, on a card that names the Diamond Dog program, the Diamond Dog message word for word, after any senior program block.
A page address on its own line above ABOUT THIS PET is reported, not required. Placement constraints are listed but never counted against the draft.
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

# Filler: mood with no fact behind it. Deleting one removes nothing an adopter could check.
PLATITUDE_PHRASES = [
    "forever home", "furever", "so much love to give", "full of love", "heart of gold",
    "steal your heart", "melt your heart", "one of a kind", "the whole package", "zest for life",
    "enthusiasm for life", "looking for his person", "looking for her person",
    "waiting for his person", "waiting for her person", "deserves a home", "deserves a family",
    "deserves a second chance", "lucky family", "lucky adopter", "won't last long",
    "what are you waiting for", "words can't describe",
]

# Trait labels went with longer listings, positive ones included (Nakamura et al. 2019).
# Positive labels are listed for review: one beside the behavior that shows it can stay.
POSITIVE_TRAIT_LABELS = [
    "friendly", "gentle", "quiet", "sweet", "loving", "affectionate", "loyal", "smart",
    "intelligent", "obedient", "trainable", "well-behaved", "well-mannered", "mellow",
    "laid-back", "easygoing", "easy-going", "energetic", "active", "high energy", "high-energy",
    "happy-go-lucky",
]

# Negative trait words: the costliest way to report a struggle. Write the behavior instead.
NEGATIVE_TRAIT_LABELS = [
    "timid", "shy", "fearful", "nervous", "anxious", "sensitive", "dominant", "submissive",
    "hyperactive", "excitable", "reactive", "aggressive", "stubborn", "pushy",
]

# Naming a trait to deny it plants the question it answers.
TRAIT_DENIAL_PHRASES = [
    "not aggressive", "no aggression", "not dominant", "not reactive", "not hyperactive",
    "not food aggressive", "no resource guarding", "doesn't guard", "does not guard",
    "no behavior issues", "no behavioral issues", "doesn't have a mean bone", "not a mean bone",
]

# Support and closing sentences in GOOD TO KNOW. Not struggles, so the struggle share leaves them out.
SUPPORT_LINE_MARKERS = (
    "diamond dog", "training support", "meet-and-greet", "meet and greet", "full history",
    "go over his history", "go over her history", "go over their history",
    "thank you for considering", "start by submitting an application", "adoption application",
)

# A Diamond Dog's card carries this message word for word (references/profile-template.md).
DIAMOND_DOG_SNIPPET = (
    "[Name] is a [Shelter] Diamond Dog: [Shelter] provides training and guidance to help you settle "
    "[him/her] into [his/her] new home, at no cost to you. "
    "To meet [Name], please submit an adoption application. [Shelter] will then begin the "
    "matchmaking process, go over [his/her] full history with you, and set up a meet-and-greet. "
    "Thank you for considering [Name]!"
)


def _normalize(text: str) -> str:
    text = text.replace("’", "'").replace(" ", " ").replace("*", "").replace("_", " ")
    return " ".join(text.lower().split())


def _has_snippet(template: str, text: str) -> bool:
    """`template` with any name in the [Name] slots and any shelter name in the [Shelter] slots
    (the same one each time), either pronoun, and the final period optional."""
    pattern = re.escape(_normalize(template).rstrip("."))
    for slot, alt in (("[his/her]", "(?:his|her)"), ("[him/her]", "(?:him|her)")):
        pattern = pattern.replace(re.escape(slot), alt)
    for slot, group in (("[name]", "name"), ("[shelter]", "shelter")):
        first, *rest = pattern.split(re.escape(slot))
        if rest:
            pattern = first + rf"(?P<{group}>[\w'&. -]+?)" + rest[0] + "".join(rf"(?P={group})" + part for part in rest[1:])
    return re.search(pattern, _normalize(text)) is not None


def has_diamond_dog_snippet(text: str) -> bool:
    return _has_snippet(DIAMOND_DOG_SNIPPET, text)


# Lines naming a program are often stripped as boilerplate by scoring tools.
PROGRAM_MARKERS = ("senior care plan", "senior program", "grey muzzle", "waives the adoption fee", "waives her adoption fee", "waives his adoption fee", "reimburses up to")

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


def extract_body(text: str) -> tuple[str, list[str], dict[str, str]]:
    """Profile prose under the four headings, the headings found, and each section's prose."""
    text = re.sub(r"\A---\n.*?\n---\n", "", text, flags=re.DOTALL)
    out: list[str] = []
    found: list[str] = []
    sections: dict[str, list[str]] = {}
    for line in text.splitlines():
        h = heading_of(line)
        if h:
            found.append(h)
            sections.setdefault(h, [])
            continue
        if found and _MD_HEADING.match(line):
            break
        if found:
            out.append(line)
            sections[found[-1]].append(line)
    return "\n".join(out), found, {h: "\n".join(lines) for h, lines in sections.items()}


_PAGE_ADDRESS = re.compile(r"^<?https?://\S+?>?$")


def page_address(text: str) -> str | None:
    """The last non-blank line before the first section heading, if it is a bare web address."""
    text = re.sub(r"\A---\n.*?\n---\n", "", text, flags=re.DOTALL)
    before: list[str] = []
    for line in text.splitlines():
        if heading_of(line):
            break
        if line.strip():
            before.append(line.strip())
    return before[-1] if before and _PAGE_ADDRESS.match(before[-1]) else None


def drop_program_lines(text: str) -> str:
    """Program-name lines count as boilerplate, not profile copy."""
    return "\n".join(ln for ln in text.splitlines() if not any(mk in ln.lower() for mk in PROGRAM_MARKERS))


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

    body, found, sections = extract_body(args.draft.read_text())
    if not found:
        print("No ABOUT THIS PET / HOUSEHOLD FIT / TRAINING / GOOD TO KNOW headings found: nothing to check.")
        return 2

    prose = drop_program_lines(body)
    words = word_count(prose)
    problems: list[str] = []

    missing = [h for h in HEADINGS if h not in found]
    print(f"Headings missing: {', '.join(missing) or 'none'}")
    problems += [f"missing heading {h}" for h in missing]

    first = re.search(r"^(.*?[.!?])(\s|$)", prose.strip(), re.DOTALL)
    print(f"Opening sentence: {(first.group(1) if first else prose.strip()[:80])!r}")

    print(f"Narrative words: {words} (target 175-250)")
    if 140 <= words <= 300 and not 175 <= words <= 250:
        problems.append(f"word count {words} outside 175-250 (within 20%: loses a quarter of the length points)")
    elif not 140 <= words <= 300:
        problems.append(f"word count {words} more than 20% outside 175-250 (loses most or all of the length points)")

    # Long struggle sentences cap the grader's struggle balance (rubric 1.6): over 20% of the
    # card caps it at 3 of 4. The support sentence and closing lines are not struggles.
    gtk = drop_program_lines(sections.get("GOOD TO KNOW", ""))
    struggle = sum(
        word_count(s)
        for s in re.split(r"(?<=[.!?])\s+", strip_markup(gtk))
        if not any(mk in s.lower() for mk in SUPPORT_LINE_MARKERS)
    )
    share = struggle / words if words else 0.0
    print(f"Struggle sentences in GOOD TO KNOW: {struggle} words, {share:.0%} of the card (target under 20%, one or two struggles)")
    if share > 0.20:
        problems.append(f"struggles are {share:.0%} of the card (over 20%): move a struggle to the history review")

    for label, phrases in (
        ("Social/humanizing words", SOCIAL_WORDS),
        ("Adopter-screening phrases", ADOPTER_CONDITION_PHRASES),
        ("Absolute-claim phrases", ABSOLUTE_CLAIM_PHRASES),
        ("Platitudes", PLATITUDE_PHRASES),
    ):
        found_hits = hits(prose, phrases)
        print(f"{label}: {found_hits or 'none'}")
        problems += [f"{label.lower()} '{w}'" for w in found_hits]

    denials = hits(prose, TRAIT_DENIAL_PHRASES)
    without_denials = prose.lower()
    for d in TRAIT_DENIAL_PHRASES:
        without_denials = re.sub(r"\b" + re.escape(d) + r"\b", " ", without_denials)
    negative = hits(without_denials, NEGATIVE_TRAIT_LABELS)
    print(f"Negative trait words: {negative or 'none'}")
    problems += [f"negative trait word '{w}': write the behavior instead" for w in negative]
    print(f"Traits named to deny them: {denials or 'none'}")
    problems += [f"denial '{w}': say what the dog does, or nothing" for w in denials]
    print(f"Positive trait labels (review: keep only beside the behavior that shows them): {hits(prose, POSITIVE_TRAIT_LABELS) or 'none'}")

    print(f"Placement constraints (listed, not penalized): {hits(prose, PLACEMENT_CONSTRAINT_PHRASES) or 'none'}")

    if "—" in body:
        problems.append("em-dash present")

    if "diamond dog" in prose.lower():
        ok = has_diamond_dog_snippet(prose)
        print(f"Diamond Dog message: {'present' if ok else 'missing or reworded'}")
        if not ok:
            problems.append("use the Diamond Dog message from references/profile-template.md word for word")

    address = page_address(args.draft.read_text())
    print(f"Page address above ABOUT THIS PET: {address or 'none (optional)'}")

    # A senior program block is boilerplate and stripped from `prose`, so read `body`.
    lowered = body.lower()
    if "diamond dog" in lowered:
        program_at = [lowered.find(mk) for mk in PROGRAM_MARKERS if mk in lowered]
        if program_at and max(program_at) > lowered.find("diamond dog"):
            problems.append("put the senior program block before the Diamond Dog message")

    for ln in body.splitlines():
        sentences = [s for s in re.split(r"(?<=[.!?])\s+", ln.strip()) if s]
        if sentences and all(any(mk in s.lower() for mk in PROGRAM_MARKERS) for s in sentences):
            continue  # a program block on its own line
        if any(mk in ln.lower() for mk in PROGRAM_MARKERS) and len(ln.split()) > 25:
            print(f"Program name shares a line with other copy: {ln.strip()[:100]!r}")
            problems.append("give the support sentence its own paragraph")

    print("\nRESULT: " + ("PASS" if not problems else "FIX: " + "; ".join(problems)))
    return 0 if not problems else 1


if __name__ == "__main__":
    sys.exit(main())
