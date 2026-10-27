# %% [markdown]
# # SME Loan Origination: Current-State Process Analysis
#
# **Harbour Bank Ireland is fictional and the event log is simulated** ([`src/generate_event_log.py`](../src/generate_event_log.py)).
#
# This notebook is the **evidence base** for the business analysis deliverables. It quantifies the pain points
# that stakeholders described in workshops, and sizes the opportunity for the business case.
#
# **Data:** 5,995 SME loan applications (Oct 2025 to Sep 2026) and 70,399 process events (*case, activity, timestamp, resource*),
# the standard format used by process-mining tools such as Celonis.

# %%
import json
import sys
from pathlib import Path

import duckdb
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression

ROOT = Path.cwd().parent if Path.cwd().name == "notebooks" else Path.cwd()
sys.path.insert(0, str(ROOT / "src"))
import style  # noqa: E402

style.apply()
FIG = ROOT / "reports/figures"
FIG.mkdir(parents=True, exist_ok=True)
pd.set_option("display.width", 160, "display.max_colwidth", 120)

con = duckdb.connect()
con.execute(f"CREATE VIEW event_log AS SELECT * FROM read_csv_auto('{ROOT / 'data/event_log.csv'}')")
con.execute(f"CREATE VIEW applications AS SELECT * FROM read_csv_auto('{ROOT / 'data/applications.csv'}')")
sql = lambda f: con.sql((ROOT / "sql" / f).read_text()).df()

# %% [markdown]
# ## 1. Baseline KPIs

# %%
kpi = sql("08_kpi_baseline.sql")
kpi.T.rename(columns={0: "baseline"})

# %% [markdown]
# **Takeaway:** a median of **16 days to a credit decision** and **28 days to funds**, with only **2% decided within a week**.
# Fintech lenders advertise SME decisions in 24 to 48 hours. **27% of applicants withdraw**, which means €162M of
# requested lending walks out of the door.

# %% [markdown]
# ## 2. Funnel: where are applications lost?

# %%
funnel = sql("01_funnel.sql")
outcomes = pd.read_csv(ROOT / "data/applications.csv").outcome.value_counts()

fig, ax = plt.subplots(figsize=(9, 3.6))
ax.barh(funnel.milestone[::-1], funnel.applications[::-1], color=style.BLUE, height=0.6)
for i, (v, p) in enumerate(zip(funnel.applications[::-1], funnel.pct_of_submitted[::-1])):
    ax.text(v + 60, i, f"{v:,}  ({p:.0f}%)", va="center", color=style.INK_2, fontsize=9)
ax.set_xlim(0, 7200)
ax.set_title("Application funnel: 38% of applications never get funded")
ax.set_xlabel("Applications"); ax.grid(axis="x"); ax.grid(axis="y", visible=False)
style.save(fig, FIG / "01_funnel.png")
funnel

# %% [markdown]
# ## 3. Where does the time go?
# Time between consecutive activities, summed over all cases. This shows **where applications sit waiting**.

# %%
waits = sql("02_stage_waiting_times.sql")
top = waits.head(8).iloc[::-1]
fig, ax = plt.subplots(figsize=(10, 4.2))
labels = [t.replace("  ->  ", " → ") for t in top.transition]
ax.barh(labels, top.total_case_days / 1000, color=[style.CRITICAL if i >= len(top) - 3 else style.BLUE
                                                   for i in range(len(top))], height=0.6)
for i, (v, m) in enumerate(zip(top.total_case_days / 1000, top.median_days)):
    ax.text(v + 0.2, i, f"{v:.1f}k days  (median {m:.1f} d)", va="center", fontsize=8.5, color=style.INK_2)
ax.set_xlim(0, 28)
ax.set_title("Top waiting points (total case-days across all applications)")
ax.set_xlabel("Thousand case-days"); ax.grid(axis="x"); ax.grid(axis="y", visible=False)
style.save(fig, FIG / "02_waiting_points.png")
waits

# %% [markdown]
# **Takeaway:** the three biggest sinks of elapsed time are:
# 1. **Waiting for missing documents** (22k case-days). The application is incomplete at the start.
# 2. **Waiting in the underwriter queue** after KYC (22k case-days). This is a capacity and allocation issue.
# 3. **Manual credit assessment after re-keying financials** (19k case-days).
#
# The **weekly credit committee** adds a median 7 days to every loan of €100k or more (next section).

