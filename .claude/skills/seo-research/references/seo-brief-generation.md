# SEO Brief Generation

> Phase 6 deliverable: a draft Title, Meta description, H1, **and AI Overview readiness block** per page. These are **SEO scaffolding** — they lock keyword placement, length budget, and snippet-ready answer surface. The project's copy skill can refine wording downstream (via `seo-copy-sync`) as long as the constraints survive.

## Inputs that drive the brief

The brief is generated from the per-page row in the `Page Map` tab + each keyword row in the `Keyword Research` tab. The five inputs that matter:

| Input | What it answers | Where it lives |
|---|---|---|
| **Volume** | Demand magnitude | `Keyword Research` col B |
| **KD** | How hard to rank | computed during Phase 4 |
| **Intent** | What the user is trying to do | col C |
| **CPC** | How valuable each click is | col G |
| **SERP Features** | What format the SERP rewards | col H |

Volume + KD answers *should we try*. Intent + CPC + SERP Features answers *how to write the page*. Skipping the last three is the difference between writing a page that ranks and a page that just exists.

## Decision matrix — SERP Features × CPC × Intent

Use this matrix to translate keyword research data into brief decisions before drafting the Title / Meta / H1.

| SERP Feature present | Brief decision |
|---|---|
| **AI Overview** | Write a 40–60 word **snippet-ready paragraph** directly below the H1 (or first H2) that answers the search query literally. Add FAQ schema. Without this, Google's AI Overview eats the click and the page sees zero traffic despite ranking. |
| **People Also Ask (PAA)** | Add a **FAQ section** to the page answering the PAA questions verbatim. PAA presence is explicit signal that informational sub-queries cluster around this keyword. |
| **Featured Snippet** | Put a **40–60 word answer paragraph** right under the relevant H2. This is position-zero real estate. |
| **Local Pack** | Deprioritize **unless** the page is geo-targeted. Local Pack = Google ranks geo-near businesses; a non-local page rarely cracks it. Flag the keyword `low-priority (local)` in `Notes`. |
| **Video / Video Carousel** | Consider embedding a short explainer video or Loom. Pure text pages rank below the video carousel. |
| **Image Pack** | Use original images with descriptive alt text and explicit `<figure>` markup. |
| **Sitelinks on competitor** | A single brand dominates the SERP. Use long-tail variation of the keyword instead of head term. |
| **Discussions and Forums** | Reddit / Quora win the SERP. Add a Q&A section with first-person operator voice; pure marketing copy underperforms. |
| **Things to Know** | The topic is multi-faceted. Use clear H2/H3 hierarchy with sub-topic chunks (not one long flow). |
| **Jobs / Reviews** | Wrong intent for B2B SaaS landings. Reconsider page mapping. |
| **Ads top / Ads middle / Ads bottom** | High paid competition. Organic CTR is depressed; lean harder on differentiator in Meta to earn the click. |

| CPC value | Brief decision |
|---|---|
| **$0** | Almost always pure-informational. Useful for TOFU/blog, not for a landing page. Reconsider page mapping unless intentional TOFU. |
| **$0.01 – $1.99** | Mixed intent. Lean toward differentiator language in Meta to push commercial framing. |
| **$2 – $4.99** | Clear commercial intent. Write the brief expecting cart-warm users. Strong CTA in Meta is mandatory. |
| **$5+** | High-value B2B / contract intent. Treat this page as a top-priority conversion surface — meta CTA, H1 differentiator, persistent in-page CTA, snippet-ready answer. |

| Intent | Brief shape |
|---|---|
| **Informational** | Question-answer Title acceptable for blog/hub; landing pages should still assert a value. Meta = problem + insight + soft CTA. |
| **Commercial** | Title = primary keyword + benefit/differentiator + brand. Meta = problem-solution-CTA. H1 = asserts the value, ends in period. |
| **Transactional** | Title = primary keyword + offer + brand. Meta = direct offer + price/promise + CTA. |
| **Navigational** | User is looking for the brand — usually doesn't need its own brief unless the keyword reveals a competitor-comparison need. |

### Worked example — `embedded credit` for [Brand]

