# De-identification: case-clover

Techniques are named in ISO/IEC 20889 terms. The source is one animal's shelter-management memo export, its volunteer walk notes and adoption-event notes, a foster's note, and the stay history the shelter-management system records. The ideal is the operator's own published Description for this animal, de-identified the same way.

| Field | Technique | Change |
|---|---|---|
| Animal name and former name | pseudonymization | Replaced with "Clover" in the record and the ideal; the former name removed |
| Other shelter dogs' names (a former housemate, a dog from her building) | pseudonymization | Replaced with "Dog A" and "Dog B" |
| Shelter name and address | pseudonymization | Replaced with "Hollowbrook Animal Rescue"; address removed |
| Shelter ID, microchip number and registry | suppression | Removed |
| Staff, volunteer, and foster names, memo authors | suppression | Removed; entries name the role ("another volunteer", "her foster") |
| Calendar dates | generalization | Rewritten as weeks from intake for the current stay; the earlier stays as "about four years before this intake" |
| Date of birth, exact age, exact weight | generalization | "adult (about 4 years)", "about 46 lb" |
| Adoption-event names and venues | suppression | Replaced with "first off-site event" and "second off-site event" |
| Veterinary clinic and veterinarian names | suppression | Removed with the medical entries |
| Medical entries (an ear concern, X-rays and medication from the earlier stay, recent urine and gum findings, a jaw-muscle condition the vet ruled out) and medical expenses | suppression | Removed as medical detail the profile does not use |
| Earlier stays | generalization | Dates and agency types removed; kept as transfer, adoption, return with its recorded reason, and readoption |
| Published profile from the earlier stay and its page address | suppression | Removed from the record |
| Ideal Description | pseudonymization | The operator's published Description, with the name and shelter replaced and the page-address line removed. To limit the words the three-word pseudonym adds, "came to [shelter]" became "came to the shelter" and "at [shelter] events" became "at adoption events". Three HOUSEHOLD FIT sentences (dogs on the trail, the cat, children) were later rewritten to what the record supports, at the operator's direction, which also makes the text harder to match to the published page. The card measures 279 narrative words on `check_draft.py`, against 250 for the published original |
