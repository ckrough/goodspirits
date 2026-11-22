---
type: regex
weight: 1
target: {source: file, path: profile.md}
match: not_contains
pattern: '\b(must have a fenced(-in)? yard|fenced(-in)? yard required|requires a fenced|needs a fenced|qualified adopters only|experienced owners only|experienced adopters only|experienced home only|no apartments|serious inquiries only|not for first-time owners|must apply)\b'
flags: i
---
The profile places no condition on the adopter ("experienced owners only", "must have a fenced yard"). Placement limits on the home, such as "would do best in an adult-only home", are not conditions and are graded per case. Rubric dimension 5; the list is the profile grader's ADOPTER_CONDITION_PHRASES lexicon.
