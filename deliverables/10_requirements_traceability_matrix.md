# 10 · Requirements Traceability Matrix (RTM)

Each business need traces forward to a requirement, a user story, a test and a KPI, and back to the pain point
that justified it. Any requirement without a test, or a test without a requirement, is a gap.

| Pain point | Business req. | Functional req. / rule | User story | UAT scenario | KPI | Phase | Status |
|---|---|---|---|---|---|---|---|
| P1 Document chasing | BR-02 | FR-01 Personalised checklist | US-01 | UAT-01, UAT-02 | First-time complete | 1 | Approved |
| P1 Document chasing | BR-02 | FR-02 Digital upload + validation | US-01 | UAT-03 | First-time complete | 1 | Approved |
| P1 Document chasing | BR-02 | FR-03 Block incomplete submission | US-02 | UAT-04, UAT-05 | First-time complete | 1 | Approved |
| P1 Document chasing | BR-02 | FR-04 Automatic reminders | US-03 | UAT-06 | First-time complete | 1 | Approved |
| P2 Weekly committee | BR-04 | FR-05 Delegated authority €250k + daily forum; BRL-01 | US-04 | UAT-07, UAT-08, UAT-09 | Time to decision; credit quality | 1 | Pending CCO approval |
| P4 Uneven workload | BR-05 | FR-06 Capacity-based routing | US-05 | UAT-10, UAT-11 | Load balance | 1 | Approved |
| P5 No status visibility | BR-06 | FR-07 Status tracker | US-06 | UAT-12 | NPS; withdrawal rate | 1 | Approved |
| P5 No status visibility | BR-06 | FR-08 Notifications | US-07 | UAT-13 | NPS; withdrawal rate | 1 | Approved |
| P6 Lost after approval | BR-01 | BRL-02 SLA clock definition | US-02 | UAT-05 | Decisions within SLA | 1 | Approved |
| (constraint) | BR-07 | FR-11 Decision audit trail | US-04, US-05 | UAT-07, UAT-11 | – | 1 | Approved |
| (constraint) | BR-07 | BRL-03 KYC before decision released | US-04 | UAT-14 | – | 1 | Approved |
| (constraint) | BR-07 | BRL-04 Written decline reasons | – | UAT-15 | – | 1 | Approved |
| (measurement) | BR-08 | FR-12 Event logging | US-08 | UAT-17 | All KPIs | 1 | Approved |
| (measurement) | BR-08 | FR-13 Pipeline dashboard | US-08 | UAT-16 | All KPIs | 1 | Approved |
| P3 Re-keying | BR-03 | FR-09 Open-banking import | US-09 | Phase 2 UAT | Time to decision | 2 | Draft |
| P3 Re-keying | BR-03 | FR-10 Automatic ratios | US-10, US-11 | Phase 2 UAT | Time to decision | 2 | Draft |
| P6 Lost after approval | BR-01 | FR-14 Automated decisions ≤ €50k | US-12 | Phase 2 UAT | Decisions within SLA | 2 | Draft |

**Coverage check:** 8 of 8 business requirements are traced to at least one test. All 17 phase 1 UAT scenarios trace to a
requirement. Phase 2 tests will be written when phase 2 starts.
