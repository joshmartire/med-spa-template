# -*- coding: utf-8 -*-
"""Treatment pages. One entry per service; the build drops any slug not listed in site.config.json "services".

WRITING RULES (keep them when editing):
- No prescription-drug brand names (Botox, Dysport, Xeomin, Juvederm, Restylane...). In Canada, advertising a
  prescription drug to the public is limited to its name, price and quantity, so the pages describe the treatment
  ("wrinkle-relaxing injections", "a prescription neuromodulator") instead. Fillers and devices are also described
  generically so the template fits any clinic. CLIENT REVIEW with the clinic's medical director before launch.
- No promised results, no "best", no before/after promises, no invented statistics. Results vary by person; say so.
- [[slug|anchor]] links to another service, [[contact|...]], [[menu|...]], [[finder|...]] are resolved by build.py.
- "cat": injectables | skin | laser.  "concerns": ids used by the treatment finder (see CONCERNS in build.py).
- "dt": downtime level for the finder: 0 none, 1 a day or two of redness or swelling, 2 several days.
"""

SERVICES = [
# ------------------------------------------------------------------ INJECTABLES
{
"slug": "wrinkle-relaxing-injections",
"name": "Wrinkle-Relaxing Injections",
"cat": "injectables",
"art": "vial",
"short": "A prescription neuromodulator softens the expression lines between the brows, across the forehead and around the eyes.",
"title": "Wrinkle-Relaxing Injections",
"desc": "Wrinkle-relaxing injections for frown lines, forehead lines and crow's feet, performed by licensed injectors after a consultation.",
"h1": "Wrinkle-Relaxing Injections",
"lead": "Soften the lines that come from frowning, squinting and raising your brows, while your face still moves like yours.",
"concerns": ["lines"],
"time": "15 to 30 minutes",
"downtime": "Little to no downtime",
"dt": 0,
"sessions": "Repeated about every three to four months",
"related": ["dermal-fillers", "skin-boosters", "microneedling"],
"body": """<p>Most of the lines people notice first are made by movement. Frowning creases the skin between the brows, raising your eyebrows folds the forehead, and smiling or squinting gathers the skin at the corners of the eyes. Years of the same expressions turn those folds into lines that stay even when your face is at rest. Wrinkle-relaxing injections use a prescription neuromodulator to quiet the small muscles that make those movements, so the skin above them creases less.</p>
<h2>How the treatment works</h2>
<p>After a consultation with a licensed injector, a very small amount of product is placed into specific muscles with a fine needle. The injector maps the dose to how your face moves, which is why the same area can need a different amount on two different people. The aim at {biz} is a softer, rested look: lines relaxed, brows that still lift, and expressions that still read as yours.</p>
<ul>
<li><strong>Frown lines.</strong> The vertical "11s" between the eyebrows.</li>
<li><strong>Forehead lines.</strong> Horizontal lines from raising the brows, treated lightly to keep the brows from feeling heavy.</li>
<li><strong>Crow's feet.</strong> The fan of lines at the outer corners of the eyes.</li>
<li><strong>Other areas.</strong> Some clinics also treat a gummy smile, a dimpled chin, neck bands or jaw clenching. Your injector will tell you what is suitable for you.</li>
</ul>
<h2>What to expect</h2>
<p>The appointment is short and most people return to their day straight away. You may see small bumps at the injection points for under an hour and, occasionally, a little bruising. Results appear gradually over about two weeks, and a follow-up visit lets your injector check the result and adjust if needed. The effect typically lasts three to four months before movement returns, at which point you can decide whether to repeat it.</p>
<h2>Who it suits</h2>
<p>This treatment suits adults who are bothered by expression lines and want a subtle change. It is not suitable during pregnancy or breastfeeding, or with certain neuromuscular conditions and medications, which is why a medical history review comes first. Deep creases that remain at rest may respond better when combined with [[skin-boosters|skin boosters]] or [[microneedling|microneedling]].</p>""",
"cost": "<p>Pricing is usually by area or by unit of product. What you pay depends on how many areas are treated, the strength of the muscles involved and the dose needed to get a natural result. Your injector will confirm the plan and the price at your consultation, before anything is injected, and our [[menu|treatment menu]] lists starting prices.</p>",
"faqs": [
("Will I look frozen?", "Not if the dose suits your face. Our approach is to soften lines while keeping natural movement, and we would rather add a little at your follow-up than overdo it the first time."),
("Does it hurt?", "Most people describe a quick pinch at each point. The needle is very fine and the injections take only a few minutes. Ice can be used beforehand if you are nervous."),
("When will I see results?", "Changes start within a few days and settle at about two weeks. That is why we book a follow-up then, to check the result together."),
],
},
{
"slug": "dermal-fillers",
"name": "Dermal Fillers",
"cat": "injectables",
"art": "vial",
"short": "Hyaluronic acid gel restores lost volume and support in the cheeks, chin, jawline, temples and folds.",
"title": "Dermal Fillers",
"desc": "Hyaluronic acid dermal fillers for cheeks, chin, jawline, temples and smile lines, placed by licensed injectors after a full consultation.",
"h1": "Dermal Fillers",
"lead": "Replace volume where your face has lost it, so you look like yourself on a well-rested day, not like someone else.",
"concerns": ["volume", "lines"],
"time": "30 to 60 minutes",
"downtime": "A day or two of possible swelling",
"dt": 1,
"sessions": "Often lasts six to eighteen months, depending on area",
"related": ["lip-filler", "wrinkle-relaxing-injections", "skin-tightening"],
"body": """<p>As we age, the face slowly loses volume. Fat pads in the cheeks thin and shift, bone changes underneath, and the skin loses some of its support. The result is flatter cheeks, deeper folds from the nose to the mouth, hollow temples and a softer jawline. Dermal fillers are smooth gels, most often made from hyaluronic acid, a sugar your skin already contains. Placed carefully, they restore support and shape where it has faded.</p>
<h2>How the treatment works</h2>
<p>Your consultation starts with how your face looks at rest and in motion, from the front and in profile. A licensed injector then places filler with a fine needle or a blunt-tipped cannula, building gradually and checking symmetry as they go. Different gels are made for different depths and areas, so a cheek and a fine line under the eye are not treated with the same product.</p>
<ul>
<li><strong>Cheeks and mid-face.</strong> Lift and support that also softens the folds below.</li>
<li><strong>Chin and jawline.</strong> Definition and balance in profile.</li>
<li><strong>Temples.</strong> Filling hollows that can make the face look tired.</li>
<li><strong>Smile lines and marionette lines.</strong> Softening folds around the mouth, usually alongside support higher up.</li>
<li><strong>Under the eyes.</strong> An advanced area, assessed carefully, and not right for everyone.</li>
</ul>
<h2>What to expect</h2>
<p>Most appointments take under an hour, including numbing. Many fillers contain a local anaesthetic. Swelling, tenderness and bruising are common for a few days, so avoid booking right before a big event. The result looks softer once swelling settles at about two weeks. Hyaluronic acid fillers break down gradually and can be dissolved by a medical professional if ever needed, which is part of why they are the most common choice.</p>
<h2>Who it suits</h2>
<p>Fillers suit adults who have lost volume or want subtle structure added. They are not used during pregnancy, over active skin infections, or with some medical conditions. We plan conservatively: a natural result often needs less product than people expect, spread across the right places. Many clients pair fillers with [[wrinkle-relaxing-injections|wrinkle-relaxing injections]] for lines caused by movement.</p>""",
"cost": "<p>Fillers are usually priced per syringe. The total depends on how many areas you want to treat, how much volume has been lost and which gel suits each area. Your injector will recommend a plan and give you the price before treatment. Some people spread a larger plan over two visits. Starting prices are on our [[menu|treatment menu]].</p>",
"faqs": [
("How long does filler last?", "It varies by product, area and person. Many hyaluronic acid fillers last from about six months in the lips to a year or more in the cheeks or chin."),
("Can filler be reversed?", "Hyaluronic acid filler can be dissolved with an enzyme by a qualified medical professional. Your injector will explain this, and the risks, at your consultation."),
("Will people be able to tell?", "Our aim is that people notice you look well, not that you have had filler. That means measured amounts, the right product for each area and a follow-up check."),
],
},
{
"slug": "lip-filler",
"name": "Lip Filler",
"cat": "injectables",
"art": "lips",
"short": "Soft hyaluronic acid filler adds shape, definition or hydration to the lips, in proportion to your face.",
"title": "Lip Filler",
"desc": "Lip filler for natural shape, definition, symmetry and hydration, planned in proportion to your face by a licensed injector.",
"h1": "Lip Filler",
"lead": "Shape, definition or a little more fullness, planned around your face so your lips still look like yours.",
"concerns": ["lips", "volume"],
"time": "About 45 minutes",
"downtime": "Swelling for one to three days",
"dt": 1,
"sessions": "Often lasts six to twelve months",
"related": ["dermal-fillers", "wrinkle-relaxing-injections", "hydrating-facials"],
"body": """<p>Lip filler is often thought of as making lips bigger, but most requests are smaller than that. People ask for a clearer border, a little more balance between the upper and lower lip, corners that turn up rather than down, or lips that look less dry and creased. A soft hyaluronic acid filler, made for the movement of the mouth, can do all of those things in measured amounts.</p>
<h2>How the treatment works</h2>
<p>At your consultation your injector looks at the proportions of your lips, your teeth and your profile, and asks what you want to change. They will be honest if a request would look out of balance with your face. Numbing cream is applied first and most lip fillers contain a local anaesthetic. The filler is placed in small amounts, shaping as the injector goes and checking symmetry from several angles.</p>
<ul>
<li><strong>Definition.</strong> A crisper border along the edge of the lip.</li>
<li><strong>Volume.</strong> Gentle fullness, usually starting with half a syringe to a syringe.</li>
<li><strong>Balance.</strong> Correcting one side or one lip that is fuller than the other.</li>
<li><strong>Hydration.</strong> A light, smoothing treatment for fine vertical lines and dryness.</li>
</ul>
<h2>What to expect</h2>
<p>Lips swell more than other areas, so expect them to look larger than the final result for the first day or two. Bruising is possible. Avoid strenuous exercise, alcohol and very hot drinks for the first day, and book well ahead of weddings or photos. The filler settles over about two weeks, which is when your follow-up visit takes place. If you would like more, it is added then rather than all at once.</p>
<h2>Who it suits</h2>
<p>Lip filler suits adults who want a natural-looking change. It is postponed if you have an active cold sore, and if you get cold sores often, your provider may recommend preventive medication from your doctor or pharmacist first. Fine lines around the mouth may also benefit from [[wrinkle-relaxing-injections|wrinkle-relaxing injections]] or a [[hydrating-facials|hydrating facial]].</p>""",
"cost": "<p>Lip filler is typically priced per treatment or per syringe. A first treatment often uses half a syringe to one syringe; correcting asymmetry or building definition can take more. Your injector confirms the amount and the price before starting. Starting prices are listed on our [[menu|treatment menu]].</p>",
"faqs": [
("Will my lips look overdone?", "Not with a measured approach. We start conservatively, in proportion to your face, and add more at follow-up only if you want it."),
("How long does the swelling last?", "Most swelling settles in one to three days, and the final shape shows at about two weeks. Cold compresses help in the first day."),
("How long does lip filler last?", "Lips move constantly, so filler there breaks down faster than in other areas, often in six to twelve months. Many people top up about once a year."),
],
},
{
"slug": "skin-boosters",
"name": "Skin Boosters",
"cat": "injectables",
"art": "drop",
"short": "Fine injections of hydrating hyaluronic acid improve skin quality, glow and fine crepey lines.",
"title": "Skin Boosters",
"desc": "Skin booster injections that hydrate from within for glow, smoother texture and fine lines on the face, neck and hands.",
"h1": "Skin Boosters",
"lead": "Hydration placed under the skin instead of on top of it, for a smoother, brighter surface that does not change your shape.",
"concerns": ["dull", "lines", "texture"],
"time": "About 30 minutes",
"downtime": "Small bumps for a day or two",
"dt": 1,
"sessions": "Usually two or three sessions, a month apart",
"related": ["microneedling", "dermal-fillers", "hydrating-facials"],
"body": """<p>Some skin concerns are not about volume or movement at all. Skin can look dull, feel thin, or show fine crepey lines on the cheeks, neck and the backs of the hands, even when the face has kept its shape. Skin boosters are very fine injections of a thin, hydrating hyaluronic acid. Instead of lifting or shaping, they spread through the skin, attract water and support its quality from within.</p>
<h2>How the treatment works</h2>
<p>After your consultation, the area is cleansed and numbed. A licensed injector then places tiny amounts of product across the treatment area in a grid of small injections, or with a blunt cannula through a few entry points. Because the gel is thin and spreads, it improves the whole surface rather than one feature. Most people need a short course of treatments to build the effect, followed by maintenance.</p>
<ul>
<li><strong>Face.</strong> Glow, hydration and fine lines on the cheeks.</li>
<li><strong>Neck and chest.</strong> Crepey texture and fine horizontal lines.</li>
<li><strong>Hands.</strong> Thin skin that shows veins and tendons.</li>
<li><strong>Around the eyes.</strong> Some products are suitable for fine lines here; your injector will advise.</li>
</ul>
<h2>What to expect</h2>
<p>You will see small raised bumps at the injection points straight after treatment. They usually settle within a day or two, and bruising is possible. Avoid makeup for the rest of the day, and skip strenuous exercise and saunas for twenty-four hours. Skin often feels more hydrated within a couple of weeks, with the full effect building over the course.</p>
<h2>Who it suits</h2>
<p>Skin boosters suit people who want better skin quality without a change in shape. They work well alongside other treatments: [[microneedling|microneedling]] for texture and scarring, [[dermal-fillers|dermal fillers]] where volume has been lost, and a home skincare routine with daily sunscreen to protect the result. They are not used during pregnancy or over active skin infection.</p>""",
"cost": "<p>Skin boosters are priced per session, and many clinics offer the course of two or three sessions at a set price. The total depends on the product, how many areas are treated and how many sessions your skin needs. Your provider will recommend a course and confirm the price at consultation. See our [[menu|treatment menu]] for starting prices.</p>",
"faqs": [
("Are skin boosters the same as filler?", "Both use hyaluronic acid, but skin boosters are much thinner and spread through the skin to hydrate it. They improve quality and glow rather than adding shape."),
("How many sessions will I need?", "Most people start with two or three sessions about four weeks apart, then a maintenance session every six to twelve months."),
("Can I wear makeup afterwards?", "Wait until the next day so the small injection points can close. Gentle cleansing and moisturiser are fine that evening."),
],
},
# ------------------------------------------------------------------ SKIN
{
"slug": "microneedling",
"name": "Microneedling",
"cat": "skin",
"art": "roller",
"short": "Controlled micro-injuries prompt the skin's own repair, improving texture, acne scarring, pores and fine lines.",
"title": "Microneedling",
"desc": "Medical microneedling for acne scars, enlarged pores, uneven texture and fine lines, with a series planned at your skin consultation.",
"h1": "Microneedling",
"lead": "Smoother texture, softer scarring and refined pores, by working with the way your skin already repairs itself.",
"concerns": ["texture", "lines", "dull"],
"time": "About 60 minutes, including numbing",
"downtime": "Redness for one to three days",
"dt": 1,
"sessions": "Usually three to six sessions, four to six weeks apart",
"related": ["chemical-peels", "skin-boosters", "skin-tightening"],
"body": """<p>Your skin is very good at repairing itself. Microneedling, also called collagen induction therapy, uses that ability on purpose. A medical device creates thousands of tiny, controlled channels in the skin. In response, the skin goes through a repair process that, over the following weeks, can improve its texture and firmness. It is one of the most useful treatments for acne scarring, enlarged pores and rough, uneven skin.</p>
<h2>How the treatment works</h2>
<p>Your skin is assessed at consultation, including any active acne, sensitivity or recent sun exposure. On the day, the area is cleansed and a numbing cream is applied for about thirty minutes. The provider then glides a pen-style device over the skin, adjusting the needle depth for each zone: shallower on the forehead, deeper over scarring. A hydrating serum is applied during or after treatment.</p>
<ul>
<li><strong>Acne scarring.</strong> Rolling and boxcar scars soften gradually over a series.</li>
<li><strong>Texture and pores.</strong> Smoother, more even skin with refined pores.</li>
<li><strong>Fine lines.</strong> Especially around the eyes and mouth.</li>
<li><strong>Stretch marks.</strong> Some body areas can be treated; ask at consultation.</li>
</ul>
<h2>What to expect</h2>
<p>Skin looks pink to red, like a mild sunburn, for one to three days and may feel tight or dry. Use gentle skincare only, skip makeup for the first day, and protect your skin from the sun. Because new collagen forms over weeks, results build gradually. Most people need a series of treatments, spaced four to six weeks apart, to see the change they are after.</p>
<h2>Who it suits</h2>
<p>Microneedling suits most skin types, which makes it a good option where some lasers are less suitable. It is postponed with active acne breakouts, cold sores, eczema in the area, or a recent tan. It pairs well with [[chemical-peels|chemical peels]] for pigmentation and with [[skin-boosters|skin boosters]] for hydration.</p>""",
"cost": "<p>Microneedling is priced per session, and a package price is often available for a series. Cost depends on the area treated (face, face and neck, or a body area), whether any add-on serum is used and how many sessions your skin needs. Your provider will recommend a plan at your consultation. Starting prices are on the [[menu|treatment menu]].</p>",
"faqs": [
("Does microneedling hurt?", "Numbing cream is applied first, so most people feel a light scratching or vibration. Bony areas like the forehead can feel more sensitive."),
("How many sessions do I need?", "For texture and fine lines, three sessions is a common start. Acne scarring often needs four to six, a month or more apart."),
("When can I wear makeup?", "Wait at least twenty-four hours so the skin can close. After that, gentle mineral makeup is usually fine; your provider will give you aftercare instructions."),
],
},
{
"slug": "chemical-peels",
"name": "Chemical Peels",
"cat": "skin",
"art": "jar",
"short": "Medical-grade peels lift dull surface cells to brighten tone and soften pigmentation, breakouts and fine lines.",
"title": "Chemical Peels",
"desc": "Medical-grade chemical peels for dull skin, pigmentation, acne-prone skin and fine lines, matched to your skin type at consultation.",
"h1": "Chemical Peels",
"lead": "A brighter, more even complexion by clearing away the dull outer layer and letting fresher skin come through.",
"concerns": ["dull", "spots", "texture"],
"time": "30 to 45 minutes",
"downtime": "Light flaking for a few days with stronger peels",
"dt": 1,
"sessions": "Usually a series of three to six, every two to four weeks",
"related": ["microneedling", "ipl-photofacial", "hydrating-facials"],
"body": """<p>The outer layer of your skin is constantly renewing, but with age, sun exposure and breakouts the process slows and uneven. Dead cells build up, tone becomes patchy and the surface looks dull. A chemical peel applies a controlled acid solution that loosens and lifts that outer layer, so the skin renews more evenly. The word "peel" sounds dramatic, but most medical-grade peels cause light flaking at most.</p>
<h2>How the treatment works</h2>
<p>Your provider chooses the peel for your skin type and goal. Lighter peels use acids such as lactic, mandelic or glycolic acid; others use salicylic acid for oily, breakout-prone skin, or blended formulas for pigmentation. The skin is cleansed, the solution is applied in layers and timed, then neutralised or removed. You may feel warmth or tingling for a few minutes.</p>
<ul>
<li><strong>Brightening.</strong> For dull, tired-looking skin.</li>
<li><strong>Pigmentation.</strong> Sun spots, uneven tone and some types of melasma, as part of a plan.</li>
<li><strong>Breakouts.</strong> Oily, congested skin and post-acne marks.</li>
<li><strong>Fine lines.</strong> Gentle smoothing of the surface.</li>
</ul>
<h2>What to expect</h2>
<p>After a light peel, skin may be pink for a few hours. Stronger peels can cause tightness and flaking from about day two to day five. Do not pick at peeling skin, use gentle skincare only, and wear a broad-spectrum sunscreen every day, because fresh skin is more sensitive to the sun. Results build over a series of peels spaced two to four weeks apart. Between peels, a simple routine of gentle cleanser, moisturiser and sunscreen does more to protect the result than a shelf of new products.</p>
<h2>Who it suits</h2>
<p>Peels can be adapted for most skin types and tones, which is why a consultation comes first. Some medications, recent waxing or a recent tan mean waiting. For deeper pigmentation and redness, a peel series is often combined with an [[ipl-photofacial|IPL photofacial]]; for scarring, with [[microneedling|microneedling]].</p>""",
"cost": "<p>Peels are priced per treatment, and a series is often available at a package price. The cost depends on the type and strength of peel, the area treated and whether it is combined with another treatment such as a facial. Your provider will recommend a series and confirm pricing at consultation; see the [[menu|treatment menu]] for starting prices.</p>",
"faqs": [
("Will my face peel a lot?", "Most medical-grade peels cause light flaking at most, usually from day two to day five. Your provider will tell you what to expect from the peel chosen for you."),
("Can I have a peel in summer?", "Yes, with care. Lighter peels and strict daily sunscreen are usually recommended, and stronger peels may be scheduled for autumn or winter."),
("How soon will I see a difference?", "Many people notice brighter skin within a week of a single peel. Pigmentation and breakouts improve over a series."),
],
},
{
"slug": "hydrating-facials",
"name": "Medical-Grade Hydrating Facials",
"cat": "skin",
"art": "drop",
"short": "A multi-step facial that cleanses, exfoliates, extracts and hydrates, with no downtime.",
"title": "Medical-Grade Hydrating Facials",
"desc": "Hydrating facials that cleanse, exfoliate, extract and infuse serums, for clear, glowing skin with no downtime.",
"h1": "Hydrating Facials",
"lead": "A deep clean, gentle exfoliation and a big drink of hydration, with skin that looks better the same day.",
"concerns": ["dull", "texture"],
"time": "45 to 60 minutes",
"downtime": "No downtime",
"dt": 0,
"sessions": "Monthly, or before an event",
"related": ["chemical-peels", "dermaplaning", "skin-boosters"],
"body": """<p>A hydrating facial is the treatment people book before a wedding, after a long winter or simply once a month to keep their skin in good condition. Unlike a relaxation facial at a day spa, a medical-grade facial uses professional equipment and stronger, results-focused products. It cleans pores more thoroughly than you can at home, exfoliates gently and leaves skin noticeably hydrated, with no recovery time at all.</p>
<h2>How the treatment works</h2>
<p>Your provider starts by looking at your skin and asking about your routine. The treatment then runs in steps, adapted to your skin type and concerns.</p>
<ul>
<li><strong>Cleanse and exfoliate.</strong> A gentle resurfacing step lifts dead skin cells.</li>
<li><strong>Extract.</strong> A vortex-style suction or manual technique clears congestion from pores without harsh squeezing.</li>
<li><strong>Infuse.</strong> Serums with hydrating, brightening or calming ingredients are pushed into fresh skin.</li>
<li><strong>Protect.</strong> Moisturiser and sunscreen finish the treatment.</li>
</ul>
<p>Optional extras can include LED light, a lymphatic massage, a peel booster or [[dermaplaning|dermaplaning]] for an even smoother finish.</p>
<h2>What to expect</h2>
<p>Most people find the treatment comfortable, even relaxing, and many book it as a regular monthly appointment. Skin may be slightly pink for an hour, then looks clearer, plumper and brighter. You can wear makeup the same day, although many people prefer to let their skin breathe. For lasting improvement, a monthly facial keeps pores clear and supports the rest of your routine. Your provider may also suggest a few home products to keep the result going between visits, but there is never any obligation to buy them.</p>
<h2>Who it suits</h2>
<p>Hydrating facials suit nearly every skin type, including sensitive skin, and they are a good first treatment for anyone new to the clinic. They are also useful between stronger treatments such as [[microneedling|microneedling]] or [[chemical-peels|chemical peels]], and as part of a plan before an event. Active rashes, cold sores or a recent sunburn mean rescheduling.</p>""",
"cost": "<p>Facials are priced per treatment, with add-ons such as LED light, dermaplaning or a peel booster priced separately. Many clinics offer a monthly membership or a package of facials. Your provider will suggest what your skin needs and confirm the price before starting. Starting prices are on the [[menu|treatment menu]].</p>",
"faqs": [
("How is this different from a spa facial?", "It uses professional extraction and infusion equipment and results-focused products, chosen after a skin assessment. The goal is visible improvement, not only relaxation."),
("Is there any downtime?", "No. Skin may be slightly pink for an hour. You can return to work and wear makeup the same day."),
("How often should I book?", "About once a month suits most skin, because that is roughly how long the skin takes to renew its surface."),
],
},
{
"slug": "dermaplaning",
"name": "Dermaplaning",
"cat": "skin",
"art": "mirror",
"short": "Gentle manual exfoliation removes dead skin and fine facial hair for a smooth, bright surface.",
"title": "Dermaplaning",
"desc": "Dermaplaning exfoliation that removes dead skin and fine facial hair for smoother skin, easier makeup and better product absorption.",
"h1": "Dermaplaning",
"lead": "A smooth, bright surface in under an hour, with makeup that sits better and skincare that works harder.",
"concerns": ["dull", "texture"],
"time": "About 30 minutes",
"downtime": "No downtime",
"dt": 0,
"sessions": "Every four to six weeks",
"related": ["hydrating-facials", "chemical-peels", "laser-hair-removal"],
"body": """<p>Dermaplaning is a manual exfoliation. A trained provider holds a sterile surgical blade at a shallow angle and uses short, light strokes to lift away the top layer of dead skin cells along with the fine, soft facial hair often called peach fuzz. The skin underneath looks brighter and feels noticeably smooth, makeup goes on more evenly and skincare products absorb better.</p>
<h2>How the treatment works</h2>
<p>The skin is cleansed and dried so the blade glides evenly. The provider works across the face in sections, holding the skin taut, avoiding the eyes, lips and any active breakouts. It does not hurt; most people describe a light scraping feeling. The whole face usually takes fifteen to twenty minutes, and you can see the difference in the mirror straight away. Many people book it as a standalone treatment on a lunch break. A hydrating serum and sunscreen finish the treatment. It is often added to a facial or used before a peel to help the peel work more evenly.</p>
<ul>
<li><strong>Dull skin.</strong> Removing build-up for an instant brighter look.</li>
<li><strong>Makeup texture.</strong> Foundation sits smoothly instead of catching on dry skin and fine hair.</li>
<li><strong>Product absorption.</strong> Serums reach fresher skin.</li>
<li><strong>Before events.</strong> A popular treatment a few days before photos.</li>
</ul>
<h2>What to expect</h2>
<p>There is no downtime. Skin can be slightly pink for an hour and is more sensitive to the sun afterwards, so wear sunscreen daily. A common question is whether the hair grows back thicker. It does not: removing fine vellus hair does not change how it grows, and it returns as the same soft hair over a few weeks.</p>
<h2>Who it suits</h2>
<p>Dermaplaning suits most skin types. It is not recommended over active acne, open wounds or very sensitive, reactive skin, and it is postponed if you have recently used strong retinoids or had a peel. For dark or coarse facial hair, [[laser-hair-removal|laser hair removal]] is a longer-term option. Dermaplaning also pairs well with a [[hydrating-facials|hydrating facial]].</p>""",
"cost": "<p>Dermaplaning is priced per session as a standalone treatment, or as a lower-priced add-on to a facial or peel. Your provider will confirm the price before starting, and our [[menu|treatment menu]] shows starting prices.</p>",
"faqs": [
("Will my hair grow back thicker?", "No. Dermaplaning removes fine vellus hair at the surface and does not affect the follicle, so it grows back the same soft texture."),
("Is it the same as shaving?", "It uses a blade, but it is done by a trained provider with a sterile surgical blade, and it removes dead skin cells as well as hair."),
("Can I have it if I have acne?", "Not over active breakouts. Your provider can work around small areas or suggest a different treatment until skin is calmer."),
],
},
# ------------------------------------------------------------------ LASER & BODY
{
"slug": "laser-hair-removal",
"name": "Laser Hair Removal",
"cat": "laser",
"art": "beam",
"short": "A series of laser sessions gives long-term reduction of unwanted hair on the face and body.",
"title": "Laser Hair Removal",
"desc": "Laser hair removal for the face, underarms, bikini line, legs and back, with a series planned for your skin and hair type.",
"h1": "Laser Hair Removal",
"lead": "Fewer razors, fewer ingrown hairs and smoother skin, with a series of quick sessions planned for your skin and hair.",
"concerns": ["hair"],
"time": "10 to 60 minutes, by area",
"downtime": "Little to no downtime",
"dt": 0,
"sessions": "Usually six to eight sessions, four to eight weeks apart",
"related": ["dermaplaning", "ipl-photofacial", "skin-tightening"],
"body": """<p>Shaving, waxing and plucking only deal with hair that has already grown. Laser hair removal works on the follicle itself. The laser's light is absorbed by the pigment in the hair and turned into heat, which damages the follicle and reduces its ability to grow hair. Over a series of sessions, the result is a long-term reduction in hair, with finer, lighter and fewer hairs growing back.</p>
<h2>How the treatment works</h2>
<p>Your consultation looks at your skin tone, hair colour and medical history, and includes a patch test. The right laser and settings depend on your skin type, which matters for both safety and results. Shave the area the day before. During treatment, a cooling device or gel keeps the skin comfortable while the provider passes the laser over the area in a methodical grid.</p>
<ul>
<li><strong>Face.</strong> Upper lip, chin and jawline.</li>
<li><strong>Underarms and bikini line.</strong> The most popular areas, with fewer ingrown hairs.</li>
<li><strong>Legs and arms.</strong> Larger areas treated quickly with modern devices.</li>
<li><strong>Back and chest.</strong> A common request for men.</li>
</ul>
<h2>What to expect</h2>
<p>Most people describe a quick snap, like an elastic band. Skin may look pink with small bumps around the follicles for a few hours. Treated hairs shed over one to three weeks. Because hair grows in cycles and the laser only affects hairs in the active growth phase, a series of six to eight sessions is usually needed, and some people need occasional maintenance.</p>
<h2>Who it suits</h2>
<p>Laser works most effectively when there is contrast between hair and skin, and modern lasers can treat a wide range of skin tones safely when the right device and settings are used. Very light blonde, grey, red or white hair responds poorly. Avoid tanning, sunless tanner, waxing and plucking during your course. For soft facial fuzz rather than dark hair, [[dermaplaning|dermaplaning]] may suit better.</p>""",
"cost": "<p>Laser hair removal is priced per session by area, with package prices for a full series. Small areas such as the upper lip cost less than large areas such as full legs or the back. Your provider will recommend the number of sessions for your hair and confirm the price at consultation. Starting prices are on the [[menu|treatment menu]].</p>",
"faqs": [
("Is laser hair removal permanent?", "It gives long-term hair reduction rather than permanent removal. Most people see a large reduction after a full series, and some need occasional maintenance sessions."),
("Does it work on darker skin?", "Yes, when the right laser and settings are used. That is why every course starts with a consultation and a patch test."),
("When should I start?", "Autumn and winter are popular, because treated skin must be kept out of the sun and untanned during the course."),
],
},
{
"slug": "ipl-photofacial",
"name": "IPL Photofacial",
"cat": "laser",
"art": "sun",
"short": "Intense pulsed light fades sun spots, redness and broken capillaries for clearer, more even skin.",
"title": "IPL Photofacial",
"desc": "IPL photofacial treatments for sun spots, redness, broken capillaries and uneven skin tone on the face, neck, chest and hands.",
"h1": "IPL Photofacial",
"lead": "Fade sun spots, redness and broken capillaries for clearer, more even skin.",
"concerns": ["spots"],
"time": "About 30 minutes",
"downtime": "Darkened spots for one to two weeks",
"dt": 1,
"sessions": "Usually three to five sessions, about a month apart",
"related": ["chemical-peels", "laser-hair-removal", "microneedling"],
"body": """<p>Years of sun leave their mark as brown spots, freckling and blotchy tone, and many people also have redness or small broken capillaries across the cheeks and nose. An IPL photofacial uses intense pulsed light, a broad spectrum of light filtered to target pigment and blood vessels. The light is absorbed by brown pigment and by the red in small vessels, which are then gradually cleared by the body, leaving skin clearer and more even.</p>
<h2>How the treatment works</h2>
<p>At consultation, your provider confirms that your skin type and the spots in question are suitable for IPL. Some pigment should be checked by a doctor before any light treatment. On the day, a cool gel is applied and you wear protective eyewear. The provider places a smooth glass head on the skin and delivers pulses of light across the area. Each pulse feels like a quick warm snap.</p>
<ul>
<li><strong>Sun spots and freckling.</strong> Brown spots on the face, chest and hands.</li>
<li><strong>Redness.</strong> Diffuse redness and flushing.</li>
<li><strong>Broken capillaries.</strong> Small visible vessels around the nose and cheeks.</li>
<li><strong>Overall tone.</strong> A more even, clearer complexion.</li>
</ul>
<h2>What to expect</h2>
<p>Treated sun spots usually darken, looking like coffee grounds, and then flake off over one to two weeks. Redness may look slightly worse for a day or two before it improves. Wear sunscreen daily and avoid tanning. Most people need three to five sessions about a month apart, then a maintenance session once or twice a year.</p>
<h2>Who it suits</h2>
<p>IPL suits lighter to medium skin tones with visible sun damage or redness. It is not suitable on tanned skin, for some darker skin types, or with certain medications that make skin sensitive to light. Where IPL is not right, a series of [[chemical-peels|chemical peels]] may be recommended instead. Fall and winter are a good time to start.</p>""",
"cost": "<p>IPL is priced per session by area: face, face and neck, chest or hands. A package of three or more sessions is often available. Your provider will confirm how many sessions your skin needs and the price at consultation, and our [[menu|treatment menu]] lists starting prices.</p>",
"faqs": [
("Is IPL the same as a laser?", "Not quite. A laser uses one wavelength of light, while IPL uses a broad spectrum that is filtered for each treatment. Both target pigment or vessels with light."),
("Why do my spots look darker after treatment?", "That is expected. Treated pigment rises to the surface and darkens before it flakes away, usually within one to two weeks."),
("Can I do IPL in summer?", "It works most safely when your skin is untanned and you can avoid strong sun, which is why many people schedule it for fall and winter."),
],
},
{
"slug": "skin-tightening",
"name": "RF Skin Tightening",
"cat": "laser",
"art": "waves",
"short": "Radiofrequency energy gently heats deeper layers of skin to improve firmness on the face, neck and body.",
"title": "RF Skin Tightening",
"desc": "Non-surgical radiofrequency skin tightening for mild laxity on the jawline, neck, under the eyes and body, with no downtime.",
"h1": "RF Skin Tightening",
"lead": "Firmer-looking skin along the jaw, neck and body, with a series of comfortable, no-downtime sessions.",
"concerns": ["laxity", "lines"],
"time": "30 to 60 minutes",
"downtime": "Little to no downtime",
"dt": 0,
"sessions": "Usually four to six sessions, one to two weeks apart",
"related": ["body-contouring", "dermal-fillers", "microneedling"],
"body": """<p>As collagen and elastin decline with age, skin loosens. It shows first as softening along the jawline, crepey skin on the neck, looseness under the eyes and on the stomach or arms. Radiofrequency (RF) skin tightening is a non-surgical treatment that delivers controlled heat into the deeper layers of the skin. That heat tightens existing collagen fibres and prompts the skin to build more over the following months.</p>
<h2>How the treatment works</h2>
<p>Your provider assesses the area and checks that RF is suitable for you. A conductive gel is applied and a handpiece is moved over the skin, gradually raising the temperature in the deeper layers while the surface stays comfortable. Most people describe it as a warm massage. Some devices combine RF with microneedling for a stronger effect on texture as well as firmness.</p>
<ul>
<li><strong>Jawline and jowls.</strong> Mild softening along the lower face.</li>
<li><strong>Neck.</strong> Crepey, loose skin.</li>
<li><strong>Around the eyes.</strong> Fine lines and lid laxity, with an eye-safe applicator.</li>
<li><strong>Body.</strong> Stomach, arms, knees and the skin left behind after weight changes.</li>
</ul>
<h2>What to expect</h2>
<p>Skin can look pink and feel warm for an hour or two, and you can return to normal activities the same day. Some people see a mild tightening straight away, but the main change builds slowly over two to six months as new collagen forms. A series of sessions is usually recommended, with maintenance once or twice a year. Because the change is gradual, photos taken before your first session are the easiest way to see how far your skin has come.</p>
<h2>Who it suits</h2>
<p>RF tightening suits people with mild to moderate laxity who prefer a gradual, non-surgical improvement. It cannot match the result of surgery for significant loose skin, and your provider will tell you honestly if that is the case. It is not used with pacemakers or some metal implants, or during pregnancy. Lost volume may also need [[dermal-fillers|dermal fillers]] for a balanced result.</p>""",
"cost": "<p>RF tightening is priced per session by area, with package prices for a series. The total depends on the area, the device and how many sessions your skin needs. Your provider will recommend a plan and confirm the price at consultation. See the [[menu|treatment menu]] for starting prices.</p>",
"faqs": [
("Is RF tightening painful?", "Most people find it comfortable. It feels like a warm massage, and the provider adjusts the heat to what you can tolerate."),
("When will I see results?", "Some people notice a little firmness straight away, but the main improvement builds over two to six months as new collagen forms."),
("Can it replace a facelift?", "No. It suits mild to moderate laxity. For significant loose skin, surgery gives a stronger result, and your provider will say so honestly."),
],
},
{
"slug": "body-contouring",
"name": "Non-Surgical Body Contouring",
"cat": "laser",
"art": "contour",
"short": "Non-surgical fat reduction treatments target stubborn pockets of fat that do not respond to diet and exercise.",
"title": "Non-Surgical Body Contouring",
"desc": "Non-surgical body contouring for stubborn fat on the stomach, flanks, thighs, arms and under the chin, with no surgery or downtime.",
"h1": "Body Contouring",
"lead": "Treat the stubborn pockets that stay put despite diet and exercise, without surgery and without time off.",
"concerns": ["fat", "laxity"],
"time": "35 to 60 minutes per area",
"downtime": "Little to no downtime",
"dt": 0,
"sessions": "One to three sessions per area",
"related": ["skin-tightening", "laser-hair-removal", "microneedling"],
"body": """<p>Some areas hold on to fat regardless of how well you eat or how much you train: the lower stomach, the flanks, the inner thighs, the backs of the arms and under the chin. Non-surgical body contouring uses controlled cooling, heat or other energy to damage fat cells in a targeted area. Over the following weeks, the body clears those cells naturally, gradually reducing the pocket.</p>
<h2>How the treatment works</h2>
<p>At your consultation, your provider assesses the area, pinches to check that the fat is the kind these devices can treat, and confirms the treatment is suitable for you. An applicator is placed on the area and runs for a set time while you relax, read or work on your phone. Afterwards the area is massaged and you return to your day.</p>
<ul>
<li><strong>Stomach and flanks.</strong> The most commonly treated areas.</li>
<li><strong>Thighs.</strong> Inner and outer thighs.</li>
<li><strong>Arms and back.</strong> Bra-line fat and the backs of the arms.</li>
<li><strong>Under the chin.</strong> A smaller applicator for submental fat.</li>
</ul>
<h2>What to expect</h2>
<p>Redness, numbness, tingling or tenderness in the area are common for a few days to a few weeks. Results appear gradually from about four weeks, with the main change at two to three months. Comfortable clothes on the day make the appointment easier, and you can usually drive home and return to work straight away. Some areas benefit from a second or third session. Treated fat cells are gone, but remaining fat cells can still grow with weight gain, so a stable weight protects the result.</p>
<h2>Who it suits</h2>
<p>Body contouring suits people who are near a weight they are happy with and want to refine specific areas. It is not a weight-loss treatment and is not suitable for some medical conditions, during pregnancy or over hernias. Where skin has loosened too, [[skin-tightening|RF skin tightening]] can be combined for a smoother result.</p>""",
"cost": "<p>Body contouring is priced per area per session, so the total depends on how many areas you treat and whether a second session is recommended. Packages for several areas are often available. Your provider will create a plan and confirm the price at your consultation. Starting prices are on the [[menu|treatment menu]].</p>",
"faqs": [
("Is body contouring a weight-loss treatment?", "No. It is for refining stubborn areas once you are near a stable weight you are happy with. It reduces fat in the treated area, not overall weight."),
("When will I see results?", "Changes start from about four weeks, with the main result at two to three months, as the body clears the treated fat cells."),
("Does it hurt?", "Most people feel intense cold or warmth for the first few minutes, then numbness. Tenderness afterwards usually fades over a few days to weeks."),
],
},
]
