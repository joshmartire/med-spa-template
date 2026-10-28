# -*- coding: utf-8 -*-
"""Copy for the home page and the simple pages (about, FAQ, thank-you, legal).
CLIENT REVIEW: everything here is written for the sample clinic. Replace the story on the about page, check every
FAQ answer with the clinic's medical director, and have the legal drafts reviewed before launch.
Tokens: {biz} business name, {phone} phone; [[key|anchor]] links (service slugs, contact, menu, finder, faq, about,
services, areas, privacy, terms, cookies, area:<city>)."""

GENERAL_FAQS = [
("Do I need a consultation first?", "Yes. Every new client starts with a consultation, and injectables always do. It's where we review your medical history, talk through what you'd like to change, and tell you honestly what we'd recommend, including when that's nothing at all."),
("Is the consultation free?", "Our consultations are complimentary. There's no obligation to book a treatment, and you're welcome to go home and think it over."),
("Who performs the treatments?", "Injectables are performed by licensed health professionals, such as registered nurses and physicians, working under the direction of our medical director. Skin and laser treatments are performed by trained providers who follow the clinic's medical protocols."),
("Will I look natural?", "That's our starting point. We plan in measured amounts, check the result at a follow-up visit and add more only if you want it. Our aim is that people notice you look well rested, not that you've had something done."),
("How should I prepare for my appointment?", "Arrive with clean skin if you can, bring a list of any medications and supplements, and let us know about recent treatments, cold sores, pregnancy or upcoming events. Some treatments need you to stop certain skincare products or avoid the sun beforehand; we'll tell you when you book."),
("Can I combine treatments?", "Often, yes. Wrinkle-relaxing injections and fillers are commonly done together, and skin treatments can be planned around them. Your provider will suggest an order and spacing that keeps you comfortable and safe."),
("How much do treatments cost?", "Starting prices for every treatment are on our [[menu|treatment menu]]. Your price depends on your plan, and it's confirmed at your consultation before any treatment begins."),
("What if I need to reschedule?", "Call or email us as early as you can and we'll find another time. Our full booking and cancellation policy is explained when you book."),
]

APPROACH = {
    "words": ("fresh", "frozen"),
    "captions": ("What we aim for", "What we avoid"),
}


def home(cfg, cities, services):
    city_text = ", ".join(c["name"] for c in cities[:-1]) + " and " + cities[-1]["name"]
    return {
        "desc": f"{cfg['business_name']} is a medical aesthetics clinic in {cities[0]['name']}, ON: injectables, skin treatments and laser, always starting with a consultation.",
        "sentence": f"A consultation-first medical aesthetics clinic in {cities[0]['name']}, with injectables, skin and laser treatments planned to look like you, rested.",
        "fact": "Complimentary consultations",
        "treat_head": "Three ways in",
        "cats": {
            "injectables": ("Injectables", "Wrinkle-relaxing injections, fillers and skin boosters, placed by licensed injectors in measured amounts, with a follow-up visit two weeks later."),
            "skin": ("Skin", "Medical-grade facials, peels, microneedling and dermaplaning for clearer, smoother, brighter skin, adjusted through the seasons."),
            "laser": ("Laser and body", "Laser hair removal, IPL, radiofrequency tightening and body contouring, planned as a course around your skin type."),
        },
        "finder_head": "Find your treatment",
        "finder_lead": "Pick what you'd like to change. We'll show the treatments that address it, how long they take and the downtime to plan for.",
        "approach_head": "Our approach",
        "approach_text": "Good aesthetic work is measured. We start with less, check the result at two weeks and add only if you want more. Faces should still move, and skin should still look like skin.",
        "steps": [
            ("Talk", "A complimentary consultation: your goals, your medical history and an honest recommendation."),
            ("Plan", "A written plan with the treatments, the timing and the price, before anything begins."),
            ("Treat", "Comfortable treatment from a licensed provider, with aftercare explained before you leave."),
            ("Review", "A follow-up visit to check your result and adjust if needed."),
        ],
        "menu_head": "The menu",
        "consult_title": "Your first visit",
        "consult_text": "A relaxed conversation with a provider about your skin and your goals, and a plan you can take home. No obligation.",
        "areas_head": "Close to home",
        "areas_lead": f"Clients come to us from across {cfg['region_label']}. Every area page lists each treatment with notes for that town.",
        "faq_head": "Good questions",
        "close_head": "Still you, just fresher",
        "close_text": f"Book a complimentary consultation in {cities[0]['name']}, and leave with a plan, not a sales pitch.",
        "faqs": GENERAL_FAQS[:5],
        "city_text": city_text,
    }


