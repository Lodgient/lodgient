# AcquireDesk — Platform Specification v2

Private acquisition operating system. Not a marketplace. Internal only.

**What changed from v1 and why** is documented in `CHANGELOG-v1-to-v2.md`. This
document is the build spec.

---

## 0. THE STRATEGIC CORRECTION

v1 optimized for finding *good businesses*. Good businesses are not the
constraint — they are visible to 100,000 buyers on the same four websites, and
they clear at market price to whoever brings the most certain money fastest.

The constraint is **winning a good business on terms where we contribute little
or no cash.** That is a fundamentally different search problem, and it changes
what the software must do.

### The actual arbitrage

Separate two things v1 conflated under "distressed":

**Distressed business** — declining revenue, negative or thin EBITDA, defaulted
debt. Cheap, but: banks won't lend, SBA won't touch it, and a seller note is
worthless because there is no cash flow to service it. This is a turnaround. It
consumes operator attention, which is our scarcest asset. We will do these, but
rarely and deliberately.

**Motivated seller, healthy business** — the business is fine and boring and
throws off cash. The *seller* is the distressed party: 66 years old with no
successor, health event, divorce, partner dispute, burned out, listed 14 months
with no offers, listing agreement just expired. Nothing is wrong with the asset.
Everything is wrong with the seller's timeline.

**This second category is the entire thesis.** It is where a seller will carry
paper, accept an earnout, take an installment sale for tax reasons, or hand over
a management agreement with a purchase option — because time and certainty are
worth more to them than the last 15% of price.

The platform's primary job is therefore not "score businesses." It is:

> **Find businesses where quality is high, competition is low, and the seller's
> personal situation makes structure more valuable to them than price.**

### The three questions v1 never asks

1. **Can we actually win this?** v1 has no model of competition. A 91-scoring
   listing that is 6 days old, SBA-prequalified, and represented by a top broker
   is a deal we will lose. It should rank *below* a 74-scoring business that has
   sat for 11 months with two price cuts.
2. **Why is the seller selling, how badly, and by when?** This is the single
   highest-value field in the system and v1 has it as one free-text column
   (`reason_for_sale`) that nothing consumes.
3. **What does the seller actually net?** We win on terms, not price. To win on
   terms we have to know the seller's after-tax outcome better than they do.

### The rule that keeps us solvent

> **We never pay for value we create.**

v1 §33 shows "Current Value $735,000 → Projected Value $1,420,000." If that
second number is anywhere near the offer engine, we will hand our own future
work to the seller for free. This is the most dangerous idea in the v1 document
and §5 of this spec turns it into an enforced architectural boundary.

---

## 1. TWO BUY BOXES

One buy box cannot express both strategies. Build `BuyBox` as a first-class,
versioned, user-editable entity. Ship with two.

### BUY BOX A — "Cash Cow" (target: ~80% of deal flow)

Healthy business, motivated seller. This is the default.

| Criterion | Range |
|---|---|
| Geography | FL first (Tampa/Orlando/Jax/SW FL), then contiguous Southeast |
| Purchase price | $150k – $2.0M |
| Revenue | $300k – $5M |
| SDE | $150k+ (hard floor $100k) |
| Recurring / contracted revenue | 40%+ preferred, 60%+ excellent |
| Employees | 2 – 30 |
| Customer concentration | No customer > 20% of revenue |
| Revenue trend | Flat or growing over trailing 3 years |
| Owner role | Not the primary salesperson |
| **Licensing** | **Transferable, or a licensed qualifier stays / is hireable** |
| **Seller motivation** | **Scored ≥ 60 (see §2)** |
| **Competition** | **Winnability ≥ 50 (see §2)** |

Sectors: pool service, commercial cleaning, HVAC service (service-heavy, not
new-construction), pest control, landscaping maintenance contracts, fire & life
safety inspection, backflow testing, hood/kitchen exhaust cleaning, grease trap,
document destruction, medical equipment servicing, parking lot maintenance,
commercial compliance and inspection services, niche B2B route businesses.

The common shape: **recurring, mandated, unglamorous, route-based, and sold to
businesses rather than consumers.** Compliance-mandated services are the best of
these — the customer does not choose whether to buy, only from whom.

### BUY BOX B — "Turnaround" (target: ~20%, opportunistic)

Genuinely distressed. Different math, different sources, different structures.

| Criterion | Range |
|---|---|
| EBITDA | May be negative |
| Price basis | 0.3 – 0.8× tangible asset value, or a multiple of *normalized* EBITDA after removing the identified cause of distress |
| Required | Identifiable, single, fixable cause of distress |
| Required | Asset coverage or a customer base with demonstrable value |
| Excluded | Distress caused by market decline, litigation, or regulatory change |
| Structure | Asset purchase only. Never stock. Never assume liabilities. |
| Sources | Lender workout desks, UCC Article 9 dispositions, bankruptcy dockets, MCA-stacked operators, expired listings |

