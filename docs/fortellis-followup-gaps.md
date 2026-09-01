# The Recovery Ledger

**Fortellis gap analysis — the four follow-up failures Peter named, and the product that closes all four.**

Published version: https://claude.ai/code/artifact/32f7cab0-1156-43b7-b3cf-1019c36cccad

> Input gap: the two artifacts linked in the originating request could not be read (served as public non-member reader; that read path is not enabled). This analysis is built from Peter's text, the public Fortellis/CDK API surface, and the competitive landscape as of Sept 2026.

---

## 1. The reframe

Peter's four pain points, stripped of department names:

| Department | Stated pain |
|---|---|
| Service | Declined ROs and the lack of consistent follow-up afterward |
| Parts | Lack of follow-up when a customer's part arrives and is ready for pickup and payment |
| F&I | Following up with customers who did not purchase F&I products at the time of sale |
| Business office | Payments not posted on time, AR not collected quickly enough |

Each is the same sentence: **a dollar amount is sitting in a DMS field, attached to a named customer, aging, with no owner and no clock.**

- A declined ASR is a receivable the dealership never invoiced.
- An unclaimed special-order part is a receivable sitting on a shelf.
- An F&I no-buy is a receivable with an expiry date.
- An aged schedule line is a receivable everyone already agrees is a receivable.

**The product is not declined-RO follow-up software.** It is a *recovery ledger*: one queue where every open obligation across service, parts, F&I and the business office becomes a row with a value, an age, an owner, a next action and an outcome. One number on the GM's screen: dollars sitting in open loops, and dollars recovered this month.

---

## 2. The four gaps: pain → data → API → dollars

Competitive heat is the key variable. Dollar figures are modelled on a single rooftop at ~1,000 ROs and ~100 units/month — replace with Peter's actuals.

### Service — declined repair orders (CROWDED)
- **Breaks:** ASR recorded at decline, then dies. Advisors paid on today's RO, not next quarter's.
- **Data:** Additional Service Requests on closed ROs, op codes, hours, parts already priced.
- **Fortellis:** `Repair Order V2 bundle` (full RO lifecycle incl. ASR creation/approval), `CDKDrive OpCodes`.
- **API confidence:** HIGH — best-documented surface on the platform.
- **Incumbents:** Xtime (Inspect / declined-service recapture), UpdatePromise. Often already bundled.
- **Modelled:** $9k–17k GP/rooftop/mo at 8–12% recapture on a $120k–180k monthly declined pool.

### Parts — special orders that arrive and sit (OPEN)
- **Breaks:** Money already spent. Part lands, nobody calls, 90 days later it's obsolescence write-off plus a lost customer.
- **Data:** Special-order parts tagged to customer/RO, bin location, arrival date, no pickup event.
- **Fortellis:** `Parts Management`, `Search Parts Pick Ticket`, `Async Parts Inventory`. A first-class "special order arrived for named customer" event is **not** publicly confirmed.
- **API confidence:** MEDIUM-LOW — biggest unknown in the plan. Verify week one.
- **Incumbents:** Effectively none found. Cleanest air of the four.
- **Modelled:** $1k–2k/rooftop/mo avoided obsolescence, plus working capital and the follow-on service visit.

### F&I — post-delivery second chance (CONTESTED)
- **Breaks:** Customer declined at 9pm on delivery day. Nobody re-approaches inside the eligibility window.
- **Data:** Sold deals where product penetration is below the eligible set, inside VSC/GAP windows by miles and days.
- **Fortellis:** `CDK F&I APIs` (vehicle sale records with products sold), joined to `Customer` and service-history mileage.
- **API confidence:** HIGH for data, LOW for the compliance wrapper.
- **Incumbents:** Impel F&I Pursuit, Darwin, servicecontract.com. Reported ~$2.4bn post-sale VSC volume — real category, thin coverage.
- **Modelled:** $2k–3.5k/rooftop/mo at 4–7% close on ~45 monthly no-buys, ~$1,100 PVR.

