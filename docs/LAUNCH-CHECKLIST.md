# Launch checklist

- [ ] All sample values replaced in `_build/site.config.json` (name, phone, email, address, hours, prices, provider line). The build prints a warning for any left.
- [ ] `demo_mode` set to `false` (removes noindex and the demo banner); `domain` set to the real domain.
- [ ] Clinic's logo, hero photo and category photos added; drawings no longer in the picture slots.
- [ ] Unoffered treatments removed from `services`; `removed-service-mentions.txt` gone.
- [ ] Every `CLIENT REVIEW` note resolved; medical director has read every treatment page and FAQ (see `COMPLIANCE.md`).
- [ ] Legal drafts reviewed; privacy contact named.
- [ ] FormSubmit activated with a test submission; thank-you page reached.
- [ ] `python3 _build/qa.py` passes with 0 failures.
- [ ] Hosting: Cloudflare Pages project connected, custom domain added, HTTPS on. The `_headers` noindex rule only matches `*.pages.dev`.
- [ ] Google Search Console verified (`google_site_verification`), sitemap submitted.
- [ ] Google Business Profile linked in config (`google_business_profile_url`).
- [ ] Checked on a phone: menu, finder, booking form, call bar.