**Critical rule for Box B:** the distress must be *operational* (owner checked
out, lost a key employee, botched a software migration, over-levered on an MCA)
and never *structural* (the industry is dying, the customers are leaving, there
is a lawsuit). Operational distress is fixable by an operator. Structural
distress is a trap that looks identical in a spreadsheet.

A deal is scored against **one** buy box. The UI must always show which.

---

## 2. SCORING — FOUR SCORES, NOT ONE

v1's single 0–100 AcquireScore blends things that must not be blended. A
business can be excellent and unwinnable. Collapsing that into one number
destroys the signal that decides where we spend our time.

Replace with four independent scores, each 0–100, each independently explainable.

### 2.1 QUALITY (0–100) — is this a good business?

Deterministic. Computed from financials only. No LLM involvement in the number.

| Component | Weight | Inputs |
|---|---|---|
| Margin & cash conversion | 25 | Gross margin, EBITDA margin, EBITDA→cash conversion, AR days |
| Revenue durability | 25 | % contracted, churn, avg customer tenure, contract renewal terms |
| Revenue trend | 20 | 3-yr CAGR, trailing-12 vs prior-12, monthly variance |
| Customer diversification | 15 | Top-1 %, top-5 %, customer count, HHI |
| Owner independence | 15 | Owner hours, GM present, owner's share of sales, documented SOPs |

### 2.2 MOTIVATION (0–100) — how badly does the seller need out?

**This is the score v1 is missing and it is the most important one.**

LLM-assisted extraction from listing text, broker calls, and public records;
every contributing signal is stored as a discrete, evidenced row.

| Signal | Weight | Source |
|---|---|---|
| Days on market | 20 | Listing date vs today; > 180 days is strong |
| Price reductions | 20 | Count and cumulative % cut |
| Stated reason (retirement, health, divorce, partner split, relocation, burnout) | 15 | Listing text, broker conversation |
| Business tenure vs no successor | 15 | Entity registration age, officer continuity, no family in payroll |
| Prior failed listing | 10 | Relisted, expired listing agreement, changed brokers |
| Financial pressure signals | 10 | Recent UCC filings, MCA lenders on file, tax liens, judgments |
| Explicit openness to seller financing | 10 | Listing field or broker statement |

**Compliance guardrail (carried forward from v1 and expanded):** never model,
store, or infer owner *age*, health status, family status, or any protected
characteristic as a scoring input. Use **business tenure**, **license issue
date**, and **entity registration age** — these are public, non-protected,
directly relevant, and are better predictors anyway. Where a seller volunteers a
personal reason, store it verbatim as a quoted, attributed note; do not derive a
demographic inference from it. Encode this as a lint rule over the scoring
inputs, not just a comment.

### 2.3 WINNABILITY (0–100) — can we actually get it, on our terms?

Also missing from v1. High quality and high winnability are usually inversely
correlated, and that tension is the whole game.

| Signal | Weight | Direction |
|---|---|---|
| Time on market | 25 | Longer = more winnable |
| SBA-prequalified | 20 | Prequalified = **less** winnable (invites all-cash competition) |
| Broker sophistication | 15 | Top-tier M&A broker = less winnable; FSBO or generalist = more |
| Off-market / no listing | 20 | Never listed = most winnable |
| Price vs our fair value | 10 | Overpriced = fewer competing buyers, more room to trade terms |
| Complexity that scares buyers | 10 | Licensing hurdles, ugly books, weird lease — we can solve these, most buyers can't |

That last row is deliberate. **We should be systematically attracted to deals
that are hard for others for reasons that are cheap for us.** Messy QuickBooks
is a discount we can capture with two weeks of work. A licensing qualifier
requirement is a discount we can capture with one hire. Encode these as
`solvable_friction` items with an estimated cost-to-solve, and let them *raise*
winnability while lowering the price we offer.

### 2.4 FIT (0–100) — is this a business where *we* have an unfair advantage?

Do we have an operating playbook for this vertical? Have we closed one before?
Do we have a manager who could run it? Is it within 90 minutes of an existing
portfolio company (shared dispatch, shared back office, tuck-in)?

Starts as a manual multiplier and becomes learned from outcomes over time (§10).
Deal #2 in a vertical is worth far more than deal #1 in a new one, and nothing
in v1 expresses that.

### 2.5 Composition and explainability

Do **not** average the four into a headline number. Show them as four bars, and
route deals by rule:

- Quality ≥ 70 AND Motivation ≥ 60 AND Winnability ≥ 50 → **PURSUE**
- Quality ≥ 70, Winnability < 40 → **WATCH** (revisit at day 120, 180, 240 —
  the deal that was unwinnable in March is winnable in October)
- Quality < 50 → **PASS** regardless of anything else
- Motivation ≥ 85 with Quality 50–70 → **STRUCTURE PLAY** (price is negotiable
  enough that a bad multiple can be fixed with terms)

Every score stores: `weights_version`, the raw input values at scoring time, the
per-component contribution, and the provenance of each input (§9.2). Clicking
any component shows the arithmetic and the source document page. No black boxes,
and — equally important — no score that cannot be *re-derived* six months later
when we are arguing about whether the model works.

---

## 3. SOURCING — OFF-MARKET IS THE PRODUCT