# %% [markdown]
# ## 4. Root cause deep dives

# %%
loops = sql("03_rework_document_loops.sql")
route = sql("04_committee_vs_delegated.sql")
print(route.to_string(index=False), "\n")
loops

# %%
lost = sql("05_withdrawal_by_wait.sql")
fig, axes = plt.subplots(1, 2, figsize=(12, 3.8))
ax = axes[0]
ax.bar(loops.doc_requests, loops.median_days_to_decision, color=style.BLUE, width=0.55)
for i, (d, w) in enumerate(zip(loops.median_days_to_decision, loops.withdrawal_rate_pct)):
    ax.text(i, d + 0.6, f"{d:.0f} days\n{w:.0f}% withdraw", ha="center", fontsize=8.5, color=style.INK_2)
ax.set_ylim(0, 42)
ax.set_title("Each missing-documents loop adds about 6 days")
ax.set_xlabel("Number of document requests"); ax.set_ylabel("Median days to decision")
ax = axes[1]
ax.bar(lost.time_to_decision.str[3:], lost.lost_after_approval_pct, color=style.ORANGE, width=0.55)
for i, v in enumerate(lost.lost_after_approval_pct):
    ax.text(i, v + 0.8, f"{v:.0f}%", ha="center", fontsize=9, color=style.INK_2)
ax.set_ylim(0, 46)
ax.set_title("Approved customers walk away when we are slow")
ax.set_xlabel("Days from application to credit decision"); ax.set_ylabel("% lost after approval")
fig.tight_layout()
style.save(fig, FIG / "03_root_causes.png")
lost

# %% [markdown]
# **Takeaway:**
# * **41% of applications are incomplete** on arrival. Each document loop adds about 6 days and raises withdrawal risk.
# * Loans ≥ €100k wait a **median 7.1 days (P90 13 days)** for the weekly committee, against same-day delegated decisions.
# * Even **approved** customers are lost: **16% when the decision takes under 10 days, 39% after 25+ days**. Speed is revenue.

# %%
uw = sql("06_underwriter_workload.sql")
variants = sql("07_process_variants.sql")
print("Underwriter workload:")
print(uw.to_string(index=False))
print(f"\nTop 8 process variants cover {variants.pct.sum():.0f}% of applications; "
      f"the 'happy path' (variant 1) is only {variants.pct.iloc[0]:.0f}%.")

# %% [markdown]
# ## 5. Sizing the opportunity
# **How many more loans would we fund if we were faster?**
#
# A logistic regression on approved applications estimates how the probability of losing the customer depends on
# days to decision. Separately, the pre-decision withdrawal rate is measured for applications with and without
# document loops. Both are then applied to the two future-state options.

# %%
ev = pd.read_csv(ROOT / "data/event_log.csv", parse_dates=["timestamp"])
apps = pd.read_csv(ROOT / "data/applications.csv").set_index("case_id")
piv = ev.pivot_table(index="case_id", columns="activity", values="timestamp", aggfunc="min")
apps["days_to_decision"] = (piv[["Credit committee decision", "Delegated authority decision"]].min(axis=1)
                            - piv["Application submitted"]).dt.total_seconds() / 86400
decided = apps.dropna(subset=["days_to_decision"])
approved = decided[decided.outcome != "Declined"]
model = LogisticRegression().fit(approved[["days_to_decision"]], (approved.outcome == "Withdrawn").astype(int))
p_lost = lambda days: model.predict_proba(pd.DataFrame({"days_to_decision": np.atleast_1d(days)}))[:, 1]

pre_withdraw = apps.days_to_decision.isna() & (apps.outcome == "Withdrawn")
pre_rate = {k: pre_withdraw[apps.doc_loops > 0].mean() if k else pre_withdraw[apps.doc_loops == 0].mean() for k in (0, 1)}
print(f"Probability an approved customer walks away: {p_lost(5)[0]:.1%} at 5 days, "
      f"{p_lost(16)[0]:.1%} at 16 days, {p_lost(30)[0]:.1%} at 30 days")