- Volume 30/mo · KD 27 · Intent: Commercial · CPC: assume ~$8 · SERP Features: AI Overview, PAA, Sitelinks
- Decisions:
  - AI Overview present → snippet-ready 50-word paragraph below H1 answering *"What is embedded credit?"* literally.
  - PAA present → FAQ section: *"How is embedded credit different from BNPL?"*, *"Is embedded credit regulated?"*, *"Who issues the credit?"*.
  - CPC ~$8 → high commercial value, write the page as a top conversion surface (persistent CTA, demo as primary).
  - Sitelinks present on competitor → use long-tail variation in H1 (`embedded credit for dealerships`) rather than head term.

## Templates

### Title tag

```
[Primary keyword] [optional modifier] | [Brand]
```

**Rules:**

- **Primary keyword in the first 30 characters.** Google may truncate beyond that depending on pixel width.
- **Total length ≤ 60 characters** (Google's ~580 px desktop cap is roughly 55–60 chars; mobile is shorter).
- **Brand name at the end**, after a pipe (`|`) or em dash (`—`). Pipe is the convention for SEO; em dash is fine but takes a glyph slot.
- **Sentence case or Title Case** — pick one per project and apply consistently. Sentence case reads more human and matches modern brand norms; Title Case looks more traditional.
- **Avoid stuffing.** One primary keyword, one optional modifier. Not three keywords joined by pipes.

**Good examples:**

- `Embedded credit for dealerships | [Brand]`
- `B2B value-back platform pricing | [Brand]`
- `Sports venue payments vs interchange | [Brand]`

**Bad examples:**

- `[Brand] | Embedded credit, value-back, dealerships, sports, entertainment` *(stuffed, brand first wastes ranking real estate)*
- `Welcome to the [Brand] automotive page` *("Welcome to" is filler; no keyword in first 30 chars)*
- `The complete platform for automotive credit and value-back rewards | [Brand]` *(over 60 chars, will truncate)*

### Meta description

**Structure:**

1. **First sentence:** problem or value proposition that contains the primary keyword.
2. **Second sentence (optional):** differentiator — what makes this page's offer distinctive.
3. **Third clause / sentence:** soft CTA — *"see how," "learn more," "book a demo,"* etc.

**Rules:**

- **150–160 characters total.** Google truncates ~155 chars on desktop and ~120 on mobile. Target 155 to be safe.
- **Primary keyword once**, ideally in the first sentence.
- **Avoid:** *"Welcome to…," "On this page…," "Click here…,"* and any meta that doesn't differentiate the page from competitors.
- **No keyword stuffing.** A meta with 4 keyword variations reads like spam and may be replaced by Google with an auto-generated snippet.
- **Active voice.** Imperative or second-person.

**Good examples:**

- `Cut interchange to a sixth on every $1M your dealership processes. Embedded credit and value-back, no card-network handoff. Book a demo today.`
- `Compare [Brand] vs Stripe for B2B embedded credit: pricing, integration time, merchant-owned loyalty. See the side-by-side breakdown.`
- `How much does interchange cost a sports venue per game night? [Brand] charges $6K per $1M vs $36K with Visa/MC. Calculate your savings.`

**Bad examples:**

- `Welcome to the [Brand] automotive page. We have many features. Click here to learn more about how we help dealerships.` *(filler, no keyword, no differentiator)*
- `Embedded credit embedded value embedded payments for dealerships sports venues entertainment retail B2B SaaS.` *(stuffed)*
- `[Brand] is the best embedded credit platform.` *(too short — Google fills with auto-snippet; opportunity wasted)*

### H1

**Rules:**

- **One H1 per page.** Non-negotiable.
- **Sentence case ending with a period** — matches modern editorial convention; the period gives the line breath.
- **Primary keyword used naturally** — don't force-insert. If the keyword can't fit cleanly, the keyword-to-page mapping was probably wrong.
- **≤ 70 characters.** Longer H1s lose impact and split awkwardly on mobile.
- **No questions for landing pages.** Question H1s belong to informational / blog pages. Landing H1s state a value, not ask one.

**Good examples:**

- `Your dealership processes $1M/month on Visa. [Brand] saves you $30,000 of it.`
- `Embedded credit for sports venues, in your team's brand.`
- `A B2B payment platform that pays merchants back.`

**Bad examples:**

- `EMBEDDED CREDIT PLATFORM — BEST IN CLASS FOR DEALERSHIPS` *(ALL CAPS, no period, hype language)*
- `Welcome to [Brand]` *(no keyword, no value)*
- `What if your dealership could keep $30,000 every month?` *(question H1 on a landing page; opens uncertainty instead of asserting)*

### OG Title / OG Description

**Rule of inheritance:** if `og:title` and `og:description` are not explicitly set, Google and social platforms pull from `<title>` and `<meta name="description">`. That's usually correct.

**Set OG fields only when:**

- The page's social share story differs from the SEO story (e.g., social wants the human angle; SEO wants the keyword).
- The Title / Meta truncates badly when shared (rare).
- The page has a strong visual hook that the social caption should reference.

When set, follow the same length budgets:

- `og:title` ≤ 60 chars.
- `og:description` ≤ 160 chars.

Leave the SEO Briefs cells empty when inheritance is sufficient.

### AI Overview readiness block

A per-page block the brief carries alongside Title / Meta / H1. Not a cell in the xlsx — lives in the page's brief section inside `copy/<page>.md` (or wherever the project anchors briefs). Required when the primary keyword's SERP shows `AI Overview` or `Featured Snippet`; optional otherwise.

```
AI Overview readiness:
- Snippet paragraph (40–60 words):
  "[Direct, factual, first-sentence-answers-the-query paragraph that the AI can quote.
   Mentions the primary keyword once, includes the brand once, ends with the
   differentiating fact.]"
- FAQ schema: yes / no (yes if PAA present)
- PAA questions answered (verbatim):
  1. [PAA question 1 from SERP]
  2. [PAA question 2]
  3. [PAA question 3]
- Placement: below H1 (preferred) | below first H2 (acceptable)
```

**Rules:**

- The snippet paragraph must answer the *exact question form* implied by the primary keyword. If the keyword is `embedded credit`, the paragraph opens with "Embedded credit is …". If the keyword is `how does interchange work`, the paragraph opens with "Interchange works by …".
- 40–60 words. Shorter is fine if precise. Longer gets truncated by the AI Overview summary.
- One factual claim per sentence. AI Overviews stitch together citation-ready sentences; rhetorical or comparative sentences get dropped.
- The page's H1 should NOT be a question. The snippet paragraph IS the answer; the H1 still asserts a value.

## The 7-check pass before saving briefs

For each row:

1. **Title** — keyword in first 30 chars, total ≤ 60.
2. **Meta** — problem-then-differentiator-then-CTA structure, 150–160 chars, keyword once.
3. **H1** — sentence case, ends with period, keyword natural, ≤ 70 chars.
4. **Cross-page consistency** — no two pages have the same Title or H1 (would confuse Google).
5. **Brand voice flag** — if the brand has known forbidden words (per the project's copy skill), check none slipped through. Defer to copy skill for canonical voice; flag conflicts in `Notes`.
6. **Honest** — no exaggerated claims, no fake numbers, no superlatives without backing.
7. **AI Overview readiness** — if the primary keyword's SERP carries `AI Overview` or `Featured Snippet`, the brief includes a 40–60 word snippet paragraph + FAQ schema decision + PAA questions answered list. If not present, the field is allowed to be empty with a `(skip — no AI Overview on SERP)` note.

## Hand-off to `seo-copy-sync`

The briefs from this phase are **drafts locked in length and keyword**, **flexible in wording**. When `seo-copy-sync` invokes the project's copy skill to write final copy:

- Keyword presence in title / meta / H1 is non-negotiable.
- Length budget is non-negotiable.
- Exact wording is open to the copy skill's voice rules.

`seo-validate` will check the final rendered page against these locked constraints.

## Anti-patterns

- **Templated title across 20 pages** — `[Product] | [Brand]` on every page kills differentiation. Each page's title earns its primary keyword.
- **Meta that promises the page can't deliver** — overpromise = bounce = lost ranking.
- **H1 that doesn't match the title's promise** — the user clicked through expecting one thing; landing on a different framing causes immediate distrust.
- **Multiple H1s on a page** — semantic HTML error; some renderers fall back to wrong primary keyword inference.