v1 puts the four big listing portals first and off-market in §20. Invert this.

Listing portals are a commodity feed of the most contested inventory in the
market. Use them, but understand what they are: a source of **comps and market
multiples**, and occasionally an aged listing everyone else has already passed on.

### 3.1 Tier 1 — Off-market, public-record derived (build first)

Legally clean, structured, free or cheap, and almost nobody does it well.

| Source | What it gives us |
|---|---|
| **FL Division of Corporations (Sunbiz) bulk data** | Entity age, officers, registered agent, status, annual-report continuity. Free bulk download. 15–30 year old entity + individual officer + no successor officers added = owner-operator approaching exit. |
| **FL DBPR license data** | Pest control (Ch. 482), contractors/HVAC (Ch. 489), fire equipment dealers. Defines the licensed universe and gives license issue date as an operator-tenure proxy. |
| **FL Secured Transaction Registry (UCC-1)** | **The best single distress and capacity signal available.** Who holds equipment liens, when filed, when lapsing. Multiple recent filings or merchant-cash-advance filers = an operator under pressure and highly motivated. A lapsed UCC = debt-free equipment = better collateral for our acquisition loan. |
| **County tax liens, judgments, lis pendens** | Direct financial-pressure signals. |
| **County/municipal business tax receipts** | Cross-reference for operating businesses not otherwise indexed. |
| **FMCSA / DOT** | Fleet size for any route business — an excellent revenue proxy. |
| **Google Places / review data** | Review count and velocity as a demand proxy; last-review recency as a "still operating" check; website quality as an under-digitization signal. |

Cross-referencing these is the moat. "Pest control license issued 1997, entity
registered 1996, same officer since inception, 6 trucks on DOT, 180 Google
reviews, no website SSL, one UCC lapsing next year, no successor officer ever
added" is a better acquisition target than anything on BizBuySell, and no
competing buyer has assembled that view.

### 3.2 Tier 2 — Broker relationship channel

**Email alert ingestion, not scraping.** Create a dedicated inbox, subscribe to
every broker alert list in the target geography, and parse inbound mail into
normalized deals. This is legally clean, avoids the entire terms-of-service and
robots question, and is genuinely *faster* than scraping — new listings hit
email before they are well-indexed.

Also ingest: broker newsletters, individual broker sites where terms permit,
and manual entry from calls.

Track brokers as first-class entities with a **relationship score**: deals sent
to us, deals we pursued, our response time, deals closed. Brokers send their
best inventory to buyers who close and who do not waste their time. Being the
fastest, most decisive responder in a broker's inbox is worth more than any
scraping pipeline. The CRM should surface "brokers we've gone quiet on."

### 3.3 Tier 3 — Distress channel (Buy Box B)

Lender workout and special-assets desks at regional FL banks and credit unions;
UCC Article 9 disposition notices; bankruptcy dockets (PACER); equipment lessors
with repossessed assets; MCA-stacked operators identified via §3.1 UCC data.

These require relationships more than software, but the software should
**identify and queue the targets** and track the relationship.

### 3.4 Scraping policy (binding)

Respect `robots.txt` and site terms. Do not build portal scraping into the
product. Where a source's terms forbid automated access, the connector must be
email-ingest or manual-entry only. Every `DealSourceAdapter` declares a
`legal_basis` field (`public_record` | `email_consented` | `manual` |
`licensed_api` | `permitted_crawl`) and the ingestion pipeline refuses to run an
adapter that has not declared one. This is a hard gate, not documentation.

---

## 4. THE 90-SECOND KILL — TRIAGE BEFORE ANALYSIS

v1 analyzes everything deeply. Our scarcest resource is attention, and secondarily
inference spend. Most deals should die before either is committed.

Run a **deterministic gate** before any LLM call. Any single failure = auto-pass,
logged with the reason, no model invocation:

1. **Licensing not transferable** and no qualifier available → dead. In FL this
   kills more deals than bad financials and belongs at the *top* of the funnel,
   not in diligence. You cannot own what you cannot legally operate.
2. **Customer concentration > 30%** → dead (Box A).
3. **Owner is the primary salesperson** with no sales team → dead. You are
   buying a job and the revenue leaves with the owner.
4. **Revenue declined in both of the last two years** → dead unless Box B.
5. **DSCR < 1.15 at asking price** under our standard financing template → dead
   at that price. Auto-generate the price at which DSCR = 1.35 and re-rank the
   deal at *that* number. Often the deal is fine and the ask is fantasy — the
   system should say so rather than discarding it.
6. **No usable financials and broker won't provide** after two asks → dead.

### 4.1 Inference cost cascade

Do not run a frontier model over every listing. Three stages:

- **Stage 0 — deterministic** (free): the gate above, plus arithmetic scoring on
  any deal with structured financials.
- **Stage 1 — small/fast model** (cheap): parse unstructured listing text into
  the normalized schema, extract motivation signals, classify industry. Runs on
  everything that survives Stage 0.
- **Stage 2 — frontier model** (expensive): full analysis, AI upside modeling,
  deal memo. Runs **only** on deals that clear the routing rules in §2.5 —
  realistically the top 5–10% of flow.

