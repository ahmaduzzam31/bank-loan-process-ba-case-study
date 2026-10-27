# 08 · User Acceptance Testing (UAT) Plan: Phase 1

## 1. Objective
Confirm that the phase 1 solution meets the business requirements in the [BRD](04_business_requirements_document.md) and is
ready for go-live, as judged by the people who will use it.

## 2. Scope
Epics E1 (complete first time), E2 (faster decisions), E3 (transparency) and E5 (control & insight). Phase 2 (E4) is out of scope.

## 3. Roles
| Role | Responsibility |
|---|---|
| Business Analyst | Writes test scenarios, coordinates UAT, triages defects, reports progress |
| UAT testers | 3 RMs, 2 underwriters, 1 compliance analyst, 2 pilot brokers |
| Product owner (SME Banking) | Prioritises defects, gives go/no-go recommendation |
| IT test lead | Environment, test data, defect fixes |

## 4. Entry and exit criteria
| Entry criteria | Exit criteria |
|---|---|
| System test passed with no open Critical/High defects | **100%** of Must-have scenarios executed; **≥ 95%** passed |
| UAT environment with anonymised test data | **No open Critical or High** defects |
| Testers trained (1-hour session) | Medium defects have an agreed workaround and fix date |
| Test scenarios reviewed by product owner | Sign-off by Sponsor, Chief Credit Officer and Head of Compliance |

## 5. Test scenarios
| ID | Scenario | Requirement | User story | Expected result | Priority |
|---|---|---|---|---|---|
| UAT-01 | Secured loan for a limited company shows full checklist | FR-01 | US-01 | Checklist includes valuation, accounts, statements, tax clearance, ID | Must |
| UAT-02 | Small unsecured loan shows reduced checklist | FR-01 | US-01 | Valuation and management accounts not requested | Must |
| UAT-03 | Upload rejects wrong file type / oversize file | FR-02 | US-01 | Clear error message, file not stored | Must |
| UAT-04 | Submit with missing mandatory document | FR-03 | US-02 | Submission blocked, missing item named | Must |
| UAT-05 | Submit complete application | FR-03, BRL-02 | US-02 | Status "Received"; SLA clock starts | Must |
| UAT-06 | Reminder sent after 2 business days | FR-04 | US-03 | SMS + email with outstanding items | Should |
| UAT-07 | Senior underwriter approves €220k | FR-05, FR-11 | US-04 | Final decision; full audit record | Must |
| UAT-08 | €400k application routed to daily forum | FR-05 | US-04 | Queued for next forum; decision within 1 business day | Must |
| UAT-09 | Underwriter (non-senior) tries to approve €150k | FR-05, BRL-01 | US-04 | Action blocked; referral to senior or forum | Must |
| UAT-10 | Auto-allocation to least-loaded eligible underwriter | FR-06 | US-05 | Assigned to UW with fewest open cases | Should |
| UAT-11 | Manual reassignment requires reason | FR-06, FR-11 | US-05 | Reason mandatory; audit entry created | Should |
| UAT-12 | Customer sees 6-stage tracker and expected date | FR-07 | US-06 | Correct stage and date shown | Must |
| UAT-13 | Broker notified on decision | FR-08 | US-07 | Email within 5 minutes | Must |
| UAT-14 | Decision not released before KYC passes | BRL-03 | US-04 | Offer cannot be issued until KYC complete | Must |
| UAT-15 | Decline triggers written reasons letter | BRL-04 | – | Letter generated within 5 business days | Must |
| UAT-16 | Dashboard lists SLA-at-risk applications | FR-13 | US-08 | Applications > 4 business days without decision listed | Should |
| UAT-17 | Every stage change logged with timestamp and user | FR-12 | – | Event present in log extract | Must |

## 6. Defect severity
| Severity | Definition | Example | Fix target |
|---|---|---|---|
| Critical | Blocks a core journey or breaches regulation | Decision released before KYC | Before go-live |
| High | Major function wrong, no workaround | Wrong delegated authority applied | Before go-live |
| Medium | Function wrong, workaround exists | Reminder sent at wrong time | Agreed date |
| Low | Cosmetic | Label typo | Backlog |

## 7. Schedule
| Activity | Dates |
|---|---|
| Test preparation and data setup | 01 to 05 Mar 2027 |
| UAT cycle 1 | 08 to 12 Mar 2027 |
| Fixes and cycle 2 (regression) | 15 to 19 Mar 2027 |
| Go / no-go meeting | 22 Mar 2027 |
