# ===================================================== CAPITAL STACK ========
# Appended by build_model.py. Assumes the module-level helpers, styles and the
# R / C / PL / RT row registries are already in scope.

ws = wb.create_sheet("Capital Stack")
ws.sheet_view.showGridLines = False
for k, v in {"A": 48, "B": 16, "C": 16, "D": 54}.items():
    ws.column_dimensions[k].width = v

r = 1
put(ws, r, 1, "CAPITAL STACK — SBA & CREATIVE FINANCING", TITLE); r += 1
put(ws, r, 1, "Total project cost including real estate, and how it gets funded. "
              "All rates and structures are planning assumptions — confirm every one with your lender and CDC.",
    NOTE); r += 2
put(ws, r, 2, "18,000 SF", H2); put(ws, r, 3, "35,000 SF", H2); put(ws, r, 4, "Note", H2); r += 1

K = {}


def krow(key, text, fa, fb, fmt, note_text="", bold=False, fill=None, top=False, font=None):
    global r
    label(ws, r, text, bold=bold)
    bd = TOPLINE if top else None
    f = font or (TOTAL if bold else BODY)
    put(ws, r, 2, fa, f, fmt, fill, bd)
    put(ws, r, 3, fb, f, fmt, fill, bd)
    if note_text:
        note(ws, r, 4, note_text)
    K[key] = r
    r += 1


band(ws, r, "REAL ESTATE (BUY CASE)"); r += 1
krow("re_psf", "Building purchase price per SF ($)", 150, 150, MONEY,
     "Sarasota / Bradenton warehouse-flex. Verify against live comps", font=INPUT, fill=KEY)
krow("re_sf", "Building size (SF)",
     f"={AS('sf','B')}", f"={AS('sf','C')}", NUM, "SBA requires you to occupy at least 51%")
krow("re_price", "Building purchase price",
     f"=B{K['re_sf']}*B{K['re_psf']}", f"=C{K['re_sf']}*C{K['re_psf']}", MONEY)
krow("re_costs_pct", "Acquisition costs (% of price)", 0.03, 0.03, PCT,
     "Survey, environmental, legal, title, appraisal", font=INPUT)
krow("re_costs", "Acquisition costs",
     f"=B{K['re_price']}*B{K['re_costs_pct']}", f"=C{K['re_price']}*C{K['re_costs_pct']}", MONEY)
krow("re_total", "Real estate subtotal",
     f"=B{K['re_price']}+B{K['re_costs']}", f"=C{K['re_price']}+C{K['re_costs']}", MONEY,
     "", bold=True, top=True)
r += 1

band(ws, r, "TOTAL PROJECT COST"); r += 1
krow("venue", "Venue project cost (from Capex)",
     f"=Capex!$B${C['total']}", f"=Capex!$C${C['total']}", MONEY, "Fit-out, ESA equipment, FF&E, tech, pre-opening")
for cc in (2, 3):
    ws.cell(row=K['venue'], column=cc).font = LINK
krow("wc", "Working capital & debt service reserve", 350000, 550000, MONEY,
     "CRITICAL. Year 1 does not cover debt service — see the DSCR sheet", font=INPUT, fill=KEY)
krow("total_buy", "TOTAL PROJECT COST — BUY",
     f"=B{K['re_total']}+B{K['venue']}+B{K['wc']}",
     f"=C{K['re_total']}+C{K['venue']}+C{K['wc']}", MONEY, "", bold=True, fill=SUB, top=True)
krow("ti_psf", "Landlord TI allowance per SF ($) — lease case", 15, 15, MONEY,
     "Negotiable. A startup covenant gets less than an established one", font=INPUT)
krow("ti", "Landlord TI allowance",
     f"={AS('sf','B')}*B{K['ti_psf']}", f"={AS('sf','C')}*C{K['ti_psf']}", MONEY)
krow("total_lease", "TOTAL PROJECT COST — LEASE",
     f"=B{K['venue']}-B{K['ti']}+B{K['wc']}",
     f"=C{K['venue']}-C{K['ti']}+C{K['wc']}", MONEY, "", bold=True, fill=SUB, top=True)
r += 1