Budget and log token spend per deal. Surface cost-per-qualified-deal on the
dashboard. If we are spending $40 of inference to find a deal we then pass on,
the funnel is misconfigured and we should be able to see it.

---

## 5. THE VALUATION FIREWALL

**The most important architectural constraint in this system.**

Two numbers exist. They must never touch.

```
ENTRY VALUE   = trailing normalized EBITDA × market multiple for the sector
                ± asset and working capital adjustments

                This is what we pay. It is computed ONLY from historical,
                document-verified financials. The AI upside model has no
                input to this number, by construction.

OWNED VALUE   = post-improvement EBITDA × exit multiple

                This is our return. It exists to decide whether to pursue,
                and never to decide what to offer.
```

Enforcement, and it must be actual enforcement, not a note in a README:

- `entry_value` is computed by `lib/valuation/entry.ts`, which imports **nothing**
  from `lib/ai-upside/`. Add a dependency-cruiser or ESLint boundary rule to CI
  that fails the build on violation.
- The offer engine (§7) takes `entry_value` as its only valuation input. Its
  function signature must not accept an upside parameter.
- In the UI, `owned_value` is never displayed on the same screen as the offer
  recommendation. Different tab. This is a debiasing measure, and it is
  deliberate: anchoring is not defeated by knowing about anchoring.

### 5.1 Comparable multiples

Store observed sector multiples with real provenance: source, date, deal size
band, geography, sample size. A multiple with n=2 must render visibly differently
from one with n=40. Seed from published broker data and industry reports; append
every deal we see, including ones we lose — **especially** ones we lose, and at
what number they cleared. Our own lost-deal data becomes the best comp set we
have within about 18 months.

### 5.2 Output

```
Asking                    $700,000    (4.7× SDE — above market)
Normalized EBITDA         $190,000    (from 2023–2025 returns, 8 add-backs approved, 3 rejected)
Sector multiple           3.0× – 3.8× (n=23, FL service, $500k–$1.5M, trailing 24mo)
ENTRY VALUE               $570,000 – $722,000
Opening offer             $550,000
Walk-away (cash)          $640,000
Walk-away (with 60% seller carry @ 6%, 5yr)   $710,000
```

That last line is the point of the whole exercise. **Our walk-away price is a
function of the structure, not a single number.** We can pay more nominal dollars
for better terms — and the system should compute exactly how much more, and show
the present value of each so we know whether we are actually paying more or just
appearing to.

---

## 6. AI UPSIDE — WITH REALITY CLAMPS

Keep v1's category taxonomy. It is good. Add the constraints that make it honest.

### 6.1 The scale problem

v1's worked example: two admin staff costing $90,000, reduced to one plus AI at
$52,000, saving $38,000. That describes a business with a real back office. A
$1.1M-revenue pool route has roughly 1.5 administrative heads total, one of whom
is the owner's spouse working part-time and unpaid.

**Hard clamps, enforced in code:**

1. **No savings without a line item.** Every projected saving must reference a
   specific, extracted P&L line with a dollar amount. No line, no saving. This
   alone eliminates most of the fantasy.
2. **Cap at 60% of the addressable line.** You cannot automate away 90% of a
   cost category that includes a human who also fixes pumps.
3. **Headcount floor.** Cannot model below 1 admin FTE for any business over
   $500k revenue. Cannot model any reduction in field/technician labor without an
   explicit route-density justification.
4. **Revenue lift requires a measured baseline.** "Missed-call recovery worth
   $27,000" requires an actual missed-call count (from phone records, obtained in
   diligence) × measured close rate × actual average ticket. Absent measured
   inputs, the opportunity is created with `confidence = speculative` and
   contributes **$0** to any headline figure. It stays visible as a hypothesis to
   test in diligence — it just cannot be counted.
5. **Implementation cost is never zero.** Every opportunity carries our internal
   build cost, ongoing software cost, and — the one everyone omits — **management
   attention in operator-hours.** Ten opportunities at 5 hours a week each do not
   fit in one week.
6. **Ramp, not step.** Savings phase in over the implementation timeline with a
   realistic adoption curve. A saving that begins in month 9 is worth
   substantially less in year one than the annualized figure, and the model must
   reflect that.

### 6.2 Three scenarios, and only one of them counts

- **Conservative** — measured inputs only, `confidence ≥ high`, 60% haircut. **This
  is the only scenario permitted to inform any decision.**
- **Base** — `confidence ≥ medium`, 30% haircut. For planning the 90-day plan.
- **Aggressive** — everything. For internal ambition only. Watermarked in the UI.

Every scenario renders with its assumption count and the share of value that is
measured versus estimated. "72% of this upside rests on unmeasured assumptions"
is the most useful sentence the system can print.

### 6.3 Where AI actually moves the number in these businesses

Be specific rather than generic, because the generic version produces generic
fantasy. In a $1M route-service business the real levers, ranked by reliability:

