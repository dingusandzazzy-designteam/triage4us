# Intent Classification

> Every keyword on the final list has an intent and a funnel stage. Intent decides the *page type*; funnel stage decides the *role in the journey*. Get this wrong and the rest of the work compounds the error.

## The four intent classes

### Informational (TOFU)

The searcher wants to learn something. They're not buying yet.

| Pattern | Examples |
|---|---|
| Question forms | *"what is embedded credit," "how does interchange work," "why are fees high"* |
| Definition / category | *"types of payment processing," "credit card fees explained"* |
| Educational guides | *"guide to merchant pricing," "how to compare credit platforms"* |

**Page types that fit:** blog posts, guides, glossary entries, hub pages with educational angles.

**Common mistake:** mapping informational queries to landing pages. The user isn't ready. They'll bounce.

### Commercial (MOFU)

The searcher is evaluating options. They have a need; they're comparing solutions.

| Pattern | Examples |
|---|---|
| Superlatives | *"best embedded credit platform," "top fintech for dealerships"* |
| Comparisons | *"[Brand] vs Competitor," "Competitor alternatives," "embedded credit comparison"* |
| Use-case framing | *"embedded credit for sports venues," "credit platform for B2B"* |
| Review / opinion | *"X review," "is X worth it," "X case study"* |

**Page types that fit:** landing pages, comparison pages, use-case / industry pages, solution pages, case studies.

**Common mistake:** treating commercial like informational. *"best X"* searchers want a curated list, not a 3,000-word definition essay.

### Transactional (BOFU)

The searcher has decided and wants to act.

| Pattern | Examples |
|---|---|
| Purchase intent | *"buy X," "X pricing," "X cost," "get X"* |
| Direct conversion | *"X demo," "X trial," "X signup," "schedule X"* |
| Discount / deal | *"X promo code," "X discount," "X for free"* |

**Page types that fit:** pricing page, signup / demo-request page, product page, checkout.

**Common mistake:** burying CTA. A transactional searcher who has to scroll to find a form leaves.

### Navigational

The searcher knows where they want to go and is using search as a shortcut.

| Pattern | Examples |
|---|---|
| Brand-specific | *"[brand] login," "[brand] support," "[brand] dashboard"* |
| Site-specific | *"[brand] pricing," "[brand] careers"* |

**Page types that fit:** branded pages — login, support, the brand's own homepage.

**Strategic role:** capture *your own* brand traffic so a competitor doesn't bid on it in paid. Don't optimize for *competitor* navigational queries (low conversion, often penalized).

## Funnel stage

Funnel stage is intent + position in the user's journey:

| Stage | Intent typical | What the page must do |
|---|---|---|
| **TOFU** (top of funnel) | Informational | Build trust, answer the question, soft introduction to brand. |
| **MOFU** (middle of funnel) | Commercial | Differentiate, prove value, comparison shopping. |
| **BOFU** (bottom of funnel) | Transactional | Remove friction, close the conversion. |

Branded queries don't fit cleanly — they're "post-funnel" or "loyalty stage." Treat them as a separate bucket if needed.

## Hard / ambiguous cases

### "X review"

Could be commercial (a buyer comparing) or informational (a researcher learning). Resolve by:

- Looking at the SERP. Vendor landing pages dominating = commercial. Editorial sites (e.g., G2, Capterra, Forbes) = informational mixed with commercial intent.
- Looking at modifiers. *"X review 2026"* trends commercial. *"X review what is it"* trends informational.

Document the call in `Notes`.

### "X for [industry]"

Almost always commercial (a buyer in industry Y looking for X). The page type is a use-case / industry landing page, not a blog.

### "how to [do thing X solves]"

Often informational at the surface but with high commercial conversion potential if the answer naturally leads to "use X." Treat as TOFU informational; let the page funnel readers to a MOFU page via internal links.

### "[brand] vs [brand]"

Commercial. The searcher is comparing two solutions. Treat as a comparison page if you have a defensible angle.

### Single-word queries

Almost always too broad to classify. Either narrow with a modifier or discard. *"credit"* is not a keyword target.

## Workflow: how to classify

For each candidate:

1. Read the term out loud. What is the searcher trying to accomplish?
2. If ambiguous, web-search the term and scan the top 10 result types.
3. Apply the patterns above.
4. If still ambiguous after both, classify by the *dominant* SERP result type and note the ambiguity in `Notes`.

Don't over-engineer this. Most keywords classify in 5 seconds. Ambiguous ones cost an extra minute.

## Intent weights (used in priority scoring)

The Phase 4 scoring formula weights intent:

| Intent | Weight (with-volumes mode) |
|---|---|
| Commercial | 1.5 |
| Transactional | 1.3 |
| Informational | 1.0 |
| Navigational | 0.4 |

Why commercial > transactional? Commercial keywords drive larger volumes and the conversion potential per page is higher when the journey is correctly mapped. Transactional keywords convert better per visit but volumes are smaller.

Override these per niche if the project skews heavily one way. Document the override in the report.