def simple_pages(cfg, cities, services, city_text):
    biz = cfg["business_name"]
    offered = {x["slug"]: x for x in services}

    def links(slugs, limit=None):
        out = [f"[[{sl}|{offered[sl]['name'].lower()}]]" for sl in dict.fromkeys(slugs) if sl in offered]
        return out[:limit] if limit else out

    def and_join(items):
        return items[0] if len(items) == 1 else ", ".join(items[:-1]) + " and " + items[-1]

    def about(here):
        work = and_join(links([x["slug"] for x in services], 6) or ["aesthetic treatments"])
        return f"""
<!-- CLIENT REVIEW: replace with the clinic's real story: founding year, the medical director's name and licence, each provider's credentials (RN, NP, MD), training, the devices and product lines used, and real photos of the clinic and team. Do not add claims that can't be verified. -->
<h2>Who we are</h2>
<p>{biz} is a medical aesthetics clinic serving {city_text}. Our treatments include {work}.</p>
<p>We started with a simple idea: aesthetic treatments should be planned like any other medical care. That means a real consultation, a medical history review, honest advice about what will and won't help, and a result you can live with every day.</p>
<h2>How we work</h2>
<ul>
<li><strong>Consultation first.</strong> Every new client starts with a conversation, and nothing is booked until you've had time to think.</li>
<li><strong>Licensed providers.</strong> {cfg.get("provider_line", "")}</li>
<li><strong>Measured results.</strong> We start conservatively and review your result at a follow-up visit.</li>
<li><strong>Clear pricing.</strong> Prices are confirmed in writing before treatment. Starting prices are on our [[menu|treatment menu]].</li>
</ul>
<h2>Where we are</h2>
<p>We see clients from across {city_text}. Each town has its own page with notes on every treatment: [[area:{cities[0]['slug']}|{cities[0]['name']}]], [[area:{cities[1]['slug']}|{cities[1]['name']}]] and [[area:{cities[2]['slug']}|{cities[2]['name']}]].</p>
<h2>Before you choose a clinic</h2>
<p>Wherever you go, ask who will perform your treatment and what their licence is, who the medical director is, which products and devices are used, and what happens if you need a follow-up or a correction. A good clinic is glad to answer. When you're ready, [[contact|book a complimentary consultation]] or try the [[finder|treatment finder]].</p>
"""

    def faq(here):
        out = '<h2>Frequently asked questions</h2><div class="faq">'
        for q, a in GENERAL_FAQS:
            out += f'<details><summary>{q}</summary><div class="faq-a"><p>{a}</p></div></details>'
        l = links(["wrinkle-relaxing-injections", "dermal-fillers", "laser-hair-removal", "microneedling"] + [x["slug"] for x in services], 4) or ["our treatments"]
        out += ('</div><h2>Treatment questions</h2><p>Each treatment page answers the questions we hear most about it. Start with '
                + (l[0] if len(l) == 1 else ", ".join(l[:-1]) + " or " + l[-1]) + ', or browse [[services|all treatments]].</p>')
        return out

    def thanks(here):
        return f"""<h2>Your request is with us</h2>
<p>Thanks for contacting {biz}. We'll be in touch by phone or email to confirm your consultation time.</p>
<p>If you need to reach us sooner, call <a href="tel:{cfg['phone_e164']}">{cfg['phone_display']}</a>.</p>
<p>While you wait, you can read about [[services|our treatments]] or our [[faq|frequently asked questions]].</p>"""

    def privacy(here):
        return f"""
<!-- CLIENT REVIEW / LEGAL REVIEW REQUIRED: draft based on the website as built (booking requests through {cfg['form_provider_name']}, static hosting, the treatment finder running in the browser, no analytics or advertising). A clinic whose regulated health professionals collect personal health information is likely a health information custodian under Ontario's Personal Health Information Protection Act (PHIPA), and its clinical records, charting software and booking tools need their own privacy practices. Confirm data handling, retention, the booking and charting systems and the clinic's privacy officer before publishing. If analytics, advertising pixels, chat or online booking tools are added, update this policy. -->
<p><strong>Effective date:</strong> {cfg['policy_effective_date']}</p>
<p>This Privacy Policy explains how {cfg['legal_name']} ("we", "us") collects, uses and protects personal information through this website and when you contact us about our treatments. We handle personal information in accordance with applicable Canadian and Ontario privacy law, including the <em>Personal Information Protection and Electronic Documents Act</em> (PIPEDA) and, for personal health information collected in the course of providing health care, Ontario's <em>Personal Health Information Protection Act</em> (PHIPA).</p>
<h2>Information we collect through this website</h2>
<p><strong>Booking requests.</strong> When you send a consultation request, we collect your name, phone number, email address, the treatments you're interested in, your preferred days and times, whether you're a new or returning client and any message you choose to include.</p>
<p><strong>Please don't send health information through the website.</strong> Our booking form is not designed for medical details. We collect your medical history privately at your consultation, where it becomes part of your clinical record.</p>
<p><strong>Treatment finder.</strong> The treatment finder runs entirely in your web browser. The concerns you select are not sent to us or to anyone else.</p>
<p><strong>Technical information.</strong> When you visit, our hosting provider's servers may automatically log technical information such as your IP address and browser details for security purposes. We do not use analytics, advertising or tracking cookies on this website.</p>
<h2>How we use your information</h2>
<ul>
<li>To respond to your request and book your consultation.</li>
<li>To communicate with you about appointments, treatment plans and aftercare.</li>
<li>To provide care, keep clinical records and meet our professional and legal obligations.</li>
<li>To handle payments, accounting and tax requirements.</li>
</ul>
<p>We do not sell your personal information, and we do not use it for unrelated marketing without your consent.</p>
<h2>Who we share it with</h2>
<p>Booking requests submitted through this website are transmitted through {cfg['form_provider_name']}, a third-party form service that delivers submissions to our email. Service providers we use may store or process information outside Canada, including in the United States and Europe, where it may be subject to the laws of those jurisdictions. We share personal health information only as permitted or required by law, such as with your consent or with other health care providers involved in your care.</p>
<h2>How long we keep it</h2>
<p>We keep booking requests only as long as needed to respond and schedule your visit. Clinical records are kept for the periods required by the regulatory colleges and laws that apply to our health professionals, then securely destroyed.</p>
<h2>How we protect it</h2>
<p>We use reasonable administrative, technical and physical safeguards appropriate to the sensitivity of the information. No method of transmission or storage is completely secure, which is another reason not to include health or financial details in website forms.</p>
<h2>Your choices and rights</h2>
<p>You may ask to access or correct the personal information we hold about you, or withdraw consent to its use, subject to legal restrictions. To make a request, contact us using the details below. If you're not satisfied with our response, you may contact the Information and Privacy Commissioner of Ontario or the Office of the Privacy Commissioner of Canada, depending on the information involved.</p>
<h2>Cookies</h2>
<p>This website does not set cookies. See our [[cookies|Cookie Policy]] for details on the limited browser storage the site uses.</p>
<h2>Contact us</h2>
<p>Questions about privacy can be sent to our privacy contact at <a href="mailto:{cfg['privacy_contact']}">{cfg['privacy_contact']}</a> or by phone at <a href="tel:{cfg['phone_e164']}">{cfg['phone_display']}</a>.</p>
<h2>Changes to this policy</h2>
<p>We may update this policy from time to time. The effective date above shows when it last changed.</p>
"""

    def terms(here):
        return f"""
<!-- CLIENT REVIEW / LEGAL REVIEW REQUIRED: draft website terms. Treatment consent, deposits, cancellation fees, refunds and package terms belong in the clinic's own consent forms and policies. Have the limitation of liability and governing-law sections reviewed by a lawyer. -->
<p><strong>Effective date:</strong> {cfg['policy_effective_date']}</p>
<p>These Terms and Conditions apply to your use of this website, operated by {cfg['legal_name']} ("we", "us"). By using the website, you agree to these terms.</p>
<h2>Not medical advice</h2>
<p>Content on this website, including the treatment finder, is general information about aesthetic treatments. It is not medical advice and does not replace a consultation with a qualified health professional. Whether a treatment is suitable for you depends on your medical history and an in-person assessment. Results vary from person to person, and no particular result is promised.</p>
<h2>Treatment finder and prices</h2>
<p>The treatment finder suggests treatments that commonly address the concerns you select. It is not a diagnosis or a recommendation for you personally. Prices shown on this website are starting prices; your actual price is confirmed at your consultation, before any treatment.</p>
<h2>Bookings</h2>
<p>Sending a request through this website does not confirm an appointment. An appointment is confirmed only when we contact you to confirm it. Treatment consent, deposits, cancellations and refunds are covered by our clinic policies and the consent forms you sign.</p>
<h2>Use of this website</h2>
<p>You may use this website for lawful purposes, such as learning about our treatments and contacting us. You agree not to misuse the website, interfere with its operation, or submit false information through our forms.</p>
<h2>Intellectual property</h2>
<p>The text, design, graphics and logos on this website belong to us or our licensors. You may view and print pages for personal, non-commercial use, but you may not copy or republish website content for commercial purposes without our written permission.</p>
<h2>Third-party services</h2>
<p>This website uses third-party services such as our form provider. We aren't responsible for the content, terms or privacy practices of third parties.</p>
<h2>Limitation of liability</h2>
<p>To the extent permitted by law, we are not liable for any indirect or consequential loss arising from your use of this website or reliance on its general information. Nothing in these terms limits any rights you have under applicable consumer protection law.</p>
<h2>Governing law</h2>
<p>These terms are governed by the laws of the Province of {cfg['legal_jurisdiction']} and the federal laws of Canada that apply there.</p>
<h2>Changes and contact</h2>
<p>We may update these terms from time to time. Questions can be sent to <a href="mailto:{cfg['email']}">{cfg['email']}</a>. Our [[privacy|Privacy Policy]] explains how we handle personal information.</p>
"""

    def cookies(here):
        return f"""
<!-- CLIENT REVIEW: accurate for the template as built (no cookies, no analytics, no pixels; the treatment finder runs in the browser). If Google Analytics, Meta Pixel, Google Ads tags, chat widgets or an online booking embed are added, update this page and add a consent mechanism that blocks non-essential tags until the visitor agrees. -->
<p><strong>Effective date:</strong> {cfg['policy_effective_date']}</p>
<h2>Does this website use cookies?</h2>
<p>No. This website does not set cookies, and it does not use analytics, advertising pixels or other tracking technologies.</p>
<h2>Browser storage we use</h2>
<p>The website uses your browser's <em>session storage</em> to remember that the opening animation has already played during your visit, so it isn't shown on every page. This stores a single value with no personal information, isn't shared with us or anyone else, and is cleared when you close the tab.</p>
<h2>Third-party services</h2>
<p>When you submit our booking form, your browser sends it to {cfg['form_provider_name']}, which delivers it to us by email. That service may show its own pages, such as a spam check, and may use cookies on its own domain under its own policies. Our hosting provider may log technical information such as IP addresses for security purposes, as explained in our [[privacy|Privacy Policy]].</p>
<h2>Managing storage</h2>
<p>You can clear or block site data at any time in your browser settings. The website will still work, although the opening animation may play again.</p>
<h2>Changes</h2>
<p>If we add tools that use cookies or similar technologies, we will update this policy and, where required, ask for your consent before those tools run.</p>
"""

    return {
        "about": dict(title=f"About {biz}", desc=f"{biz} is a consultation-first medical aesthetics clinic serving {city_text}. Meet our approach to natural-looking results.", h1="About us", lead="A medical aesthetics clinic built on consultations, licensed providers and results that still look like you.", inner=about, active="about"),
        "faq": dict(title="Med Spa FAQ", desc=f"Answers about consultations, providers, natural results, preparing for treatment, combining treatments and booking at {biz}.", h1="Questions, answered", lead="What clients ask us most, before they book anything.", inner=faq, active="faq"),
        "thanks": dict(title="Thank You", desc="Your consultation request has been sent.", h1="Thank you", lead="Your request is on its way to us.", inner=thanks, noindex=True, aside=False, cta=False, hero_ctas=False),
        "privacy": dict(title="Privacy Policy", desc=f"How {biz} collects, uses and protects personal information submitted through this website and its booking form.", h1="Privacy policy", lead="How we collect, use and protect your personal information.", inner=privacy, aside=False, cta=False, hero_ctas=False),
        "terms": dict(title="Terms and Conditions", desc=f"Terms and conditions for using the {biz} website, its treatment finder and its booking form.", h1="Terms and conditions", lead="The terms that apply when you use this website.", inner=terms, aside=False, cta=False, hero_ctas=False),
        "cookies": dict(title="Cookie Policy", desc=f"How the {biz} website uses cookies and browser storage.", h1="Cookie policy", lead="What this website stores in your browser, and what it doesn't.", inner=cookies, aside=False, cta=False, hero_ctas=False),
    }