1. **Missed-call capture.** These businesses miss 25–40% of inbound calls. This
   is the most reliable, most measurable, fastest-payback AI intervention that
   exists in this sector, and it is a revenue lever, not a cost lever.
2. **Collections and AR.** 60–90 day AR is standard and often just neglect.
   Automated follow-up is nearly pure working-capital release, which matters
   enormously when we are debt-financed.
3. **Price realization.** Most of these businesses have not raised prices in
   3–5 years and are under-priced relative to their own market. A structured
   annual increase is the highest-EBITDA-per-effort action available and requires
   no AI at all — but the system should identify and quantify it, because it
   funds the debt service in year one.
4. **Scheduling and route density.** Real but bounded; needs route data.
5. **Review generation → local SEO → inbound lead volume.** Slow, compounding, real.
6. **Back-office automation.** Genuinely the *smallest* lever at this scale
   despite being the most talked-about. There simply is not enough admin cost in
   a 12-person company to matter.

Note that levers 2 and 3 are not AI at all. Say so. The credibility of this
module depends on it not claiming credit for basic management.

### 6.4 AI-adjusted EBITDA

Keep v1 §10's arithmetic. Add: display it **only** on the AI Upside tab, never in
the deal header, and never within two clicks of the offer engine. Label it
"modeled, unverified" until §10's realized-tracking has actuals to compare
against.

---

## 7. CREATIVE STRUCTURE ENGINE

v1 lists eight capital sources. The genuinely creative structures — the ones that
answer "without using our own money" — are mostly absent. Ship this library.

### 7.1 Structure library

Each is a parameterized template with its own constraint set, required
disclosures, and generated term sheet.

**S1 — Full seller carry.** 100% seller-financed, secured by business assets,
personal guarantee, 5–10yr amortization. Works with retiring sellers with no debt
and no urgency for a lump sum. Zero bank, zero equity, fastest close. The single
best structure for our thesis. Requires very high Motivation.

**S2 — SBA 7(a) + standby seller note.** The workhorse. Encode current SOP rules
as **versioned, citable, editable** parameters, never hardcoded constants: minimum
equity injection for a complete change of ownership; the conditions under which a
seller note counts toward that injection (standby period and terms); restrictions
on the seller's post-close role; personal guarantee thresholds. **SBA rules change
materially between SOP revisions.** Store `sop_version`, `effective_date`, and a
citation on every rule, warn when a modeled deal used a superseded version, and
require lender confirmation before any offer relies on a rule. Treat every SBA
number in this system as a lender-confirmable input, not a fact.

**S3 — Seller carry + asset-based lender.** Skip SBA entirely. Equipment and AR
collateralized with a regional lender or specialty ABL. Faster, no SBA paperwork,
higher rate. Excellent for Box B.

**S4 — Management agreement with purchase option.** *The most underused structure
in small-business M&A and the best fit for our stated goal.* We manage the
business for 12–24 months for a management fee, with an option to purchase struck
at today's valuation. Zero capital at risk. We see the books from the inside
before committing. If it is worse than represented, we walk. If our AI thesis
works, we exercise at the old price and capture 100% of the improvement. Requires
a genuinely motivated, tired seller — which is exactly what §2.2 finds. Note
honestly: this creates operational obligations before ownership, and a seller can
attempt to unwind it if we succeed too visibly. Option must be recorded and
specifically enforceable.

**S5 — Revenue-share / self-liquidating earnout.** Price paid as a fixed % of
collections over N years, with a cap and a floor. Automatically downside-protected
— if revenue falls, we pay less. Sellers accept this when they genuinely believe
in their business, and their belief is the risk transfer. Watch imputed interest
(§1274 AFR) and the tax treatment for both sides.

**S6 — Seller retains real estate + long-term lease.** Where property is involved,
carving it out cuts the purchase price dramatically and gives the seller ongoing
income they often prefer to a lump sum. Model the lease as a permanent EBITDA
reduction with escalators, and negotiate a purchase option on the property. Very
common, very effective with retirees, and it converts a deal we cannot finance
into one we can.

**S7 — Key-employee rollover.** The GM or lead technician takes 10–25% equity for
staying 3–5 years, reducing our cash requirement and — more importantly — solving
the operator problem that is the actual binding constraint on a holdco. Vesting,
drag-along, and a valuation formula for their eventual buyout.

**S8 — Consulting / non-compete allocation.** Part of the price paid as a
post-close consulting agreement and non-compete. Different tax treatment for both
parties, moves cash out of closing and into operating expense. Purchase price
allocation is negotiable and is real money to both sides. Must be economically
genuine — the seller has to actually consult — or it is a sham allocation.

**S9 — Assumption + assignment.** Assume existing equipment financing rather than
paying it off. Reduces cash needed at close; requires lender consent and clean
assignment language.

**S10 — Working capital arbitrage.** Businesses with AR and cash on the balance
sheet where the working capital delivered at close, plus a factoring or AR line
established on day one, funds part of the down payment. Model AR quality
carefully — 90+ day AR in a service business is often uncollectible and sellers
know it.

