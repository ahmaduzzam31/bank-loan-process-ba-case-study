# 07 · Business Case and Options Appraisal

The full model with live formulas is in **[07_business_case.xlsx](07_business_case.xlsx)** (Inputs → Cash_Flows → Summary).
Volumes come from the [process analysis](../notebooks/process_analysis.ipynb). Financial assumptions are stated on the
Inputs sheet and can be changed.

## 1. Options
| Option | Description | One-off cost | Run cost / yr |
|---|---|---|---|
| **A. Do nothing** | Keep the current process | €0 | €0 |
| **B. Process quick wins** | Checklist + digital upload, delegated authority to €250k, daily credit forum, capacity-based allocation, status tracking | €450k | €120k |
| **C. Digital origination + quick wins** | Option B plus open-banking data capture, automated spreading and an automated decision engine for ≤ €50k | €2.4M (over 2 years) | €380k |

## 2. Benefits logic
* **Revenue:** extra funded loans (from fewer withdrawals) × average loan (€91k) × 1.8% net margin × 3-year average life.
  Only **50% of modelled extra loans are counted** (realisation factor).
* **Efficiency:** underwriter re-keying time saved (C only) and RM document-chasing time saved (B: −50%, C: −80% requests).
* **Not counted** (upside): better customer satisfaction, broker retention, lower operational risk from fewer re-keying errors.

## 3. Results (5 years, 8% discount rate)
| Option | NPV | IRR | Payback | Extra loans / yr counted |
|---|---|---|---|---|
| A. Do nothing | €0 | n/a | n/a | 0 |
| **B. Quick wins** | **€3.2M** | **154%** | **< 1 year** | 228 |
| C. Digital + quick wins | €2.2M | 35% | 2.8 years | 343 |

### Sensitivity: NPV by benefit realisation factor
| Realisation | 25% | 50% (base) | 75% | 100% |
|---|---|---|---|---|
| B. Quick wins | €1.3M | €3.2M | €5.2M | €7.2M |
| C. Digital + quick wins | **−€0.4M** | €2.2M | €4.8M | €7.4M |

## 4. Recommendation
**Approve Option B now.** It pays back within a year, stays positive even if only a quarter of the benefit is
achieved, and needs no major technology build.

**Prepare Option C as phase 2.** It adds value but carries more delivery risk and is negative at low realisation.
Start it once phase 1 has **proven the withdrawal reduction**. Phase 1's dashboard (FR-13) gives the evidence, and
phase 1 benefits help fund phase 2.

## 5. Key risks to the benefits
| Risk | Effect on case | Mitigation |
|---|---|---|
| Withdrawal rate does not fall as modelled | Lower revenue benefit | 50% realisation already applied; track monthly from go-live |
| Credit quality worsens with higher delegated limits | Higher credit losses | 3-month pilot, 10% post-decision quality sampling, Chief Credit Officer review |
| Phase 2 integration overruns | Cost overrun on C | Fixed-price vendor contract; gate C on phase 1 results |
