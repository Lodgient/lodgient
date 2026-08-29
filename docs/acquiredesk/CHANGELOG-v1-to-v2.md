# AcquireDesk v1 → v2: What Was Wrong

Critique of the original specification. Read alongside `SPEC.md`.

v1 is a genuinely strong document — the module decomposition, the scoring
explainability requirement, the human-approval layer, and the
calculations-outside-React rule are all correct and survive into v2 intact. The
problems below are not sloppiness. They are the specific places where the spec
described a *different strategy* than the one stated, and where following it
would cost real money.

---

## CRITICAL — these lose money

### 1. The buy box contradicts the strategy

**Stated goal:** distressed businesses, creative deals, none of our own capital.
**v1 buy box:** $150k+ SDE, 50%+ recurring, manager in place, not owner-dependent.

Those are the most contested assets in small-business M&A. They receive 15+ NDAs,
carry an SBA prequalification letter, and clear at full market multiple to a cash
buyer inside 90 days. Creative terms are what a seller grants *in exchange for* a
discount, and no discount exists on a contested asset.

v1 was built to find deals we cannot win on the terms we want.

**Fix:** v2 §0 separates *distressed business* (a turnaround — no financing
available, no cash flow to service a seller note, consumes operator attention)
from *motivated seller with a healthy business* (nothing wrong with the asset,
everything wrong with the seller's timeline). The second is the thesis. §1 splits
this into two explicit buy boxes with different criteria, sources, and structures.

### 2. AI-adjusted EBITDA can reach the offer engine

v1 §33 renders "Current Value $735,000 → Projected Value $1,420,000" and §11's
valuation engine sits in the same pipeline as §10's AI-adjusted EBITDA. Nothing
in the architecture prevents projected value from anchoring the offer.

This is the most dangerous idea in the document. It is the mechanism by which a
buyer pays 4.5× for a 3× business because a model told them AI will fix it — and
then discovers that the seller captured 100% of the value of work the buyer had
not yet done.

**Fix:** v2 §5 makes this an enforced boundary, not a guideline. `entry_value`
imports nothing from the upside module; a CI dependency rule fails the build on
violation; the offer function's signature cannot accept an upside parameter; and
`owned_value` never renders on the same screen as the offer. Anchoring is not
defeated by being aware of anchoring — it has to be structurally prevented.

### 3. "Founder capital: $0" hides the actual risk

v1 §13's optimizer headlines founder equity of $0 and never mentions the personal
guarantee. SBA requires a personal guarantee from every 20%+ owner. A $487,000 PG
secured against personal assets is *more* personal risk than writing a $100,000
check, not less.

A tool that reports "$0 of your money" next to an unmentioned half-million-dollar
guarantee is a machine for generating confident mistakes.

**Fix:** v2 §7.2 requires founder cash, **PG exposure**, investor waterfall, and
stressed DSCR to be reported together with equal visual weight, on every scenario,
every time.

### 4. No model of competition

v1 scores business quality and nothing else. A 91-scoring listing that is six days
old and SBA-prequalified is a deal we lose after three weeks of work. A
74-scoring business that has sat 11 months with two price cuts is a deal we win.

v1 ranks the first one higher and sends us to lose it.

**Fix:** v2 §2.3 adds a Winnability score. It deliberately rewards *solvable
friction* — messy books, a licensing qualifier requirement, an ugly lease — as
things that suppress competition for reasons that are cheap for us to fix. That
is where the margin actually is.

### 5. Seller motivation is a free-text field nothing consumes

`reason_for_sale` is a string in v1's schema. It is the most predictive variable
in the entire dataset for whether a creative structure is achievable, and it is
inert.

**Fix:** v2 §2.2 makes Motivation a first-class score with weighted, evidenced,
individually-stored signals. §2.2 also keeps v1's correct instinct to exclude
owner age, and names the compliant alternatives that are better predictors
anyway: entity registration age, license issue date, officer continuity.

---

## MAJOR — these waste time and money

### 6. AI upside has no reality clamp

v1 §9's worked example saves $38,000 from a two-person, $90,000 admin function.
A $1.1M-revenue pool route has roughly 1.5 admin heads, one of them the owner's
unpaid spouse. The example describes a business with a back office that businesses
this size do not have.

Unclamped, this module produces exactly the number needed to justify overpaying.

**Fix:** v2 §6.1 adds six enforced clamps — no saving without a referenced P&L
line item, 60% cap on any addressable line, headcount floors, measured baselines
required for revenue lift (speculative opportunities contribute $0 while staying
visible as diligence hypotheses), non-zero implementation cost including operator
hours, and phased ramp rather than step-function savings.

§6.3 also ranks the levers honestly for this business size — and notes that the
top two reliable ones (collections and price realization) are not AI at all. The
credibility of the module depends on not claiming credit for basic management.

### 7. Off-market is buried at §20

The four listing portals are a commodity feed of the most-viewed inventory in the
market. Their real value is comps, not deals.

**Fix:** v2 §3 inverts the priority and specifies the actual data: Sunbiz bulk
entity data, DBPR license data, **UCC-1 filings** (the best available distress and
collateral signal — MCA filers are highly motivated sellers; lapsing filings mean
debt-free equipment), tax liens, judgments, FMCSA fleet data, Google Places. The
cross-reference is the moat, and no competing buyer has assembled that view.

§3.2 also replaces portal scraping with **broker email-alert ingestion** —
legally clean, avoids the entire ToS question, and is genuinely faster since new
listings hit email before they are indexed. §3.4 makes `legal_basis` a required
declaration on every connector, gated in code.

### 8. Missing the structures that answer the actual question

v1 lists eight capital sources — all conventional. Absent: full seller carry,
**management agreement with purchase option** (the single best fit for
"no capital" — you run it for a fee with an option struck at today's price, and
walk if the books lie), self-liquidating revenue-share, real-estate carve-out with
leaseback, key-employee rollover, consulting/non-compete allocation, debt
assumption, working-capital arbitrage, Article 9 asset purchase, and — most
importantly — **tuck-in acquisitions against holdco capacity.**

That last omission matters most: v1 models every deal standalone. Buying deal #2
against deal #1's cash flow and borrowing base is how founder capital actually
reaches zero, and it is the entire reason to have a holdco.

**Fix:** v2 §7.1 specifies twelve structure templates, each with its own
constraints and disclosures.

### 9. Nothing models the seller's after-tax outcome

We intend to win on terms rather than price. Winning on terms requires knowing the
seller's after-tax position better than they do — and most sellers of $1M
businesses have never modeled theirs, because their broker only models gross
price.

**Fix:** v2 §8 specifies a seller net-proceeds engine with purchase price
allocation and installment-sale (§453) comparison. The worked example pays
$60,000 *more* nominal, $358,000 *less* cash, and nets the seller $45,000 more
after tax. That is not a trick — it is genuine tax-deferral efficiency, both sides
are better off, and it is the entire reason creative structuring works.

No competing tool does this. It is the highest-leverage missing feature in v1.

### 10. SBA rules hardcoded as facts

v1 §12 lists "SBA acquisition loan" as a capital source with no rule encoding. SBA
equity-injection requirements, standby-note treatment, seller-role restrictions,
and guarantee thresholds change materially between SOP revisions.

**Fix:** v2 §7.1/S2 requires every SBA rule to be a versioned, cited, editable
parameter carrying `sop_version` and `effective_date`, with warnings when a model
used a superseded version and mandatory lender confirmation before any offer
relies on one. Every SBA number is a lender-confirmable input, never a constant.

### 11. Analyze-everything is the wrong funnel shape

v1 runs full analysis on all ingested deals. Attention is the binding constraint;
inference spend is the secondary one.

**Fix:** v2 §4 adds a deterministic kill gate ahead of any model call — with
**license transferability first**, because in Florida it kills more deals than bad
financials and belongs at the top of the funnel rather than in diligence. Plus a
three-stage cost cascade (deterministic → small model → frontier model on the top
5–10%) with per-deal token accounting and cost-per-qualified-deal on the dashboard.

The DSCR gate is the useful subtlety: rather than discarding a deal that fails at
the asking price, the system computes the price at which DSCR = 1.35 and re-ranks
it there. Often the business is fine and only the ask is fantasy.

### 12. The feedback loop is named but not designed

v1 §37 correctly calls predicted-vs-actual the long-term asset, then specifies no
schema for it. A feedback loop not designed in on day one cannot be retrofitted,
because the data was never captured.

**Fix:** v2 §10 specifies capture from deal one of every offer and its outcome,
every lost deal and its clearing price, every passed deal with a scheduled
12-month lookback, and monthly predicted-vs-realized per opportunity.

Note which of these is most valuable: **our own offer-outcome history.** Within a
year it tells us our real winning price by sector, seller type, and structure.
That is worth more than the upside model, and v1 captured none of it.

### 13. The 18-feature "MVP"

v1 §31's MVP includes a conversational analyst and a daily autonomous agent — a
year of work that front-loads the features which only matter once deal flow exists.

**Fix:** v2 §12 specifies a two-week v0.1: paste a listing, normalize it, score
it, structure it, model the seller's proceeds. Nine features. Use it on twenty
real deals before building anything else.

---

## MODERATE

### 14. Add-back handling is too permissive

v1 §16 correctly requires human approval. It does not distinguish *verified* from
*plausible* from *seller-claimed*. Add-backs are where small-business M&A fraud
lives, and where our own optimism does the most damage.

**Fix:** v2 §9.3 permits only `verified` add-backs into normalized EBITDA and
surfaces the seller's-number-vs-our-number gap as a negotiating asset. A seller
claiming $85,000 of add-backs against $31,000 verified has told us something
important about both the business and the seller.

### 15. No provenance model

v1 requires audit logs on AI-generated changes. It does not require that every
*number* trace to a source. Without this, a hallucinated revenue figure is
visually indistinguishable from a tax-return figure at the moment of decision.

**Fix:** v2 §9.2 specifies a `Provenance` union on every monetary value,
integer-cents money (never floats), visually distinct rendering for LLM-derived
values, a prohibition on unapproved LLM values entering calculations, and an
`explain(valueId)` function returning the full input tree.

### 16. Stack over-specified and over-built

Redis + BullMQ + separate NestJS "if cleaner" + S3 + pgvector + Clerk-or-Auth0,
for an internal tool with a handful of users. Every service is something that
breaks at 2am.

**Fix:** v2 §9.1 — Next.js, one Postgres, one worker (`pg-boss` on the same
database), Clerk, Sentry. Add Redis when queue depth justifies a second
datastore; add pgvector when full-text stops being enough.

### 17. Single blended score destroys signal

Averaging quality, financing feasibility, and AI potential into one 0–100 number
means a 78 can mean "excellent business we cannot win" or "mediocre business we
can steal." Those require opposite actions.

**Fix:** v2 §2.5 keeps four independent scores and routes on rules rather than a
blended threshold — including a WATCH state that revisits unwinnable good
businesses at day 120/180/240. The deal that was unwinnable in March is often
winnable in October, and v1 had no way to express that.

### 18. Compliance gaps in outreach

v1 correctly forbids autonomous LOIs. It omits TCPA and Florida's unusually strict
telephone solicitation statute for cold SMS, CAN-SPAM for email, Florida's
all-party consent requirement for call recording (which the proposed AI voice
agent would immediately violate), and the principal-vs-broker distinction.

**Fix:** v2 §11, with the AI-voice consent and no-offer constraints enforced in
the outreach service rather than stated as policy.

### 19. Missing stress testing

v1 computes DSCR. It never stresses it. A deal at 1.35× base that breaches
covenant at -12% revenue in a seasonal Florida service business is not financeable,
and we should learn that in minute three rather than month three.

**Fix:** v2 §7.3 mandates a stress panel on every structure: revenue -15% and
-25%, loss of largest customer, +200bp on floating debt, 60-day AR slowdown, plus
covenant modeling and months-of-reserve.

---

## WHAT v1 GOT RIGHT

Worth stating plainly, because these are the parts most specs get wrong:

- **Scoring explainability with no black boxes** (§36). Correct and non-negotiable.
- **Financial calculations outside React, unit tested** (§35). Correct.
- **Deterministic scoring with LLMs assisting interpretation only** (§8). Exactly
  the right division of labor.
- **Human approval on anything legally meaningful** (§29). Correct.
- **Abstract LLM provider layer** (§3). Correct and unusually foresighted.
- **Never present AI-adjusted EBITDA as guaranteed** (§10). The right instinct —
  v2 only adds the architecture that enforces it.
- **Excluding owner age from scoring** (§20). Correct, and rarer than it should be.
- **Add-backs require human approval** (§16). Correct, just needs the verification
  tiers.
- **The module decomposition** (§35). Sound. v2 keeps it nearly unchanged.
- **The UX thesis** (§30). Bloomberg + Linear + deal room is right for this user.

The bones are good. v2 changes what the machine *points at*, and adds the
guardrails that stop it from talking us into a bad deal with great-looking numbers.
