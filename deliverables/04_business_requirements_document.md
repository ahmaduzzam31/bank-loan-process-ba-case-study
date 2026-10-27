# 04 · Business Requirements Document (BRD)

> Fictional case study: Harbour Bank Ireland, SME Loan Origination Redesign.

| | |
|---|---|
| **Document owner** | Business Analyst |
| **Approvers** | Director of SME Banking (Sponsor), Chief Credit Officer, Head of Compliance, Head of Digital |
| **Version** | 1.0 (for sign-off) |
| **Related** | [Charter](01_project_charter.md) · [AS-IS](03_current_state_process.md) · [TO-BE](05_future_state_process.md) · [Backlog](06_user_stories.md) · [RTM](10_requirements_traceability_matrix.md) |

## 1. Purpose
This document defines **what** the business needs from the redesigned SME loan origination process. It does not
define **how** the solution will be built. Every requirement traces to a pain point ([03](03_current_state_process.md))
and to test cases ([08](08_uat_plan.md)).

## 2. Business requirements
| ID | Business requirement | Pain point | Priority (MoSCoW) |
|---|---|---|---|
| **BR-01** | The bank shall give SME applicants a credit decision within **5 business days** of a complete application, for loans up to €750k. | P1, P2, P6 | **Must** |
| **BR-02** | Applications shall be **complete at first submission** in at least 80% of cases. | P1 | **Must** |
| **BR-03** | Financial data shall be captured **without manual re-keying** by underwriters. | P3 | **Should** (phase 2) |
| **BR-04** | Credit decisions shall not wait for a weekly committee when they are within an experienced underwriter's competence. | P2 | **Must** |
| **BR-05** | Underwriting work shall be **allocated by capacity and complexity**, not ad hoc. | P4 | **Should** |
| **BR-06** | Customers, brokers and RMs shall see **real-time application status**. | P5, P6 | **Must** |
| **BR-07** | All changes shall keep full compliance with AML/KYC and Central Bank of Ireland requirements, with a complete audit trail. | (constraint) | **Must** |
| **BR-08** | Management shall have a **daily KPI dashboard** of the origination pipeline. | (measurement) | **Should** |

## 3. Functional requirements
| ID | Functional requirement | Traces to | Priority |
|---|---|---|---|
| FR-01 | The system shall generate a **personalised document checklist** based on loan amount, purpose, entity type and secured/unsecured. | BR-02 | Must |
| FR-02 | Customers and brokers shall **upload documents digitally** (web and mobile), with file-type and completeness validation before submission. | BR-02 | Must |
| FR-03 | The system shall **block submission** of an application that is missing mandatory documents, and explain which are missing. | BR-02 | Must |
| FR-04 | The system shall send **automatic reminders** (email/SMS) for outstanding documents after 2 and 5 business days. | BR-02 | Should |
| FR-05 | Underwriters with the "Senior" credit grade shall approve loans **up to €250k** under delegated authority. Loans above go to a **daily credit forum**. | BR-04 | Must |
| FR-06 | The system shall route each application to an underwriter using **round-robin weighted by open caseload and grade**, with manual override and a logged reason. | BR-05 | Should |
| FR-07 | The system shall show application **status** in 6 stages (Received, Documents, Checks, Assessment, Decision, Funding) to customers, brokers and RMs. | BR-06 | Must |
| FR-08 | The system shall **notify the customer** by email/SMS at each stage change. | BR-06 | Must |
| FR-09 | With customer consent, the system shall **import 12 months of bank transactions (open banking)** and accounting data into the spreading tool. | BR-03 | Should |
| FR-10 | The system shall **calculate key ratios** (DSCR, leverage, interest cover) automatically from imported data. | BR-03 | Should |
| FR-11 | Every decision shall record the decision-maker, authority level, timestamp and rationale. | BR-07 | Must |
| FR-12 | The system shall record a **timestamped event** for each process step (application, documents, KYC, assessment, decision, offer, funding). | BR-08 | Must |
| FR-13 | A dashboard shall show daily pipeline, time to decision vs SLA, first-time-complete rate and withdrawals. | BR-08 | Should |
| FR-14 | An automated decision engine for applications **≤ €50k** that meet policy rules. | BR-01 | **Could** (phase 2) |

## 4. Non-functional requirements
| ID | Category | Requirement |
|---|---|---|
| NFR-01 | Availability | Customer portal available 99.5% (excluding planned maintenance). |
| NFR-02 | Performance | Document upload ≤ 10 seconds for a 10 MB file; status page loads ≤ 2 seconds. |
| NFR-03 | Security | Documents encrypted in transit and at rest; role-based access; MFA for staff and customers. |
| NFR-04 | Data protection | GDPR compliant: consent captured for open banking, retention schedule applied, data subject requests supported. |
| NFR-05 | Accessibility | Customer screens meet WCAG 2.1 AA. |
| NFR-06 | Auditability | All status changes and decisions kept for 7 years and retrievable for audit within 1 business day. |
| NFR-07 | Usability | A first-time SME customer can complete an application in ≤ 20 minutes (tested with 5 users). |

## 5. Business rules
| ID | Rule |
|---|---|
| BRL-01 | Delegated authority: Underwriter ≤ €100k; Senior Underwriter ≤ €250k; daily credit forum ≤ €750k. |
| BRL-02 | The "5 business days" SLA clock starts when the application is **complete**, and pauses only while waiting on the customer for information requested **after** submission. |
| BRL-03 | KYC/AML must be completed **before** a credit decision is communicated. |
| BRL-04 | A declined application must receive written reasons within 5 business days (SME Lending Regulations). |
| BRL-05 | Secured loans require security perfection before funding. |

## 6. Data requirements
| Data | Source | Used for |
|---|---|---|
| Application data (amount, purpose, entity, sector) | Origination portal | Checklist, routing, MI |
| Documents (accounts, bank statements, ID, tax clearance) | Upload portal | KYC, assessment |
| Bank transactions (12 months) | Open banking API (with consent) | Automated spreading |
| Process events (case, activity, timestamp, user) | Workflow engine | KPI dashboard, process mining |

## 7. Assumptions and dependencies
* Credit policy (risk appetite, pricing) is unchanged.
* Chief Credit Officer approves the revised delegated authority (BRL-01), as a 3-month pilot with quality sampling.
* The open-banking provider contract is in place before phase 2.

## 8. Out of scope
Loan pricing, collections, corporate lending above €750k, replacement of the core banking system.

## 9. Sign-off
| Name / role | Decision | Date |
|---|---|---|
| Director of SME Banking | ☐ Approved | |
| Chief Credit Officer | ☐ Approved | |
| Head of Compliance | ☐ Approved | |
| Head of Digital | ☐ Approved | |