### Business office — unposted payments and aged schedules (OPEN)
- **Breaks:** Contracts in transit, factory receivables, we-owes, customer-pay balances pile up on schedules nobody works daily. An accountability vacuum, not a systems failure.
- **Data:** Schedule lines by age bucket, unapplied cash, open balances against closed ROs and deals.
- **Fortellis:** `Payment Settling API` (retrieves exact amount owed), `Data Extract API bundle` (accounting/GL).
- **API confidence:** MEDIUM. Line-level schedule access needs verification; nightly extract is a viable fallback.
- **Incumbents:** AP automation is well covered (CloudX et al). AR/schedules/aging is largely manual.
- **Modelled:** $3k–6k/rooftop/mo equivalent, mostly cash acceleration and avoided 90+ write-off. Highest emotional urgency.

---

## 3. Why this is a company and not a feature

Xtime could ship declined-RO recapture tomorrow — they already have. What stops them eating this:

1. **They have no reason to cross the hallway.** Xtime sells to a service director. Parts obsolescence, F&I penetration and AR aging are three other buyers with three other budgets. Suite vendors expand along their buyer, not across departments.
2. **The ledger is the asset, not the outreach.** Everyone has an AI that sends texts. Almost nobody can tell a GM: here are the 340 obligations in your store, ranked by recoverable dollars, and who dropped each one. The queue is scarce; execution is commodity.
3. **Attribution is the lock-in.** Proving $14,200 of last month's gross came from ledger rows makes you a P&L line, not a software line item. Hard engineering; almost nobody does it properly.
4. **Accountability creates GM-level stickiness.** Once a dealer principal uses it in a Monday manager meeting, a department head can't remove you.

Fortellis is **not** on that list. It is a channel, not a moat.

---

## 4. Five assumptions to push back on

1. **"We have Fortellis, so we can fill the gap."** Fortellis is a public marketplace — anyone can register, certify and consume the same APIs. Certification fees and timeline are a cost you carry, not a wall you hide behind.
2. **Leading with declined ROs.** Biggest pool, worst wedge. Xtime and UpdatePromise are entrenched and possibly already paid for. Lead with the business office: the pain he called *killing me*, no incumbent, unambiguous dollars, provable in 30 days.
3. **Peter's pain equals a market.** n=1. He may also be describing a management problem in software language — "payments not posted on time" may be two vacant clerk roles. Get five dealers naming the same four unprompted before committing past the pilot.
4. **Building four modules.** Build **one engine and four detectors**. If the obligation model is right, the fourth detector is two weeks. If you build four products, it's another six months.
5. **Starting company number eight.** Ship this inside CarConnective — existing dealer brand, relationships and positioning. Only spin out if positioning actively conflicts.

---

## 5. Architecture — one engine, four detectors

```
Obligation
  id                uuid
  group_id          dealer group — the unit of sale
  store_id          rooftop
  type              declined_asr | parts_arrival | fi_no_buy | ar_balance
  source_ref        RO#, pick ticket, deal jacket, schedule line
  customer_ref      DMS customer id + consent state
  vehicle_ref       VIN, mileage, in-service date
  amount_cents      the number that makes this worth working
  opened_at         when the obligation came into existence
  aged_days         derived — drives the bucket
  expires_at        F&I eligibility, parts obsolescence, statute
  recoverability    0–100 score
  state             open | queued | worked | recovered | written_off
  owner_user_id     a human name, always
  next_action_at    the clock nobody currently sets
  attempts[]        channel, timestamp, result, operator
  outcome_ref       the RO / deal / payment that closed it
  recovered_cents   the number you put in front of the GM
```

- **Detectors** are pure functions over DMS reads; each emits Obligations and nothing else.
- **Scoring** ranks by amount × age-decay × contactability × customer value.
- **Work queue** is the product surface.
- **Attribution job** runs nightly, matching new ROs, deals and payments back to open obligations. This turns a tool into a P&L line — staff it first, not last.

### The decision that de-risks everything