**S11 — Tuck-in / roll-up.** Acquire target #2 using the cash flow, borrowing
base, and back office of portfolio company #1. **This is how founder capital
actually reaches zero by deal three, and v1 treats every deal as standalone.**
The structure engine must be able to model a deal against consolidated holdco
capacity, not just the target's standalone financials. Encode shared-overhead
synergy — one dispatcher across three route businesses is real, unlike most
claimed synergies.

**S12 — Article 9 / lender-workout asset purchase.** For Box B. Purchase assets
from a secured lender following foreclosure, or through a consensual disposition.
Liabilities stay behind. Requires counsel every single time; encode a mandatory
legal-review gate that blocks term-sheet generation without it.

### 7.2 What the optimizer must actually output

v1's example ends with "Founder equity: $0" as the headline. That is the
misleading half of the truth, and internalizing it is how people end up
personally bankrupt while believing they used none of their own money.

Every structure must report **all four** of these together, with equal visual
weight:

```
Founder cash at close        $0
Founder personal guarantee   $487,000     ← THE REAL EXPOSURE
Founder ownership            62%
Investor preferred return    8% cumulative, 1.4× minimum multiple
Post-debt cash flow (yr 1)   $71,400
DSCR (base)                  1.48×
DSCR (conservative: -15% rev) 1.09×      ← BREACHES 1.25 COVENANT
Months of cash reserve       2.4          ← THIN
Break-even revenue decline   -19%
```

**"No money down" is not the same as "no risk."** An SBA loan with a personal
guarantee and a lien on your house is more personal risk than writing a $100k
check. The system must make that trade explicit on every scenario, every time,
or it is a machine for generating confident mistakes.

Required outputs per scenario: cash at close, founder cash, **founder PG
exposure**, **investor waterfall and preferred return** (not just ownership %),
monthly and annual debt service, DSCR at base and stressed, **stressed DSCR at
-15% and -25% revenue**, cash flow after debt and after distributions, months of
operating reserve, break-even revenue decline, seller net proceeds (§8), and
investor IRR/MOIC.

### 7.3 Covenant and stress modeling

Real acquisition loans carry DSCR covenants, distribution restrictions, and
reporting requirements. Model them. A deal that clears 1.35× base DSCR but
breaches at -12% revenue in a seasonal business is not financeable and the system
should say so loudly, before we spend three months on it.

Every structure runs a mandatory stress panel: revenue -15%, revenue -25%, loss
of largest customer, +200bp rate on any floating debt, and a 60-day AR slowdown.

---

## 8. SELLER NET PROCEEDS ENGINE

**The highest-leverage feature in this document that exists in no competing tool.**

We win on terms. To win on terms we must understand the seller's after-tax
position better than they do — most sellers of $1M businesses have never modeled
theirs, and their broker has modeled only gross price because that is what the
commission is based on.

Compute and present, for any structure we propose:

```
Gross price                              $700,000
Less broker commission (10%)             ($70,000)
Less transaction costs                    ($18,000)
Less debt payoff                          ($95,000)
Gross proceeds                           $517,000

Purchase price allocation:
  Goodwill (capital gain)                 $480,000
  Equipment (ordinary recapture)          $180,000
  Consulting agreement (ordinary income)   $40,000

Estimated federal tax                    ($121,000)
State tax (FL: none on individuals)             $0
NET TO SELLER                            $396,000
```

Then the comparison that wins deals:

```
              ALL CASH $700k      OUR OFFER $760k, 55% CARRIED @ 6%/7yr
Net year 1        $396,000                     $148,000
Total net         $396,000                     $441,000  (installment sale, §453)
Deferral benefit         —                     Gain recognized over 7 years,
                                               likely across lower brackets
Our cash at close $700,000                     $342,000
```

**We paid $60,000 more nominal and $358,000 less cash, and the seller nets
$45,000 more after tax.** That is not a trick — it is a genuine efficiency
created by tax deferral under the installment method, and both sides are better
off. It is the entire reason creative structuring works, and it is completely
absent from v1.

**Mandatory disclaimers, rendered prominently, no exceptions:** estimates only,
based on stated assumptions, not tax advice, seller must consult their own CPA.
Include an assumption panel showing every input (filing status assumption,
bracket assumption, basis assumption, state of residence). Never present a
seller-facing number without it. Basis in particular is usually unknown to us and
dominates the result — flag it as an input we must ask for rather than assume.

---

## 9. TECHNICAL

### 9.1 Stack — simplified

v1 hedges (NestJS "if cleaner", Redis + BullMQ, S3, pgvector, Clerk or Auth0).
For a small internal team, complexity is the enemy and every service is a thing
that breaks at 2am.

- **Next.js (App Router) + TypeScript + Tailwind + shadcn/ui + Recharts**
- **PostgreSQL + Prisma.** Single database.
- **One worker process** (`pg-boss` on the same Postgres, or BullMQ + Redis only
  when queue depth actually justifies a second datastore). Do not run Redis on
  day one.
- **Auth: Clerk.** Pick one and move on. Enforce MFA.
- **Storage: S3 or R2**, signed URLs only, short TTL, every access logged.
- **Sentry.** **Vercel + Neon/Supabase.** No Kubernetes, no microservices.
- **pgvector** only when semantic search over documents is actually needed —
  Postgres full-text handles the first year.

