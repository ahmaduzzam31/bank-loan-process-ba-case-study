# Executive Summary: SME Loan Origination Redesign

**To:** Director of SME Banking (Sponsor), Chief Credit Officer
**Bank:** Harbour Bank Ireland (fictional). Process data simulated.

## The problem
SME customers wait a **median of 16 days for a credit decision** and **28 days for funds**. Only **2%** get a decision
within a week. **27% of applicants withdraw**, which is **€162M of requested lending a year**, much of it to faster fintech lenders.

## What the analysis found (12 months, 5,995 applications, 70,399 process events)
1. **41% of applications arrive incomplete.** Each missing-documents loop adds about **6 days**, and withdrawal rises
   from 22% to 47% with repeated requests.
2. **Loans of €100k or more wait a median 7 days for a weekly credit committee**, against same-day delegated decisions.
3. **Speed is revenue:** even *approved* customers are lost, **16%** when decided in under 10 days and **39%** after 25+ days.
4. **Underwriters re-key every set of accounts** (about 4,200 hours a year), and two underwriters carry 45 to 56% more than an even share.
5. Customers get **no status updates**: 61% of surveyed applicants named this as their top complaint.

## Recommendation
| Option | NPV (5 yrs) | Payback | Verdict |
|---|---|---|---|
| A. Do nothing | €0 | n/a | Keeps losing a quarter of applicants |
| **B. Process quick wins:** checklist + digital upload, delegated authority to €250k, daily credit forum, workload routing, status tracking | **€3.2M** | **about 1 year** | **Approve now** |
| C. B + digital origination (open banking, automated spreading, instant decisions ≤ €50k) | €2.2M | 2.8 years | **Phase 2**, once B proves the withdrawal reduction |

Benefits count only **50%** of the modelled extra loans. Option B stays positive even at 25%.

## Decisions requested
1. Approve Option B budget (€450k one-off, €120k a year).
2. Chief Credit Officer to approve a 3-month **pilot of €250k senior delegated authority** with quality sampling.
3. Approve BRD v1.0 ([deliverables/04](../deliverables/04_business_requirements_document.md)).
