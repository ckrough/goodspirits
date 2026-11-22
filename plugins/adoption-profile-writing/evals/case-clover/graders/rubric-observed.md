---
type: llm
weight: 3
focus: {source: file, path: profile.md}
---
Grade the profile in profile.md. If the file is missing or empty, FAIL. Grade only the text under the four headings.

Rubric dimension 3, observed, not promised: every claim reports what was seen, and where ("has played well with the dogs at the shelter"), rather than predicting what the animal will do in a new home ("great with all dogs", "will love your kids", "will settle in fast"). Unknowns are stated as unknown ("has not been tested with cats", "how she does with children is not known"), with no hedge or guess attached. A placement limit on the home ("would do best in an adult-only home") is an observation-backed recommendation, not a promise.

PASS when the profile is observed throughout, with at most one soft generalization. FAIL when it makes a promise or an absolute claim about future behavior, guesses at an unknown ("probably fine with cats"), or contradicts its own disclosures (calls a trait unknown in one place and asserts it in another). Name each one found.