### 9.2 Provenance — non-negotiable

Every financial number in the system carries provenance. This is the difference
between a decision-support tool and a very expensive random number generator.

```ts
type Provenance =
  | { kind: 'document';   documentId: string; page: number; bbox?: Rect; extractedAt: Date }
  | { kind: 'user';       userId: string; enteredAt: Date; note?: string }
  | { kind: 'computed';   formula: string; inputs: ValueRef[] }
  | { kind: 'llm';        model: string; promptVersion: string;
                          inputRefs: string[]; confidence: number; generatedAt: Date }
  | { kind: 'assumption'; basis: string; setBy: string; reviewedAt: Date | null };

type Money = { cents: bigint; currency: 'USD'; provenance: Provenance };
```

Rules:

- **Money is integer cents.** Never a float. `Decimal` in Prisma. A rounding
  error in a DSCR calculation is a real mistake with real consequences.
- **LLM-derived values render visually distinct** from document-derived values —
  everywhere, without exception. A different color and an icon. The moment a
  hallucinated revenue figure is visually indistinguishable from a tax-return
  figure, this system becomes actively dangerous.
- **No LLM-derived number may enter a financial calculation without human
  approval.** Extraction proposes; a human confirms; only then does it compute.
- **Every calculated output can enumerate its input chain** to source documents.
  Build `explain(valueId)` returning the full tree. The deal memo cites it.

### 9.3 Add-back discipline

v1 §16 is right and should be strengthened. Add-backs are where small-business
M&A fraud lives, and where our own optimism does the most damage.

Each proposed add-back: amount, category, reason, **confidence**, source document
and page, **and a classification**:

- `verified` — supported by a document we have examined (a paid invoice, a
  cancelled check, a K-1)
- `plausible` — consistent with the story but unverified
- `rejected` — we do not believe it
- `seller_claimed` — asserted with no support whatsoever

**Only `verified` add-backs enter normalized EBITDA. Full stop.** Show the others
in a separate "seller's number vs our number" reconciliation — that gap is itself
a negotiating asset and often the most useful single page in the diligence file.

A seller claiming $85,000 of add-backs of which $31,000 is verified has told us
something important about both the business and the seller.

### 9.4 Scoring versioning

Store `weights_version` and a full input snapshot on every score. When weights
change, do not retroactively rewrite history — recompute into a new row. We need
to be able to ask "would our March model have flagged this deal?" and get a true
answer, or §10 is impossible.

---

## 10. THE FEEDBACK LOOP — DESIGN IT PROPERLY

v1 §37 correctly identifies this as the long-term asset, then does not specify it.
A feedback loop that is not designed into the data model on day one cannot be
retrofitted, because the data was never captured.

Capture from deal one:

**Every offer we make**, with full terms, and the outcome: accepted, rejected,
countered (at what), or ignored. Within a year this tells us our real winning
price by sector, seller type, and structure — which is worth more than any upside
model. Right now we are guessing; this is how we stop.

**Every deal we lose**, and to whom, at what price, with what structure. Feeds
§5.1 comps and calibrates Winnability with actual outcomes rather than our priors.

**Every deal we pass**, with the reason, plus a scheduled 12-month lookback: what
happened to it? Did it sell? For how much? Is it still operating? We are wrong
sometimes and this is the only way to find out which direction we are wrong in.

**Predicted vs realized**, per opportunity, per portfolio company, monthly:

```
AI Receptionist — Tampa Pool Co
  Predicted annual EBITDA impact    +$65,000
  Realized (month 14, annualized)   +$31,200
  Variance                             -52%
  Root cause: missed-call volume was 60% of estimate;
              close rate on recovered calls 22% vs 40% assumed
```

After ten of these, our conservative multiplier stops being a guess. **That
calibration is the actual asset** — not the deal flow, not the scoring model. Any
competent buyer can find businesses. Almost nobody knows, with evidence, what
their own operational improvements are actually worth. Design the schema so this
is queryable from the first portfolio company.

---

## 11. COMPLIANCE AND GUARDRAILS

Keep all of v1 §29. Add:

- **Outreach.** Cold SMS to sellers is governed by TCPA federally and by an
  unusually strict Florida statute. Do not build SMS outreach without counsel
  reviewing the specific flow. Email outreach must be CAN-SPAM compliant
  (identification, physical address, functioning opt-out). Build suppression
  lists and honor opt-outs at the platform level, not per-campaign.
- **Call recording.** Florida is a two-party (all-party) consent state for
  recording. Any call recording or AI voice feature must obtain and log consent
  from every party before recording begins. Store the consent artifact.
- **AI voice agents** may never contact a seller or broker without explicit
  per-contact human approval, must identify themselves as AI, and may never make
  or accept an offer. Encode as a hard block in the outreach service, not a
  policy document.
- **LOIs** are non-binding except for exclusivity, confidentiality, and
  governing-law provisions. Every generated LOI carries "DRAFT — NON-BINDING —
  SUBJECT TO LEGAL REVIEW" in the document header and footer, and the system
  refuses to export a version without it.