**v1 contacts no customers.** It tells the dealership's own staff exactly who to contact, in what order, with the dollar value next to each name, and records what happened. Removes the entire TCPA/consent surface from the critical path, ships months faster, and still delivers what Peter lacks: a list and an owner. Automated outbound is the v2 upsell, gated behind a consent ledger, quiet hours and DMS opt-out honouring.

### Stack
- **Ingest:** Fortellis OAuth per rooftop; async event subscriptions where available, polling where not. One adapter interface per DMS.
- **Store:** Postgres. Obligations, attempts, attribution, consent. Row-level isolation per group from day one.
- **Jobs:** Durable queue for detectors, scoring, attribution, nightly reconciliation. Every write idempotent on `source_ref`.
- **Surface:** Department queues, group roll-up for the dealer principal, monthly recovered-dollars statement that reads like a schedule.

**Build the DMS adapter interface on day one**, even with only CDK behind it. Fortellis covers CDK Drive and eLead. Reynolds is closed; Tekion, Dealertrack and DealerSocket have their own paths. Detectors talking to a DMS-agnostic interface make Tekion a sprint; detectors talking to Fortellis directly make it a rewrite, and cap TAM at the CDK installed base forever.

---

## 6. Sequencing — thirty weeks, four gates

**Phase 0 · Weeks 0–2 — Prove the dollars exist without building anything**
Register the Fortellis developer account and start CDK certification immediately (long pole). In parallel, get read-only access or exports from Peter and hand-produce one page: *here is $X sitting in your DMS right now, across four departments, by name and by age.*
- Fortellis dev account + app listing submitted
- Sandbox verification of all four API surfaces, especially parts
- The one-page recovery report, built manually if necessary

*Gate:* that page either makes Peter go quiet or it doesn't. Under ~$50k across his group, the thesis is wrong and you stop, having spent two weeks.

**Phase 1 · Weeks 2–10 — Business office (the anchor)**
Obligation model, ingest, scoring, work queue, attribution. One detector: AR balances and aged schedule lines. Internal-only outreach. Ship as a paid pilot.

*Gate:* a controller logs in unprompted five days a week for a month, and you can show recovered dollars. If they don't log in, the queue isn't good enough — fix it before adding detectors.

**Phase 2 · Weeks 10–14 — Parts arrival (the cheap win)**
Second detector on the same engine. Small dollars, highest delight-per-line-of-code, proves the one-engine thesis. First module a competitor cannot answer.

*Gate:* shipped in under five weeks. If it takes twelve, the obligation model is wrong — fix it at two detectors, not four.

**Phase 3 · Weeks 14–22 — Declined ROs (the volume)**
Biggest pool, hardest fight. Enter with two modules of proof and a cross-department story Xtime can't tell. Add automated outbound here, with the consent ledger.

*Gate:* two design partners outside Peter's group signed and paying before this ships.

**Phase 4 · Weeks 22–30 — F&I second chance (the compliance one)**
Heaviest regulatory load, provider eligibility rules per product, touches the deal jacket. Do it with revenue funding a compliance review, not as a founding bet.

---

## 7. The money

### Recovery model — per rooftop, per month

| Gap | Monthly pool at risk | Recapture assumption | GP recovered/mo |
|---|---|---|---|
| Declined ASRs | $120k–180k declined | 8–12% | $9,000–17,000 |
| Special-order parts | $6k–12k unclaimed | 60% claim-rate lift | $1,000–2,000 |
| F&I no-buys | ~45 units | 4–7% @ $1,100 PVR | $2,000–3,500 |
| AR & schedules | $250k+ aged 90+ | 10% of 90+ bucket | $3,000–6,000 |
| **Total** | | | **$15,000–28,500** |

### Pricing

**Price flat, report like revenue share.** Do not take a percentage of recovered dollars — you will spend your life arguing attribution with a controller, and you cap yourself at the ceiling of your own reporting accuracy. Charge flat per rooftop, then show recovered ÷ fee as an ROI multiple on every screen.

