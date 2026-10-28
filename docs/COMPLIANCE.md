# Compliance notes for med spa sites (Canada / Ontario)

This is not legal advice. It records how the template was written so each clinic's medical director (and, where needed, a lawyer) can review it quickly.

## Prescription-drug advertising
In Canada, advertising a prescription drug to the general public is limited to its name, price and quantity. Neuromodulators are prescription drugs, so the template:
- never names drug brands (Botox, Dysport, Xeomin) or filler brands, and describes treatments generically ("wrinkle-relaxing injections", "a prescription neuromodulator", "hyaluronic acid filler");
- makes no efficacy or result claims beyond general, hedged descriptions ("typically", "results vary").

`qa.py` fails the build if common drug or filler brand names, "permanent results", "pain-free" or "risk-free" appear in page text. If a clinic insists on brand names, get advice first.

## Regulated health professionals
Injectors (RNs, NPs, physicians) are governed by their regulatory colleges, which restrict advertising: no testimonials or patient reviews on the site, no superlatives or comparisons with other providers, no guaranteed outcomes, and care with before/after photos. The template has none of these. Keep it that way unless the clinic's college rules allow it.

## Privacy
Clinics whose health professionals collect health information are generally health information custodians under Ontario's PHIPA. The site:
- asks for no health information (the booking form tells people not to include medical history);
- runs the treatment finder entirely in the browser;
- uses no analytics or cookies.
The privacy policy draft mentions PIPEDA and PHIPA; the clinic must name its privacy contact and confirm its records and booking systems.

## Claims scan
`qa.py` also warns on "best", "#1", "guarantee", "award", years in business and star ratings, which should only appear when the client supplies something verifiable (and even then, check college rules).