band(ws, r, "SBA 504 TRANCHE (BUY CASE)"); r += 1
put(ws, r, 1, "504 funds real estate and long-life equipment. Fit-out is real-property improvement.", NOTE); r += 1
krow("elig504", "504-eligible project cost",
     f"=B{K['re_total']}+{AS('sf','B')}*{AS('fitout_psf','B')}+Capex!$B${C['equip']}",
     f"=C{K['re_total']}+{AS('sf','C')}*{AS('fitout_psf','C')}+Capex!$C${C['equip']}", MONEY,
     "Real estate + fit-out + ESA equipment")
krow("inj_pct", "Borrower injection (%)", 0.20, 0.20, PCT,
     "Standard 504 is 10%. Add 5% for a startup and 5% for a special-purpose property. "
     "An entertainment venue is almost certainly both — plan for 20%", font=INPUT, fill=KEY)
krow("bank_pct", "Bank first mortgage (%)", 0.50, 0.50, PCT, "Conventional first lien", font=INPUT)
krow("cdc_pct", "CDC / SBA debenture (%)",
     f"=1-B{K['inj_pct']}-B{K['bank_pct']}", f"=1-C{K['inj_pct']}-C{K['bank_pct']}", PCT,
     "Second lien, below-market fixed rate, fully amortising")
krow("bank_amt", "Bank first mortgage",
     f"=B{K['elig504']}*B{K['bank_pct']}", f"=C{K['elig504']}*C{K['bank_pct']}", MONEY)
krow("cdc_amt", "CDC / SBA 504 debenture",
     f"=B{K['elig504']}*B{K['cdc_pct']}", f"=C{K['elig504']}*C{K['cdc_pct']}", MONEY,
     "Debenture caps apply — confirm the current limit with your CDC")
krow("inj504", "Injection against 504",
     f"=B{K['elig504']}*B{K['inj_pct']}", f"=C{K['elig504']}*C{K['inj_pct']}", MONEY)
r += 1

band(ws, r, "SBA 7(a) TRANCHE"); r += 1
krow("non504", "Costs not covered by 504",
     f"=B{K['total_buy']}-B{K['elig504']}", f"=C{K['total_buy']}-C{K['elig504']}", MONEY,
     "FF&E, technology, pre-opening, contingency, working capital")
krow("adv7a", "7(a) advance rate (%)", 0.85, 0.85, PCT,
     "Lender-dependent. Startups typically inject 10-20%", font=INPUT)
krow("amt7a", "SBA 7(a) loan",
     f"=B{K['non504']}*B{K['adv7a']}", f"=C{K['non504']}*C{K['adv7a']}", MONEY,
     "7(a) programme maximum applies — confirm with your lender")
krow("inj7a", "Injection against 7(a)",
     f"=B{K['non504']}-B{K['amt7a']}", f"=C{K['non504']}-C{K['amt7a']}", MONEY)
r += 1

band(ws, r, "FUNDING SUMMARY — BUY CASE"); r += 1
krow("debt", "Total debt",
     f"=B{K['bank_amt']}+B{K['cdc_amt']}+B{K['amt7a']}",
     f"=C{K['bank_amt']}+C{K['cdc_amt']}+C{K['amt7a']}", MONEY, "", bold=True)
krow("equity", "Total equity required",
     f"=B{K['inj504']}+B{K['inj7a']}", f"=C{K['inj504']}+C{K['inj7a']}", MONEY,
     "The cash you actually have to find", bold=True, fill=KEY)
krow("check", "Check: debt + equity = project cost",
     f"=B{K['debt']}+B{K['equity']}-B{K['total_buy']}",
     f"=C{K['debt']}+C{K['equity']}-C{K['total_buy']}", MONEY, "Must be zero")
krow("ltc", "Debt as % of total cost",
     f"=B{K['debt']}/B{K['total_buy']}", f"=C{K['debt']}/C{K['total_buy']}", PCT)
r += 1

band(ws, r, "CREATIVE FINANCING — REDUCING THE EQUITY CHEQUE"); r += 1
put(ws, r, 1, "Each of these lowers the cash you inject. Model them, then negotiate them.", NOTE); r += 1
krow("lev_presell", "Founding memberships presold (cash pre-opening)", 150000, 200000, MONEY,
     "Non-dilutive, and the only line here that also proves demand. Do this first", font=INPUT, fill=KEY)
krow("lev_esa", "ESA equipment on lease or vendor terms", 0, 0, MONEY,
     "Ask ESA to lease rather than sell. Moves capex to opex", font=INPUT)
krow("lev_seller", "Seller financing on the building", 0, 0, MONEY,
     "Second behind the bank. Requires lender standby consent", font=INPUT)
