---
type: regex
weight: 1
target: {source: file, path: profile.md}
match: not_contains
pattern: '\b(buddy|best friend|bestie|companion|sweetheart|sweetie|fur[- ]?baby|baby boy|baby girl|soul ?mate|cuddle ?bug|snuggle bug|lifelong friend|forever friend|little angel|angel|princess|prince charming|gentleman|lady|old soul|love ?bug|velcro dog|shadow)\b'
flags: i
---
The profile uses no social or humanizing word ("buddy", "companion", "sweetheart", "fur baby"). Rubric dimension 4 (Markowitz: social words go with longer listings); the list is the profile grader's SOCIAL_WORDS lexicon.
