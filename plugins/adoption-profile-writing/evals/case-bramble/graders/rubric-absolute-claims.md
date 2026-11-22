---
type: regex
weight: 1
target: {source: file, path: profile.md}
match: not_contains
pattern: '\b(great with all|good with everyone|loves everyone|loves all|gets along with all|gets along with everyone|guaranteed|will love your|will be great with|perfect with kids|perfect family dog|the perfect|will do great with|always friendly|never aggressive)\b|100%'
flags: i
---
The profile makes no guarantee about the animal ("great with all dogs", "will love your kids"). Rubric dimension 3, observed not promised, and its absolute_claim flag; the list is the profile grader's ABSOLUTE_CLAIM_PHRASES lexicon.