print(f"Pre-decision withdrawal: {pre_rate[0]:.1%} with complete applications vs {pre_rate[1]:.1%} with document loops")

# %%
N = len(apps)
decline_rate = (apps.outcome == "Declined").mean()
incomplete_now = (apps.doc_loops > 0).mean()
scenarios = {
    "A. Do nothing":                        {"median_days": apps.days_to_decision.median(), "incomplete": incomplete_now},
    "B. Process quick wins":                {"median_days": 8.0, "incomplete": 0.20},
    "C. Digital origination + quick wins":  {"median_days": 3.0, "incomplete": 0.08},
}
rows = []
current_days = approved.days_to_decision
for name, s in scenarios.items():
    shift = s["median_days"] / apps.days_to_decision.median()              # scale the whole distribution
    lost_after = p_lost(current_days * shift).mean()
    pre = s["incomplete"] * pre_rate[1] + (1 - s["incomplete"]) * pre_rate[0]
    reach_decision = 1 - pre
    funded_rate = reach_decision * (1 - decline_rate / (1 - pre_withdraw.mean())) * (1 - lost_after)
    rows.append({"option": name, "median_days_to_decision": s["median_days"], "first_time_complete": 1 - s["incomplete"],
                 "pre_decision_withdrawal": pre, "lost_after_approval": lost_after, "funded_rate": funded_rate,
                 "funded_loans_per_year": funded_rate * N})
opp = pd.DataFrame(rows).set_index("option")
calib = opp.loc["A. Do nothing", "funded_rate"] / (apps.outcome == "Funded").mean()
opp["funded_rate"] /= calib                                                 # calibrate option A to actual
opp["funded_loans_per_year"] /= calib
opp["extra_funded_loans"] = opp.funded_loans_per_year - opp.loc["A. Do nothing", "funded_loans_per_year"]
opp.round(3)

# %% [markdown]
# **Takeaway:** at the same application volume and credit standards, **Option B funds about 450 more loans a year and
# Option C about 690 more**, just by not losing customers to delay. That is new lending won without taking more credit risk.
# These are model estimates, so the business case only counts **50% of them** (a realisation factor) to stay conservative.

# %%
avg_funded = apps.loc[apps.outcome == "Funded", "amount_eur"].mean()
opportunity = {
    "applications_per_year": int(N),
    "baseline_funded_rate": round(float((apps.outcome == "Funded").mean()), 4),
    "avg_funded_loan_eur": round(float(avg_funded), 0),
    "extra_funded_loans_option_b": round(float(opp.loc["B. Process quick wins", "extra_funded_loans"]), 0),
    "extra_funded_loans_option_c": round(float(opp.loc["C. Digital origination + quick wins", "extra_funded_loans"]), 0),
    "assessments_per_year": int(apps.days_to_decision.notna().sum()),
    "document_requests_per_year": int((ev.activity == "Missing documents requested").sum()),
    "median_days_to_decision": round(float(apps.days_to_decision.median()), 1),
}
(ROOT / "reports").mkdir(exist_ok=True)
(ROOT / "reports/opportunity.json").write_text(json.dumps(opportunity, indent=2))
opportunity

# %% [markdown]
# These figures feed the **business case workbook** ([`deliverables/07_business_case.xlsx`](../deliverables/07_business_case.xlsx)).
#
# ## 6. Summary of evidence for the BA deliverables
#
# | Pain point (from stakeholder workshops) | Evidence from the data | Requirement it drives |
# |---|---|---|
# | "Customers complain it takes weeks" | Median 16 days to decision, 2% within 7 days | BR-01 decision SLA |
# | "We chase documents constantly" | 41% incomplete on arrival, 3,883 document requests, +6 days per loop | BR-02 digital checklist & upload |
# | "Big loans sit waiting for committee" | Median 7.1-day wait for ≥€100k loans | BR-04 delegated authority & daily credit forum |
# | "Underwriters spend hours re-typing accounts" | Underwriter queue + manual assessment = 41k case-days | BR-03 automated financial data capture |
# | "Some underwriters are swamped" | Two underwriters carry 45 to 56% more than an even share | BR-05 workload-balanced allocation |
# | "We lose customers to fintechs" | 27% withdraw. Approved customers lost 16% → 39% as time to decision rises | BR-06 status tracking & proactive updates |