krow("lev_deposits", "Party & corporate booking deposits", 0, 0, MONEY,
     "Small, but it is float you would otherwise borrow", font=INPUT)
krow("lev_total", "Total creative financing",
     f"=SUM(B{K['lev_presell']}:B{K['lev_deposits']})",
     f"=SUM(C{K['lev_presell']}:C{K['lev_deposits']})", MONEY, "", bold=True, top=True)
krow("equity_net", "NET EQUITY REQUIRED",
     f"=B{K['equity']}-B{K['lev_total']}", f"=C{K['equity']}-C{K['lev_total']}", MONEY,
     "Lenders may not count all of these toward the required injection — ask first",
     bold=True, fill=SUB, top=True)

# ==================================================== DEBT & DSCR ===========
ws = wb.create_sheet("Debt & DSCR")
ws.sheet_view.showGridLines = False
ws.column_dimensions["A"].width = 48
for i in range(2, 7):
    ws.column_dimensions[get_column_letter(i)].width = 15
ws.column_dimensions["G"].width = 46

r = 1
put(ws, r, 1, "DEBT SERVICE & DSCR", TITLE); r += 1
put(ws, r, 1, "DSCR is the number the lender underwrites. Everything else is a conversation; this is the test.",
    NOTE); r += 2

band(ws, r, "RATES & TERMS", last_col=7); r += 1
put(ws, r, 2, "Principal", H2); put(ws, r, 3, "Rate", H2); put(ws, r, 4, "Years", H2)
put(ws, r, 5, "Annual payment", H2); put(ws, r, 6, "", H2); put(ws, r, 7, "Note", H2)
ws.cell(row=r, column=5).alignment = Alignment(horizontal="right")
r += 1

D = {}
tranches = [
    ("bank", "Bank first mortgage (504)", K['bank_amt'], 0.075, 25,
     "Conventional first lien, 25-year amortisation"),
    ("cdc", "CDC / SBA 504 debenture", K['cdc_amt'], 0.065, 25,
     "Below-market fixed. This is the cheap money in the stack"),
    ("sba7a", "SBA 7(a)", K['amt7a'], 0.1025, 10,
     "Variable, typically prime plus a spread. Model it high"),
]
first_tr = r
for key, text, src, rate, years, nte in tranches:
    label(ws, r, text)
    put(ws, r, 2, f"='Capital Stack'!$B${src}", LINK, MONEY)
    put(ws, r, 3, rate, INPUT, PCT)
    put(ws, r, 4, years, INPUT, NUM)
    put(ws, r, 5, f"=IF(B{r}=0,0,-PMT(C{r}/12,D{r}*12,B{r})*12)", BODY, MONEY)
    note(ws, r, 7, nte)
    D[key] = r
    r += 1

label(ws, r, "Total annual debt service", bold=True)
put(ws, r, 2, f"=SUM(B{first_tr}:B{r-1})", TOTAL, MONEY, border=TOPLINE)
put(ws, r, 5, f"=SUM(E{first_tr}:E{r-1})", TOTAL, MONEY, SUB, TOPLINE)
D["total_ds"] = r
r += 2

band(ws, r, "CASH AVAILABLE FOR DEBT SERVICE — 18,000 SF, BUY CASE", last_col=7); r += 1
for i in range(5):
    put(ws, r, 2 + i, f"Year {i+1}", H2)
    ws.cell(row=r, column=2 + i).alignment = Alignment(horizontal="right")
put(ws, r, 7, "Note", H2)
r += 1

label(ws, r, "Venue EBITDA (leased basis)")
for i in range(5):
    put(ws, r, 2 + i, f"='P&L'!{get_column_letter(2+i)}{PL['A']['ebitda']}", LINK, MONEY)
D["ebitda"] = r
note(ws, r, 7, "From the P&L, which assumes you pay rent")
r += 1

label(ws, r, "Add back: rent (you own the building)")
for i in range(5):
    put(ws, r, 2 + i, f"={AS('sf','B')}*{AS('rent_psf','B')}", BODY, MONEY)
D["rent_back"] = r
note(ws, r, 7, "Owning replaces rent with debt service")
r += 1

