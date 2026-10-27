# 01 · Project Charter: SME Loan Origination Redesign

> **Fictional case study.** Harbour Bank Ireland is an invented bank. Process data is simulated; stakeholder
> interviews are illustrative.

| | |
|---|---|
| **Project** | SME Loan Origination Redesign ("Faster Yes") |
| **Sponsor** | Director of SME Banking |
| **Business Analyst** | Ahmad Uzzam |
| **Version / date** | v1.0 · October 2026 |
| **Status** | Approved for analysis & design |

## 1. Problem statement
Small and medium-sized businesses wait a **median of 16 days for a credit decision** and **28 days for funds**.
**27% of applicants withdraw**: €162M of requested lending a year. Competing fintech lenders advertise decisions
within 48 hours. Staff spend much of their time chasing documents and re-typing financial statements.

## 2. Objectives (SMART)
| # | Objective | Baseline | Target | By |
|---|---|---|---|---|
| O1 | Reduce median time from application to credit decision | 16.2 days | **≤ 5 business days** | Q4 2027 |
| O2 | Increase applications complete at first submission | 59% | **≥ 80%** | Q2 2027 |
| O3 | Reduce applicant withdrawal rate | 27.2% | **≤ 18%** | Q4 2027 |
| O4 | Cut underwriter time spent re-keying financials | ~45 min per case | **≤ 10 min** (phase 2) | Q4 2027 |
| O5 | Give customers real-time application status | none | **100% of online applications** | Q2 2027 |

## 3. Scope
| In scope | Out of scope |
|---|---|
| SME term loans and overdrafts **€10k to €750k** | Corporate lending above €750k, mortgages, consumer loans |
| All channels: online, branch, broker | Credit risk appetite and pricing policy (no change to credit standards) |
| Steps from application submitted to loan funded | Collections and arrears management |
| Credit approval authority and committee process | Core banking system replacement |
| Document collection, KYC/AML hand-offs, status communication | Broker commission structure |

## 4. Deliverables
1. Stakeholder analysis and RACI ([02](02_stakeholder_analysis.md))
2. Current-state (AS-IS) process map with pain-point evidence ([03](03_current_state_process.md))
3. Business Requirements Document ([04](04_business_requirements_document.md))
4. Future-state (TO-BE) process and gap analysis ([05](05_future_state_process.md))
5. Prioritised product backlog with user stories ([06](06_user_stories.md))
6. Business case and options appraisal ([07](07_business_case.md), [xlsx](07_business_case.xlsx))
7. UAT plan ([08](08_uat_plan.md)), KPI framework ([09](09_kpi_framework.md)), traceability matrix ([10](10_requirements_traceability_matrix.md))

## 5. Assumptions
* Credit policy and risk appetite stay unchanged. Faster decisions must not mean weaker credit standards.
* Open-banking (PSD2) account data and accounting-software connections are available for most SME customers.
* The Credit Risk function will approve higher delegated authority if the quality of decisions is monitored.

## 6. Constraints
* Central Bank of Ireland **Consumer Protection Code** and SME Lending Regulations must be respected (e.g. written reasons for decline).
* AML/CFT obligations: KYC cannot be shortened, only made more efficient.
* Budget envelope: €0.5M for phase 1. Phase 2 subject to separate approval.

## 7. Key risks
| Risk | Impact | Likelihood | Mitigation |
|---|---|---|---|
| Credit Risk resists higher delegated authority | High | Medium | Pilot with post-decision quality sampling; monthly reporting to the Credit Risk Committee |
| Staff see automation as a threat to roles | Medium | Medium | Early involvement in design; reposition time saved to relationship work |
| Customers do not adopt the digital upload | Medium | Low | Keep assisted channel; RM sends upload link by SMS |
| Data quality in the event log limits measurement | Medium | Medium | Agree KPI definitions with MI team before go-live ([09](09_kpi_framework.md)) |

## 8. High-level timeline
| Phase | Timing | Content |
|---|---|---|
| Discovery & analysis | Oct to Nov 2026 | Interviews, process mining, AS-IS, BRD |
| Phase 1: quick wins | Dec 2026 to Mar 2027 | Checklist + digital upload, delegated authority, daily credit forum, status tracking |
| Phase 2: digital origination | Apr to Dec 2027 | Open-banking data capture, automated spreading, decision engine for ≤ €100k |
