"""Build the SME loan pipeline dashboard prototype (docs/index.html, served by GitHub Pages)."""
import shutil
import subprocess
import tempfile
from pathlib import Path

import duckdb
import pandas as pd
import plotly.graph_objects as go

from dashboard_kit import BLUE, CRITICAL, INK_2, MUTED, ORANGE, build_page

ROOT = Path(__file__).resolve().parents[1]
con = duckdb.connect()
con.execute(f"CREATE VIEW event_log AS SELECT * FROM read_csv_auto('{ROOT / 'data/event_log.csv'}')")
con.execute(f"CREATE VIEW applications AS SELECT * FROM read_csv_auto('{ROOT / 'data/applications.csv'}')")
sql = lambda f: con.sql((ROOT / "sql" / f).read_text()).df()

kpi = sql("08_kpi_baseline.sql").iloc[0]
funnel = sql("01_funnel.sql")
waits = sql("02_stage_waiting_times.sql").head(8)
loops = sql("03_rework_document_loops.sql")
route = sql("04_committee_vs_delegated.sql")
lost = sql("05_withdrawal_by_wait.sql")
uw = sql("06_underwriter_workload.sql")

with tempfile.TemporaryDirectory() as tmp:
    shutil.copy(ROOT / "deliverables/07_business_case.xlsx", f"{tmp}/bc.xlsx")
    subprocess.run(["soffice", "--headless", "--calc", "--convert-to", "xlsx", "--outdir", f"{tmp}/out", f"{tmp}/bc.xlsx"],
                   check=True, capture_output=True, timeout=300)
    summary = pd.read_excel(f"{tmp}/out/bc.xlsx", sheet_name="Summary", header=3, nrows=3)

# Funnel
f1 = go.Figure(go.Funnel(y=funnel.milestone, x=funnel.applications, marker_color=BLUE,
                         textinfo="value+percent initial", hovertemplate="%{y}<br>%{x:,} applications<extra></extra>"))

# Waiting points
w = waits.iloc[::-1]
f2 = go.Figure(go.Bar(x=w.total_case_days / 1000, y=[t.replace("  ->  ", " → ") for t in w.transition], orientation="h",
                      marker_color=[CRITICAL if i >= len(w) - 3 else BLUE for i in range(len(w))],
                      customdata=w[["median_days", "occurrences"]],
                      hovertemplate="%{y}<br>%{x:.1f}k case-days<br>median %{customdata[0]:.1f} days, "
                      "%{customdata[1]:,} times<extra></extra>"))
f2.update_layout(xaxis_title="Thousand case-days waiting", bargap=0.3, margin=dict(l=10))

# Document loops
f3 = go.Figure()
f3.add_bar(x=loops.doc_requests, y=loops.median_days_to_decision, marker_color=BLUE, name="Median days to decision",
           customdata=loops[["applications", "withdrawal_rate_pct"]],
           hovertemplate="%{x} document requests<br>%{y:.1f} days to decision<br>%{customdata[0]:,} applications"
           "<br>%{customdata[1]:.1f}% withdrew<extra></extra>")
f3.update_layout(xaxis_title="Number of missing-document requests", yaxis_title="Median days to decision", bargap=0.4)

# Lost after approval
f4 = go.Figure(go.Bar(x=lost.time_to_decision.str[3:], y=lost.lost_after_approval_pct, marker_color=ORANGE,
                      customdata=lost.approved_applications,
                      hovertemplate="Decision in %{x}<br>%{y:.1f}% lost after approval<br>%{customdata:,} approved"
                      "<extra></extra>"))
f4.update_layout(xaxis_title="Days from application to decision", yaxis_title="% of approved customers lost", bargap=0.4)

# Underwriter workload
even = 100 / len(uw)
f5 = go.Figure(go.Bar(x=uw.underwriter, y=uw.share_pct, marker_color=[CRITICAL if v > even * 1.3 else BLUE for v in uw.share_pct],
                      customdata=uw.assessments, hovertemplate="%{x}<br>%{y:.1f}% of assessments (%{customdata:,})<extra></extra>"))
f5.add_hline(y=even, line=dict(color=INK_2, width=1, dash="dash"), annotation_text="even share", annotation_position="top right")
f5.update_layout(yaxis_title="% of assessments", bargap=0.4)

# Business case
s = summary.iloc[1:]
f6 = go.Figure(go.Bar(x=s["Option"], y=s["NPV (€)"] / 1e6, marker_color=[BLUE, MUTED], width=0.45,
                      text=[f"€{v / 1e6:.1f}M" for v in s["NPV (€)"]], textposition="outside",
                      customdata=s[["Payback (years)"]],
                      hovertemplate="%{x}<br>NPV €%{y:.2f}M<br>payback %{customdata[0]:.1f} years<extra></extra>"))
f6.update_layout(yaxis=dict(title="5-year NPV (€M)", range=[0, 4]))

committee = route[route.route.str.startswith("Credit committee")].iloc[0]
b = summary.iloc[1]
build_page(
    title="SME Loan Pipeline: Current-State Dashboard",
    intro="Harbour Bank Ireland is <b>fictional</b> and the event log is <b>simulated</b>: 5,995 SME loan applications, "
          "70,399 process events. This is a prototype of the KPI dashboard specified in requirement FR-13.",
    kpis=[("Median days to decision", f"{kpi.median_days_to_decision:.1f}", "target ≤ 5 business days"),
          ("Decided within 7 days", f"{kpi.decided_within_7_days_pct:.1f}%", "of applications"),
          ("Withdrawal rate", f"{kpi.withdrawn_pct:.1f}%", f"€{kpi.withdrawn_lending_eur_m:.0f}M of lending a year"),
          ("Complete first time", f"{kpi.first_time_complete_pct:.0f}%", "target ≥ 80%"),
          ("Committee wait (≥ €100k)", f"{committee.median_wait_days:.1f} days", f"P90 {committee.p90_wait_days:.0f} days")],
    cards=[
        {"title": "Application funnel", "fig": f1, "sub": "38% of applications never get funded."},
        {"title": "Where applications wait", "fig": f2, "height": 340, "wide": True,
         "sub": "Document chasing, the underwriter queue and manual assessment are the top three."},
        {"title": "Rework: missing-document loops", "fig": f3,
         "sub": "41% of applications are incomplete. Each loop adds about 6 days."},
        {"title": "Approved customers lost by decision time", "fig": f4,
         "sub": "16% lost when we decide in < 10 days, 39% at 25+ days."},
        {"title": "Underwriter workload", "fig": f5, "sub": "Two underwriters carry 45 to 56% more than an even share."},
        {"title": "Business case: 5-year NPV", "fig": f6,
         "sub": "Option B (quick wins) pays back in about a year. Recommended now, with C as phase 2."},
    ],
    insights=[
        "<b>Speed is revenue.</b> Every extra week to decision costs approved customers. 27% of applicants withdraw.",
        "<b>Fix the front door.</b> A personalised checklist and digital upload target the 41% of incomplete applications.",
        "<b>Stop the weekly wait.</b> Delegated authority to €250k and a daily credit forum remove a median 7-day delay.",
        f"<b>Business case:</b> quick wins NPV €{b['NPV (€)'] / 1e6:.1f}M, payback under a year, still positive at 25% realisation.",
    ],
    footer="Fictional bank, simulated data. See the deliverables folder for the BRD, process maps, user stories and business case.",
    path=ROOT / "docs/index.html",
)
print("Dashboard written to docs/index.html")
