# 09 · KPI Framework

Every KPI has one definition, one data source and one owner, agreed before go-live so that baseline and results
are measured the same way. Baselines come from [`sql/08_kpi_baseline.sql`](../sql/08_kpi_baseline.sql).

| KPI | Definition | Baseline | Phase 1 target | Phase 2 target | Source | Owner | Frequency |
|---|---|---|---|---|---|---|---|
| **Time to decision** | Median calendar days from *complete application* to *credit decision* | 16.2 days* | ≤ 8 | ≤ 3 | Workflow events | Head of Credit Ops | Daily |
| **Decisions within SLA** | % of decisions within 5 business days of complete application | 2.1%** | ≥ 60% | ≥ 90% | Workflow events | Head of Credit Ops | Daily |
| **First-time complete** | % of applications with zero post-submission document requests | 59% | ≥ 80% | ≥ 92% | Workflow events | SME Banking | Weekly |
| **Withdrawal rate** | % of applications ending as withdrawn or offer declined | 27.2% | ≤ 20% | ≤ 16% | Applications | Director SME Banking | Monthly |
| **Time to funding** | Median days from application to funds drawn | 28.0 days | ≤ 18 | ≤ 12 | Workflow events | Loan Ops | Monthly |
| **Underwriter load balance** | Max underwriter share ÷ even share | 1.56 | ≤ 1.2 | ≤ 1.2 | Allocation log | Credit team lead | Weekly |
| **Funded volume** | Number and € of SME loans funded | 3,694 / yr | +5% | +8% | Core banking | Director SME Banking | Monthly |
| **Credit quality (guardrail)** | 12-month default rate of loans approved under new authority vs old | – | No worse than baseline | No worse | Credit risk MI | Chief Credit Officer | Quarterly |
| **Customer satisfaction** | Post-decision NPS of SME applicants | survey: 61% cite "no status" | +15 pts | +25 pts | Survey | CX | Quarterly |

\* Baseline measured from submission (the "complete" timestamp is not captured today; FR-12 fixes this).
\** Baseline measured as decisions within 7 calendar days of submission.

## Dashboard layout (FR-13)
1. **Today:** applications in each of the 6 stages; SLA-at-risk list with owner.
2. **Trend:** weekly time to decision and withdrawal rate vs target.
3. **Quality:** first-time-complete rate by channel; document requests per application.
4. **Capacity:** open cases per underwriter; allocation balance.
5. **Guardrail:** credit-quality sampling results for decisions under new delegated authority.

A working prototype of this dashboard, built on the current-state data, is at [docs/index.html](../docs/index.html).
