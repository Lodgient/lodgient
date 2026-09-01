# The Follow-Up Gap — CarConnective Build Order

**Pilot:** Capitol Nissan · **Channel:** CDK Drive export → CarConnective · **Verdict:** build it · **First gate:** day 14

Published version: https://claude.ai/code/artifact/929aa457-57dc-4e56-bc52-0db59fcf5fd1
Prior strategy doc: https://claude.ai/code/artifact/32f7cab0-1156-43b7-b3cf-1019c36cccad

---

## 1. Verdict — the gap is real, and it's a share-loss problem

Dealer share of service visits is **29%**, down 12% since 2018. General repair shops are now the most preferred service provider for the first time on record. Among owners of cars 0–2 years old, dealer service retention fell from **72% (2023) to 54% (2025)**.

Declined work isn't idle: **60–70% of declined safety/longevity work gets completed within 3–12 months at an independent**. Estimated **$266bn/yr** across franchised retail.

**Positioning:** not "you're leaving money on the table" (noise). The line is *"the work you found is getting done — just not by you."* Competitive loss, not inefficiency.

---

## 2. Evidence

| Headline | Figure | Source |
|---|---|---|
| Dealer share of service visits | 29% (was 35% in 2021) | Cox Automotive Service Industry Study, Nov 2025 |
| 0–2yr owners returning to selling dealer | 54% (was 72% in 2023) | Cox Automotive 2025 |
| ASRs declined at the counter | 58%+ | Fixed-ops benchmarks |
| National fixed absorption | 63.9% | NADA, Aug 2025 |

**Service** — 8,109 ROs per dealership June YTD 2025 (~1,350/mo); $470 service+parts per customer RO; $179 customer labor rate; $4.78M annual service+parts per dealership; $164bn industry on 276M ROs. Disciplined declined tracking → 15–25% capture lift; 20–35% close rate on followed-up declines. 45% of owners dissatisfied — top causes unexpected cost and **poor communication**.

**Parts** — average dealership carries **$50,000–$88,000 obsolete inventory**; carrying cost 20–30%/yr; healthy dead stock <10% (target 5–8%); uncollected special orders are a named trigger; 95% of eventual obsolete value starts as forced stock.

**F&I** — VSC penetration 45% (**55% no-buy**); GAP 39% (61% no-buy); prepaid maintenance 17% (83% no-buy); paint/fabric 20%. PVR record **$1,995** Q4 2025. VSC carries $600–900 PVR, GAP $200–350. Post-sale VSC channel ≈ $2.4bn/yr.

**Office** — healthy CIT funding 4–10 days; paper packages average 5 days; stips/resign push to 11–13 business days. CIT is the largest single receivable. AP automation is mature; **AR/schedules/aging remain manual**.

---

## 3. Where the gap actually is

| Lane | Heat | Who's there |
|---|---|---|
| Service SMS follow-up | **Crowded** | Xtime, UpdatePromise, Kimoby, Text2Drive, BizzyCar, Numa, Impel |
| F&I second chance | **Contested** | Impel F&I Pursuit, Darwin, servicecontract.com |
| Parts arrival & pickup | **Open** | No dedicated vendor found |
| AR & schedule chase | **Open** | Spreadsheets and a controller's memory |
| **One ledger across all four** | **Nobody** | Every incumbent sells to one department head |

**Cost note:** Kimoby publishes a **$209/month CDK integration fee** set by CDK, on top of subscription. If the dealer-owned export path avoids that per-rooftop tax, it's a structural margin advantage — confirm before setting list price.

---

## 4. Six corrections to the Capitol document

1. **The ask is inverted.** Ten files + two checklists + 3-year backfill + a counter behaviour change, all before Capitol sees a dollar. → Ask for **three files**, build the number, then send the full checklist with the number on top.
2. **CDK does not export to third-party IPs.** Data Export writes PGP-encrypted files to an SFTP folder *the dealer owns*. → Reword to "Capitol's own SFTP folder, or one we provision in Capitol's name; we collect from it." Upside: because Capitol shares its own data, CDK doesn't levy third-party integration fees.
3. **File 10 is a landmine.** Price/credit override logs with employee names and reasons is a staff-surveillance dataset; the parts manager it indicts is the person who must send it. → Cut from go-live. Excellent year-one product to the dealer principal.
4. **The counter habit change is unnecessary.** File 6 already carries `last received date` and `qty received`. → Drive arrival off the data. Cell-number capture stays a quality improver, never a requirement.
5. **No number anywhere.** → Lead with the Cox figures, land on Capitol's own declined total.
6. **One document doing two jobs.** → Split: Page A (GM: problem, modules, messages, the number). Page B (admin: file spec + checklists), sent after A lands. Retire *BayFill*, *ServiceLine*, *BackCounter* from dealer-facing docs.

Keep verbatim: the four sample messages and the paragraph on why they beat generic blasts. Best writing on the page.

---

## 5. The week-one ask (send this instead)