- **We are a principal buyer**, not a broker. Do not build features that
  facilitate transactions between third parties — that is licensed activity in
  most states.
- **Data handling.** Seller financials are received under NDA. Encrypt at rest,
  scope access per deal (not per user role alone), log every document view,
  auto-expire signed URLs in minutes, and support hard deletion on request. An
  NDA breach ends our reputation in a broker network that is smaller than it looks.
- **The scoring compliance lint** from §2.2: CI check that no protected
  characteristic reaches a scoring input.

---

## 12. THE ACTUAL MVP

v1's "MVP" has 18 features including a conversational analyst and a daily
autonomous agent. That is a year of work and it front-loads the parts that only
matter once deal flow exists.

**Ship this in two weeks, then use it on real deals before building anything else.**

### v0.1 — The Judgment Loop

1. Auth (Clerk, MFA on).
2. **Paste-a-listing → normalized deal.** One text box. Paste any listing or CIM
   text; LLM extracts to the normalized schema; human corrects; save. This alone
   is worth the build.
3. Deal list + deal detail.
4. **Quality + Motivation + Winnability scores**, fully explainable.
5. **Normalized EBITDA calculator** with the add-back approval workflow of §9.3.
6. **Entry valuation** with a hand-seeded sector multiple table.
7. **Structure modeler** — S1, S2, S3, S4 only, with the full §7.2 output
   including PG exposure and stressed DSCR.
8. **Seller net proceeds calculator** (§8).
9. Pipeline stages, notes, tasks.

That is it. No document pipeline, no chat, no autonomous agent, no integrations.

**Everything above this line is a decision-support tool for a human buyer. That is
the whole product for the first six months.**

### v0.2 — Volume (once v0.1 has been used on 20+ real deals)

Broker email ingestion. Document upload and extraction. Deal memo generation.
Alerts. CSV import.

### v0.3 — Off-market (the real moat)

Sunbiz + DBPR + UCC ingestion and cross-referencing. Off-market scoring. Outreach
CRM with compliance guardrails.

### v0.4 — Portfolio and loop

Portfolio module. Predicted-vs-realized tracking. 90-day plan execution. Score
recalibration from outcomes.

### v0.5 — Autonomy

Daily agent, AI analyst chat, advanced connectors.

### Build order for v0.1, concretely

1. `lib/money` — integer-cents money type, provenance, formatting. **First.**
   Everything else depends on it and retrofitting it is agony.
2. `lib/finance` — normalization, add-backs, DSCR, amortization, IRR/MOIC, NPV.
   **Unit tested against hand-worked examples before any UI exists.**
3. `lib/valuation` — entry value only. No upside imports. Boundary rule in CI.
4. `lib/structures` — the structure templates, constraint solver, stress panel.
5. `lib/scoring` — deterministic components, versioned weights, explainability.
6. `lib/tax` — seller net proceeds. Assumptions explicit and versioned.
7. Prisma schema + seed with 20 real listings pulled by hand.
8. UI last.

**No financial arithmetic in React components. No exceptions.** Every function in
`lib/finance`, `lib/valuation`, `lib/structures`, and `lib/tax` has unit tests
with hand-verified expected values. A wrong DSCR is not a rendering bug, it is a
$600,000 mistake.

---

## 13. UX

v1 §30 is right: Bloomberg + Linear + deal room. Dense, fast, serious,
desktop-first, keyboard-driven. Add:

**The deal header shows what actually matters:**

```
TAMPA COMMERCIAL POOL SERVICE                          Buy Box A · Day 187 on market

QUALITY 78   MOTIVATION 84   WINNABILITY 71   FIT 62          → PURSUE

Asking $625,000    Entry value $498k–$561k    Our offer $505,000
Normalized EBITDA $187,000 (verified add-backs only; seller claims $214,000)
Best structure: S2 · Founder cash $0 · PG exposure $412,000 · DSCR 1.44× (1.11× stressed)
```

Note what is **absent** from that header: AI-adjusted EBITDA and projected value.
Those live on their own tab, behind a click, by design (§5).

Note what is **present**: the gap between our EBITDA and the seller's, the
stressed DSCR next to the base, and personal guarantee exposure next to the "$0
founder cash." Every one of those is a number that stops a bad decision, and every
one of them was missing from v1's header.

---

## 14. THE PRINCIPLE

v1 §34 says the system should tell us why, how much, at what price, how to
finance, what could go wrong, how to automate, and what it could be worth.

Correct, but incomplete in the two places that decide whether we make money:

> **1. Can we win it — and what is it worth to us specifically, versus to the
> buyer we are competing against?**
>
> **2. What does the seller actually need — and what is the cheapest way for us
> to give them exactly that?**

The best deal is not the highest-scoring business. It is the good business where
the seller wants something we can give cheaply — speed, certainty, tax deferral,
a soft landing for their employees, their name on the truck for two more years —
and where the buyer who would have outbid us never saw the listing.

**Everything in this system should be pointed at finding that.**