| Tier | Includes | Per rooftop/mo | ROI at modelled recovery |
|---|---|---|---|
| Business office | AR & schedules | $499 | 6–12× |
| Fixed ops | Service + parts | $999 | 10–19× |
| Full ledger | All four + group roll-up | $1,799 | 8–16× |
| Group | 10+ rooftops, principal dashboard | Negotiated | — |

Sell to the **group**, not the store — the difference between a $1,800 deal and an $18,000 one for the same sales cycle. Risk-reverse the pilot: 90 days, we show recovered dollars or you don't renew. Affordable because the Phase 0 report already told you the answer.

### ARR path

| Milestone | Rooftops | Blended ARPU | ARR |
|---|---|---|---|
| Peter's group, paid pilot | 5 | $1,500 | $90,000 |
| Year one | 50 | $1,500 | $900,000 |
| Year two | 250 | $1,600 | $4.8M |
| Year three | 1,000 | $1,800 | $21.6M |

The ceiling is the CDK Drive rooftop count until a second DMS adapter exists. **Ask CDK for that number** — it is the literal TAM on this channel.

---

## 8. Risk register

| Risk | Severity | Hedge |
|---|---|---|
| Parts API can't identify a customer's special order at arrival | High | Verify week one. Fallback: pick tickets + inventory receipt deltas, or nightly extract. If truly absent, Phase 2 becomes F&I. |
| CDK certification time and fees | High | Start the clock week zero. Legacy 3PA pricing ran $10k–40k integration + $200+/rooftop/mo; confirm the Fortellis path's cost with CDK directly. |
| Accounting/schedule data not addressable at line level | Medium | Data Extract API bundle as nightly fallback. AR doesn't need real time. |
| TCPA / consent exposure on outbound | Medium | v1 contacts nobody. Consent ledger, quiet hours, DMS opt-out honouring before any automated message. |
| DMS coverage caps TAM to CDK | Medium | DMS adapter interface from day one. Non-negotiable. |
| Xtime bundles the service module free | Medium | Expected. Why service is Phase 3 and why the pitch is the ledger, not the module. |
| Building Peter's wishlist instead of a product | Medium | Two paying design partners outside his group before Phase 3. |
| Founder attention across eight companies | High | Ship inside CarConnective. One brand, one team, one sales motion. |

---

## 9. The call

Don't demo. Don't pitch a product. Extract the numbers that decide whether this is a $90k pilot or a $20M company, then make one specific ask.

**Qualify the channel (first five minutes)**
- Which DMS exactly, and which version? If it isn't CDK Drive, most of this plan changes.
- Are you already on Fortellis? Who is your CDK rep?
- How many rooftops, which brands, one controller or several?

**Get the four numbers**
- *Service:* monthly RO count; pull the declined-services report — total declined dollars last 90 days. Who owns follow-up today? Do you pay for Xtime or UpdatePromise?
- *Parts:* special orders per month; what did you write off to obsolescence last year? How long does a part sit before someone calls?
- *F&I:* units per month, product penetration %, PVR. Any post-delivery process today?
- *Business office:* total schedule balance, the 90+ bucket, days-to-post on payments — and the real question: is this people, process, or system? "I'm two clerks short" is important information.

**The ask — don't leave without all three**
1. **Read-only DMS access** so you can build the recovery report. This is all of Phase 0.
2. **A paid design-partner agreement**, even token. Never ask "would you use this" — ask "would you pay $1,500 a rooftop if I show you $15,000 recovered."
3. **Three intros to peer dealers.** The n=1 problem is solved by Peter's phone, not your marketing.

**Opening line**

> "Peter — those four things you sent me aren't four problems. They're the same problem four times: money the store has already earned or already spent, sitting in the DMS with nobody's name on it and no clock running. I want to build you one screen that shows all of it, ranked by dollars, with an owner on every line."

Then show him the number. Everything else is downstream of whether it is big enough to make him go quiet.

---

*Modelled figures are assumptions for structuring the conversation, not forecasts. API confidence levels reflect public documentation as of Sept 2026 and must be verified in a Fortellis sandbox.*