> We can show you exactly how much recoverable work is sitting in your DMS right now. To build that report we need three standard CDK exports — no configuration changes, no new software in the store.
>
> 1. **Customers** — CDK customer number, name, mobile, email, block/opt-out flags. Current file, no history needed.
> 2. **Vehicles and ownership** — VIN, year/make/model, customer number, delivery date, last known mileage.
> 3. **Declined services / denied operations** — last 24 months. RO number, close date, VIN, customer number, op code, description, quoted amount, advisor.
>
> Delivered as CSV to an SFTP folder Capitol owns — CDK's scheduled export writes there directly and we collect from it. One-time send is enough for the report; the daily drop gets set up only once you've seen the number.
>
> **What you get back within five business days:** one page showing total recoverable declined work by age bucket, by advisor, by job type, with customers ranked by recoverable dollars. Yours to keep either way.

**Why these three:** File 5 carries the quoted amount, so it alone builds the dollar total. Files 1–2 make each line a named customer with a real car. History, menu pricing, special orders, deal jackets and schedules make the *product* better — none are needed to make the *case*.

---

## 6. Compliance — the dates that shape the build

| Date | What |
|---|---|
| **24 Jan 2025** | One-to-one consent rule **vacated** (11th Cir., *Insurance Marketing Coalition v. FCC*); FCC formally deleted the language Sept 2025. No per-seller consent needed — major friction reduction for F&I. |
| **11 Apr 2025** | Revocation rules **in effect**. Revocation by any reasonable method; *stop, quit, end, revoke, opt out, cancel, unsubscribe* must be honoured. |
| **31 Jan 2027** | **"Revoke-all"** — a revocation on one topic applies to *all* future calls/texts on unrelated matters. Delayed twice (Apr 2025 → Apr 2026 → Jan 2027). |

**Build consequences:**
- **One global consent ledger per customer with a per-module overlay — built now.** From Jan 2027 a STOP on an AR text must silence service, parts and F&I. Retrofitting cross-module suppression across four live detectors is expensive; building it into the first detector is nearly free.
- **Segment the consent standard by module.** Parts arrival and AR balance concern an existing transaction. F&I product offers are marketing and need prior express written consent. Default F&I to explicit opt-in.
- **CDK block flags are the floor.** Layer own ledger + quiet hours by store timezone + state mini-TCPA rules.
- **AR texting needs counsel before volume.** First-party creditor sits outside FDCPA, but TCPA applies to the message and state collection statutes vary. Texting a named balance to a number that may not be the debtor's is the classic disclosure trap.

Not legal advice — get the four templates reviewed before Capitol goes live.

---

## 7. Architecture — one engine, four detectors

```
Obligation
  id                uuid
  group_id          dealer group — the unit of sale
  store_id          rooftop
  type              declined_asr | parts_arrival | fi_no_buy | ar_balance
  source_ref        RO#, special-order no, deal no, schedule line
  customer_ref      CDK customer no
  consent_ref       global ledger + per-module overlay
  vehicle_ref       VIN, mileage, delivery date
  amount_cents      the number that makes this worth working
  opened_at         when the obligation came into existence
  aged_days         derived — drives the bucket
  expires_at        F&I eligibility, obsolescence, statute
  recoverability    0–100 score
  state             open | queued | worked | recovered | written_off
  owner_user_id     a human name, always
  next_action_at    the clock nobody currently sets
  attempts[]        channel, timestamp, result, operator
  outcome_ref       the RO / deal / payment that closed it
  recovered_cents   the number you put in front of the GM
```

**Staff attribution first, not last.** The nightly job matching new ROs, deals and payments back to open obligations is what turns a tool into a P&L line. Without it, month four is an argument with a controller.

**Build cheaply now, before rooftop 10:** a file health monitor (expected arrival window, row-count delta, schema hash, alert on silence) and a DMS adapter interface with CSV as adapter one. Fortellis is adapter two, when volume justifies certification — today it only adds cost and delay.

### Phases

**1 · The number — days 1–14, three files, no build.**
Gate: the total makes Capitol go quiet, or it doesn't. Under ~$500k declined over 24 months, re-examine before writing production code.

**2 · Service detector, internal queue only — weeks 3–8.**
Obligation model, consent ledger, scoring, work queue, attribution. Declined ASRs only. **No customer is contacted** — the system tells advisors who to call, in what order, with the dollar beside each name. Zero TCPA surface, months faster.
Gate: an advisor opens it unprompted 5 days a week for a month and attribution shows recovered dollars.

**3 · Outbound + parts detector — weeks 8–14.**
SMS for service and parts (cleanest consent position). Parts arrival on the same engine.
Gate: parts ships in under five weeks. Twelve means the obligation model is wrong — fix at two detectors, not four.

**4 · AR, then F&I — weeks 14–24.**
AR with reviewed templates and segmented consent. F&I last: heaviest regulatory load, provider eligibility rules, touches the deal jacket.
Gate: two paying design partners outside Capitol before F&I ships.

---

## 8. Unit economics

Modelled on NADA / StoneEagle 2025 averages, ~1,350 ROs and ~100 units/month. Replace with Capitol's actuals after week one.

