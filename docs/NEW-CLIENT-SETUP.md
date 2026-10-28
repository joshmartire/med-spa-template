# New client setup

Everything client-specific is in `_build/site.config.json`. Edit it, rebuild, run QA.

## 1. Business details
`business_name`, `legal_name`, `domain`, `phone_display` / `phone_e164`, `email`, `privacy_contact`, `address` (a med spa has a storefront, so keep it), `hours`, `hours_note`, `google_business_profile_url`, `social_profiles`, `form_endpoint` (FormSubmit: `https://formsubmit.co/CLIENT-EMAIL`; the first submission sends an activation email that must be confirmed).

Set the real domain in `domain`, keep `base_path` as `/`, and set `demo_mode` to `false` at launch (removes noindex and the demo banner).

## 2. Brand
- `accent`: the brand colour for buttons and highlight panels. It sits behind dark text, so it must be light and bright (the build stops if it's too dark).
- `field_2`: second light panel colour.
- `field_3`: the deep panel colour, behind light text (the build stops if it's too light).
- `logo`: transparent PNG in `assets/img/client/`.
- `hero_claim`: the words in the moving hero line. Short is better (2–4 words). Keep it a philosophy, not a promise of results.

## 3. Treatments and prices
- `services`: delete any slug the clinic doesn't offer. Its pages, menu entries, finder entry, form option and sitemap URLs disappear. Fix any sentences listed in `_build/removed-service-mentions.txt` (QA fails while it exists).
- `prices`: the starting price and unit for each treatment, as the clinic wants it shown. `null` shows "Priced at consultation". `consultation.from: 0` shows "Complimentary".
- `provider_line`: who performs treatments, written by the clinic and checked by its medical director.

## 4. Photos
- `hero_photo`: the square picture in the hero (cropped to a square, darkened slightly so the light type stays readable).
- `category_photos`: one per family (`injectables`, `skin`, `laser`) for the colour sheets.
- `photos`: the clinic's own gallery (see `_build/photos.py`). EXIF data and GPS are stripped.

Only the clinic's own photos. Never stock photos presented as the clinic, its team or its results. Before/after photos need written patient consent and should be checked against the providers' regulatory college rules first.

## 5. Towns
Rewrite `_build/content_cities.py` for the clinic's towns: real neighbourhoods, climate, and a `visit` line with the clinic's actual parking and drive details.

## 6. Review
Search the build files for `CLIENT REVIEW` (about page, provider credentials, FAQ answers, legal drafts) and see `docs/COMPLIANCE.md`.

## 7. Build and test
```bash
python3 _build/build.py && python3 _build/qa.py
```
