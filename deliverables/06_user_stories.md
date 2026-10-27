# 06 · Product Backlog: Epics and User Stories

Format: *As a [role], I want [capability], so that [benefit].* Acceptance criteria are in **Given / When / Then**
(Gherkin). Story points use the Fibonacci scale. Priority uses MoSCoW.

## Epics
| Epic | Goal | Requirements | Phase |
|---|---|---|---|
| **E1 Complete first time** | Applications arrive with all mandatory documents | BR-02 · FR-01 to FR-04 | 1 |
| **E2 Faster decisions** | Remove the weekly committee wait; balance workload | BR-01, BR-04, BR-05 · FR-05, FR-06 | 1 |
| **E3 Transparency** | Customers, brokers and RMs always know the status | BR-06 · FR-07, FR-08 | 1 |
| **E4 Automated financials** | No re-keying of financial statements | BR-03 · FR-09, FR-10 | 2 |
| **E5 Control & insight** | Audit trail and a live KPI dashboard | BR-07, BR-08 · FR-11 to FR-13 | 1 |

## Sprint 1 to 3 backlog (phase 1)

### US-01 · Personalised document checklist (E1, Must, 5 pts)
**As an** SME customer, **I want** to see exactly which documents I need for my loan before I start,
**so that** I don't have to send documents twice.

```gherkin
Scenario: Checklist for a secured loan to a limited company
  Given I am applying for a €180,000 secured loan for premises
  And my business is a limited company
  When I reach the "Documents" step
  Then I see a checklist including 2 years of filed accounts, 6 months of bank statements,
       management accounts, tax clearance, directors' ID and property valuation
  And each item shows an example and the accepted file types

Scenario: Smaller unsecured loan needs fewer documents
  Given I am applying for a €25,000 unsecured working capital loan
  When I reach the "Documents" step
  Then the property valuation and management accounts are not requested
```

### US-02 · Block incomplete submissions (E1, Must, 3 pts)
**As a** relationship manager, **I want** the system to stop applications being submitted without mandatory documents,
**so that** I stop chasing customers after submission.

```gherkin
Scenario: Missing mandatory document
  Given my checklist has 6 mandatory items and I have uploaded 5
  When I press "Submit application"
  Then the application is not submitted
  And I see the message "1 document missing: Tax clearance certificate"

Scenario: Complete application
  Given all mandatory items are uploaded and pass validation
  When I press "Submit application"
  Then the status changes to "Received"
  And the 5-business-day decision SLA clock starts
```

### US-03 · Document reminders (E1, Should, 2 pts)
**As an** SME customer, **I want** a reminder when I have unfinished document uploads, **so that** my application doesn't stall.
```gherkin
Scenario: Reminder after 2 business days
  Given I saved an application with 2 outstanding documents on Monday
  When Wednesday 09:00 arrives and the documents are still outstanding
  Then I receive an SMS and email listing the 2 documents with an upload link
```

### US-04 · Senior delegated authority up to €250k (E2, Must, 3 pts)
**As a** senior underwriter, **I want** to approve loans up to €250k myself, **so that** good customers don't wait a week for committee.
```gherkin
Scenario: Senior underwriter approves within authority
  Given I hold the "Senior Underwriter" grade
  And the application is for €220,000 and within credit policy
  When I record an "Approve" decision with rationale
  Then the decision is final without referral
  And the audit log stores my user ID, grade, amount, timestamp and rationale

Scenario: Above authority goes to the daily forum
  Given the application is for €400,000
  When I submit my recommendation
  Then it is queued for the next daily credit forum (cut-off 12:00)
  And a decision is recorded within 1 business day
```

### US-05 · Capacity-based allocation (E2, Should, 5 pts)
**As a** credit team lead, **I want** new applications assigned automatically by open caseload and complexity,
**so that** work is spread fairly and nothing sits unassigned.
```gherkin
Scenario: Route to the least-loaded eligible underwriter
  Given UW03 has 6 open cases and UW01 has 14
  And both are eligible for a €90,000 application
  When the application completes KYC pre-checks
  Then it is assigned to UW03

Scenario: Manual override is logged
  Given an application is assigned to UW03
  When the team lead reassigns it to UW01
  Then a reason must be selected and the change is written to the audit log
```

### US-06 · Status tracker (E3, Must, 5 pts)
**As an** SME customer, **I want** to see where my application is, **so that** I don't need to call my RM.
```gherkin
Scenario: Status visible after submission
  Given my application was submitted
  When I log in to the portal
  Then I see the 6 stages with the current stage highlighted
  And the expected decision date based on the SLA
```

### US-07 · Stage-change notifications (E3, Must, 3 pts)
**As a** broker, **I want** an email when my client's application changes stage, **so that** I can keep my client informed.
```gherkin
Scenario: Decision notification
  Given I introduced application SME-104233
  When the status changes to "Decision: approved"
  Then I receive an email within 5 minutes with the decision and the RM's contact details
```

### US-08 · Pipeline KPI dashboard (E5, Should, 8 pts)
**As the** Director of SME Banking, **I want** a daily dashboard of the pipeline, **so that** I can spot delays before customers walk away.
```gherkin
Scenario: SLA breach visibility
  Given 12 applications have been complete for more than 4 business days without a decision
  When I open the dashboard
  Then they are listed under "At risk of SLA breach" with owner and days waiting
```

## Phase 2 backlog (summary)
| ID | Story | Epic | Priority | Points |
|---|---|---|---|---|
| US-09 | As a customer I want to connect my business bank account (open banking) so that I don't upload statements | E4 | Should | 8 |
| US-10 | As an underwriter I want financials imported from accounting software so that I don't re-key accounts | E4 | Should | 13 |
| US-11 | As an underwriter I want DSCR, leverage and interest cover calculated automatically | E4 | Should | 5 |
| US-12 | As a customer applying for ≤ €50k I want an instant decision when I meet policy rules | E2 | Could | 13 |

## Definition of Ready / Done
* **Ready:** story has acceptance criteria, dependencies identified, sized by the team, Compliance consulted if it touches KYC.
* **Done:** acceptance criteria pass in UAT, audit events logged (FR-11/FR-12), accessibility checked, documentation and training notes updated.