| Module | Derivation | Assumption | Monthly value |
|---|---|---|---|
| Declined ASRs | ~810 customer-pay ROs; ~40% carry an ASR; ~$400 avg declined | 8–15% recovered, ~55% GP | $5,700–10,700 |
| Parts arrival | $50k–88k obsolete carried; 20–30% carrying cost | 25% of new obsolescence prevented | $1,200–2,200 |
| F&I no-buy | 100 units; 55% VSC / 61% GAP / 83% maintenance no-buy | 3–7% post-sale close | $2,000–4,000 |
| AR & schedules | CIT 4–10 days healthy; aged customer-pay + warranty | 2-day CIT gain + 90+ recovery | $2,500–5,000 |
| **Total** | | | **$11,400–21,900** |

**Price against the alternative, not the feature.** A four-person BDC runs **$151k–201k base**, **$292k–454k all-in** (benefits, tech, training, turnover, management, facilities). Dealers underestimate true cost by 40–60% — and that team still wouldn't work declined ROs consistently.

| Tier | Includes | Per rooftop/mo | ROI |
|---|---|---|---|
| Business office | AR & schedules | $499 | 5–10× |
| Fixed ops | Service + parts | $999 | 7–13× |
| Full ledger | All four + group roll-up | $1,799 | 6–12× |
| Group | 10+ rooftops, principal dashboard | Negotiated | — |

**Flat price, revenue-share reporting.** Never take a percentage of recovered dollars — you'll spend your life arguing attribution and cap yourself at your own reporting accuracy. Charge flat, show recovered ÷ fee as an ROI multiple on every screen. At $1,799 you are **~5% of the annual cost of the BDC team you partially replace** — that's the closing sentence.

**Risk-reverse the pilot:** 90 days, we show recovered dollars or you don't renew. Affordable because the week-one report already told you the answer.

---

## 9. Scale path

CDK Drive is the core system for ~**15,000 franchised rooftops in North America** — ~40% of the US DMS market, ~$540bn annual commerce. That's the addressable universe on adapter one.

| Milestone | Rooftops | % of CDK base | ARPU | ARR |
|---|---|---|---|---|
| Capitol, paid pilot | 1–5 | — | $1,500 | $18k–90k |
| Year one | 50 | 0.3% | $1,500 | $900k |
| Year two | 250 | 1.7% | $1,600 | $4.8M |
| Year three | 750 | 5.0% | $1,800 | $16.2M |

Beyond 5% needs adapter two (Tekion, Dealertrack, DealerSocket) — which is why the DMS adapter interface goes in on day one. **Sell to the group, not the store:** same sales cycle, ten times the contract.

---

## 10. First fourteen days

**Days 1–2** — Rewrite Capitol doc into Page A (GM) and Page B (admin). Fix SFTP wording. Cut File 10 and the counter tap. Retire internal codenames. Send Page A with the Cox numbers and the three-file ask. Nothing else.

**Days 3–5** — Confirm SFTP mechanics with Capitol's admin (their folder, our collection, PGP keys). Stand up ingest and the obligation table; consent ledger schema in the same migration. Book legal review of the four templates now — lead time is the constraint.

**Days 6–10** — Files land. Build the recovery report: total declined by 30/60/90/180+ bucket, by advisor, by op code, ranked by recoverable dollars. Sanity-check against the NADA model — wild divergence is a data problem, not a discovery.

**Days 11–14** — Present the number in person or on video, never by email. Make the three asks: paid design-partner agreement, daily feed switched on, three peer intros. Confirm with CDK whether the dealer-owned export path carries any per-rooftop fee — that answer sets gross margin.

---

## The sentence it reduces to

> "Cox says dealers now handle 29% of service visits, down from 35%, and that only 54% of your two-year-old customers come back to you — it was 72% two years ago. The work your techs found is still getting done. It's getting done down the road. I can show you exactly how much of it left Capitol last year, by name, in five days, from three files you already have."

---

## Sources

1. Cox Automotive Service Industry Study, November 2025 — service visit share, retention, satisfaction drivers
2. NADA Annual Financial Profile of America's Franchised New-Car Dealerships, 2025 — RO counts, service/parts sales, labor rate, absorption
3. StoneEagle F&I Benchmark Report, Q4 2025 — PVR, VSC/GAP/maintenance penetration
4. *Insurance Marketing Coalition v. FCC* (11th Cir., 24 Jan 2025); FCC final rule eliminating one-to-one consent, Sept 2025
5. FCC consent-revocation rules effective 11 Apr 2025; revoke-all extended to 31 Jan 2027 (FCC DA 26-12)
6. Dealertrack — contracts-in-transit funding benchmarks
7. PartsEdge and fixed-ops parts benchmarks — obsolescence value, carrying cost, dead-stock thresholds
8. Strolid — in-house BDC cost analysis
9. CDK Global — Data Export and Import Tools; vendor profiles for DMS rooftop share
10. Kimoby published pricing — CDK integration fee

*Modelled figures are structured assumptions for the Capitol conversation, not forecasts. Regulatory dates current to Sept 2026 and are not legal advice.*