PTAX = r
label(ws, r, "Less: property tax & owner costs")
put(ws, r, 2, 0.017, INPUT, PCT)
note(ws, r, 7, "% of building value — Florida commercial. Edit this cell")
r += 1
D["ptax"] = r
label(ws, r, "  Property tax & owner costs", indent=1)
for i in range(5):
    put(ws, r, 2 + i, f"='Capital Stack'!$B${K['re_price']}*$B${PTAX}", BODY, MONEY)
r += 1

label(ws, r, "Cash available for debt service", bold=True)
for i in range(5):
    cl = get_column_letter(2 + i)
    put(ws, r, 2 + i, f"={cl}{D['ebitda']}+{cl}{D['rent_back']}-{cl}{D['ptax']}",
        TOTAL, MONEY, SUB, TOPLINE)
D["cads"] = r
r += 1

label(ws, r, "Annual debt service")
for i in range(5):
    put(ws, r, 2 + i, f"=$E${D['total_ds']}", BODY, MONEY)
D["ds"] = r
r += 1

label(ws, r, "DSCR", bold=True)
for i in range(5):
    cl = get_column_letter(2 + i)
    put(ws, r, 2 + i, f"=IF({cl}{D['ds']}=0,0,{cl}{D['cads']}/{cl}{D['ds']})", TOTAL, MULT, SUB)
D["dscr"] = r
note(ws, r, 7, "Lenders typically want 1.25x or better")
r += 1

COV = r
label(ws, r, "Covenant minimum")
put(ws, r, 2, 1.25, INPUT, MULT, KEY)
r += 1

label(ws, r, "Pass / fail", bold=True)
for i in range(5):
    cl = get_column_letter(2 + i)
    put(ws, r, 2 + i, f'=IF({cl}{D["dscr"]}>=$B${COV},"PASS","FAIL")', TOTAL)
    ws.cell(row=r, column=2 + i).alignment = Alignment(horizontal="right")
D["pass"] = r
note(ws, r, 7, "A Year 1 fail is normal for a startup venue — it is why the reserve exists")
r += 1

label(ws, r, "Cash flow after debt service")
for i in range(5):
    cl = get_column_letter(2 + i)
    put(ws, r, 2 + i, f"={cl}{D['cads']}-{cl}{D['ds']}", BODY, MONEY)
D["fcf"] = r
r += 1

label(ws, r, "Cumulative cash flow after debt service", bold=True)
put(ws, r, 2, f"=B{D['fcf']}", TOTAL, MONEY)
for i in range(1, 5):
    put(ws, r, 2 + i, f"={get_column_letter(1+i)}{r}+{get_column_letter(2+i)}{D['fcf']}", TOTAL, MONEY)
D["cum_fcf"] = r
note(ws, r, 7, "The most negative figure here is the minimum reserve you must fund")
r += 2

band(ws, r, "RETURN ON EQUITY", last_col=7); r += 1
label(ws, r, "Net equity injected", bold=True)
put(ws, r, 2, f"='Capital Stack'!$B${K['equity_net']}", LINK, MONEY)
D["eq"] = r
r += 1
label(ws, r, "Year 3 cash flow after debt service")
put(ws, r, 2, f"=D{D['fcf']}", BODY, MONEY)
D["y3fcf"] = r
r += 1
label(ws, r, "Year 3 cash-on-cash on equity", bold=True)
put(ws, r, 2, f"=IF(B{D['eq']}<=0,0,B{D['y3fcf']}/B{D['eq']})", TOTAL, PCT, SUB)
note(ws, r, 7, "Before principal paydown and any property appreciation")
r += 1
label(ws, r, "Year 5 cash-on-cash on equity", bold=True)
put(ws, r, 2, f"=IF(B{D['eq']}<=0,0,F{D['fcf']}/B{D['eq']})", TOTAL, PCT, SUB)
r += 2

band(ws, r, "THINGS TO CONFIRM BEFORE YOU BANK ON THIS", last_col=7); r += 1
for line in [
    "SBA eligibility depends on the ownership being US citizens or lawful permanent residents. If the",
    "ownership is non-US, the SBA route may not be available at all. Establish this before anything else.",
    "",
    "Every owner of 20% or more gives an unlimited personal guarantee. Understand what you are signing.",
    "504 debenture and 7(a) programme maximums, and whether the two can be combined at this size.",
    "Whether presold memberships and deposits count toward the required equity injection. Often they do not.",
    "Rates here are planning placeholders. Get a real term sheet before this model informs a decision.",
]:
    put(ws, r, 1, line, BODY if line else NOTE); r += 1
