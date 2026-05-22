# On-Page SEO — 8 Practices

The 8 practices below are the audit dimensions for every page this skill touches. They are derived from D&Z's "SEO for Webcopy" reference doc and the broader on-page-SEO consensus. They are project-agnostic — voice / tone / brand vocabulary belong to the project's copy skill.

Each practice is structured as:

- **What it means** — the rule.
- **Why it matters** — the SEO mechanism.
- **How to apply** — concrete moves the copy skill will execute.
- **How to audit** — what to check in existing copy.
- **Severity if violated** — Critical / High / Medium / Low (see `SKILL.md` Phase 3.`review`).

---

## 1. Write for user intent

**What it means:** the page must answer the exact question its locked primary keyword implies. If the keyword has informational intent (e.g., "how does X work"), the page must teach. If commercial intent ("best X for Y"), it must compare. If transactional ("buy X"), it must convert. Mixed intent on one page confuses both readers and search engines.

**Why it matters:** Google ranks pages that match intent. A landing page targeting an informational keyword will lose to a blog post; a blog targeting a transactional keyword will lose to a product page. Intent mismatch is the #1 reason a page fails to rank despite "good" content.

**How to apply:**
- Read the locked brief's `Intent` field. If absent, infer from the keyword + SERP shape captured by `seo-research`.
- Shape the page's opening (hero + first 100 words) to deliver exactly what the intent demands.
- Cut sections that serve a different intent (e.g., don't drop a feature comparison table into a pure informational guide).

**How to audit:**
- Read the hero copy. Does it answer the keyword's implied question in the first sentence?
- Does the CTA stage match the intent (learning vs comparing vs converting)?
- Is the page trying to do two intents at once?

**Severity if violated:** **High** — page may rank, but on the wrong query, with high bounce.

---

## 2. Address frequently asked questions (PAA targeting)

**What it means:** people type full questions into Google ("what is interchange," "how does in-house financing work"). Answering those questions on the page can earn placement in the "People Also Ask" box and feature snippets.

**Why it matters:** PAA + featured snippets carry the highest visibility on a SERP. Even a #4 organic result can earn the snippet box above #1 if the answer format matches.

**How to apply:**
- Read the PAA questions captured during `seo-research` (typically in the spreadsheet's Notes column or `seo_research_report.md`).
- Phrase FAQ headings as full questions (H2 or H3): "How does in-house financing work?" not "In-house financing explained."
- Answer immediately under the heading in **40–50 words**, paragraph or list. Featured snippets prefer this length.
- If the brief has no PAA data, flag it and proceed — don't invent.

**How to audit:**
- Is the FAQ block phrased as questions or marketing labels? Marketing labels lose PAA.
- Is the first sentence after each question a direct, concise answer? Or does it preamble?
- Are answer lengths near the 40–50-word sweet spot?

**Severity if violated:** **Medium** — missed traffic opportunity, but page can still rank.

---

## 3. Make the content organized and easy to digest

**What it means:** the page must be scannable. Bullets, short paragraphs (2–3 sentences max), clear section breaks. Walls of text are punished by both readers and search engines.

**Why it matters:** Google measures dwell time and pogo-sticking (back-to-SERP). A scannable page keeps users on it; a wall of text drives them back. Plus, AI-driven search (SGE, ChatGPT) preferentially cites structured content.

**How to apply:**
- Paragraphs: 2–3 sentences max.
- Lists: bullets or numbers whenever 3+ comparable items appear in prose.
- Section breaks: visible (heading, divider, or whitespace) every ~150 words.
- Each section should advance the page's main goal (CTA, conversion, comprehension).

**How to audit:**
- Find any paragraph >4 sentences. Flag for break-up.
- Is there a section >250 words without a sub-heading or list? Flag.
- Does each section visibly do work toward the page's CTA? Or is it filler?

**Severity if violated:** **Medium** — readability hit, downstream effect on dwell time.

---

## 4. Write clear, descriptive subheadings

**What it means:** every H2 and H3 should tell the reader (and Google) what the section covers. "What We Offer" is dead air. "Affordable In-House Financing for Powersports Dealers" is signal.

**Why it matters:** subheadings carry more SEO weight than body text and are the primary scan path for users. A vague subheading wastes both. Search engines also use heading hierarchy to understand topic decomposition.

**How to apply:**
- Replace generic subheadings ("Our Approach," "What We Do," "Features") with descriptive ones that name the topic AND, where natural, work in a secondary keyword.
- Subheadings should be self-contained — if read in isolation, the reader knows what the section discusses.
- Don't sacrifice clarity for keyword fit. Better: descriptive without keyword > clunky with keyword.

**How to audit:**
- List every H2/H3. For each: would a stranger know what the section is about from the heading alone?
- Are 2+ headings essentially identical or interchangeable? Flag — they need differentiation.
- Are any headings 8 words and contentless? Flag.

**Severity if violated:** **Medium** to **High** depending on how many. One vague heading is recoverable; a page of them is a structural rewrite.

---

## 5. Put keywords in all headlines

**What it means:** the page's primary keyword (or a close variant) should appear in the H1 and ideally in at least one H2/H3. Headlines carry the highest per-token SEO weight on the page.

**Why it matters:** keyword presence in headlines is a strong relevance signal. A page can rank reasonably with the keyword only in body text, but it ranks much better with the keyword in the H1.

**How to apply:**
- H1 must contain primary keyword or a close variant. The locked H1 from `seo-research` already does — don't drift in the copy.
- At least one H2 should reference primary keyword OR a high-priority secondary keyword.
- Don't stuff: "Affordable In-House Financing for Dealers — In-House Financing You Can Afford" is worse than no keyword.
- Variation > repetition: "in-house financing" and "dealer financing" can both appear across H2s if both are in the brief's keyword cluster.

**How to audit:**
- Find primary keyword in H1. Y/N.
- Count H2/H3 occurrences of primary + secondary keywords. Target: primary in 1+ H2 or H3.
- Look for keyword stuffing in any single heading. Flag if present.

**Severity if violated:** **High** — primary keyword missing from H1 is a top-3 SEO sin.

---

## 6. Place keywords strategically throughout the page

**What it means:** keywords should appear near the beginning (first 100 words) AND near the end (closing block / final CTA), not just in the middle. Long-tail variations should appear naturally where the topic invites them.

**Why it matters:** search engines scan the whole page but weigh position. Keyword at the top says "the page is about this." Keyword at the bottom confirms it. Long-tail variations capture related queries the primary keyword misses.

**How to apply:**
- First 100 words: primary keyword once, in flowing prose (not just in the H1).
- Last 100 words (or final CTA section): primary keyword once.
- Body: 1–3 long-tail variations naturally placed where the topic invites them. Don't force.
- Long-tail = specific multi-word variants from the brief's secondary keyword list (e.g., "in-house financing for used vehicles" vs just "financing").

**How to audit:**
- Find primary keyword in first 100 words. Y/N.
- Find primary keyword in last 100 words (or final CTA block). Y/N.
- Count secondary keywords / long-tail variations present in body. Target: 2+ used naturally.
- Look for keyword density >2% on the primary. Flag stuffing.

**Severity if violated:** **High** — keyword placement is a measurable ranking factor.

---

## 7. Support text with relevant images (and write alt text)

**What it means:** images should support the copy, break up text visually, and rank in image search. Each image needs alt text describing what's shown — accessibility + SEO at once.

**Why it matters:** images rank separately in Google Images, can earn featured-image snippets, and improve dwell time. Alt text is required for screen readers (a11y) and is a secondary signal for image SEO. Empty alt = wasted slot.

**How to apply:**
- Every meaningful image slot in `copy/<page>.md` should carry an alt-text field — typically a 1-line description.
- Alt text describes what's literally in the image, not what the brand wants the image to *mean*. "Dealership F&I office with two people at a desk" not "Trust and partnership."
- Where natural, work the primary or a secondary keyword into the alt text — don't force.
- Decorative-only images (gradients, abstract shapes) can use empty alt (`alt=""`) — that's the a11y convention. Flag if alt is missing entirely on a content image.

**How to audit:**
- For each image referenced in `copy/<page>.md`: alt text present? Y/N.
- For each alt text: does it describe what's shown? Or is it generic ("image of our team")?
- Does at least one image's alt text reference the page's primary keyword naturally?

**Severity if violated:** **Medium** for missing alt (a11y issue at minimum); **Low** for present-but-generic alt.

---

## 8. Optimize metadata and alt text

**What it means:** Title tag, Meta description, and alt text are direct SEO signals + influence click-through from the SERP. Each has a budget and a job.

**Why it matters:** Title and Meta are what the user sees on Google before clicking. A great page with a bad Title gets skipped. Meta description doesn't directly influence ranking but heavily influences CTR.

**How to apply:**
- **Title tag:** ≤60 characters. Primary keyword near the front. Click-worthy (curiosity, number, benefit).
- **Meta description:** 150–160 characters. Primary keyword once, naturally. Answer "why should I click this?". Sentence-cased, no all-caps, no clickbait.
- **Alt text:** see practice #7.
- All three should be locked in the `seo-research` brief. This skill's job in `apply` and `refine` modes is to **enforce the lock** — copy must not contradict the brief.

**How to audit:**
- Read `copy/<page>.md` Meta block (or HTML `<title>` / `<meta>` if running on rendered files).
- Title length ≤60? Title contains primary keyword? Y/N each.
- Meta description 150–160 chars? Contains primary keyword once? Y/N each.
- All image references carry alt text? Y/N.

**Severity if violated:**
- Title or Meta drift from locked brief → **Critical**. Blocks deploy.
- Title or Meta exceeds budget → **Critical** (will be truncated on SERP — broken UX).
- Primary keyword absent from Title → **Critical**.
- Primary keyword absent from Meta → **High**.
- Alt text gaps → see practice #7.

---

## Cross-practice tensions

A few real conflicts to watch:

- **Voice "punchy fragment" style vs descriptive subheadings (practice #4).** "No terminals. No card networks. No waiting." is voice-correct but undescriptive as a subheading. Resolution: punchy fragments are body copy or eyebrow text, not section H2s. Section H2s stay descriptive.
- **Keyword density (practice #5/6) vs voice's vocabulary discipline.** If the brand forbids a word that happens to be the primary keyword, that's a re-targeting decision, not a copy decision. Surface to the user.
- **Meta description tone vs voice.** Meta description is read on a SERP, in a different register from the page itself. A slightly more direct / utility-leaning Meta is acceptable even if the page reads more poetic. Voice still applies, but with the "scannable utility" mode active.
- **PAA-style FAQ phrasing (practice #2) vs marketing-voice FAQ phrasing.** Marketing voice prefers "How we keep your data yours"; PAA wants "How does [Brand] handle customer data?". The PAA phrasing wins for the heading; the answer can carry voice freely.

When a tension can't be resolved without breaking one side, **surface it to the user** — do not silently break either rule.
