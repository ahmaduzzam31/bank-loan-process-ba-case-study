# 03 · Current-State (AS-IS) Process

> Fictional case study. Figures come from the simulated event log ([process analysis notebook](../notebooks/process_analysis.ipynb),
> [SQL](../sql)).

## 1. AS-IS process map (swimlanes)
```mermaid
flowchart LR
    subgraph CUS[Customer]
        A1([Submit application<br/>online, branch or broker])
        A4[Gather and send<br/>missing documents]
        A9{Accept offer?}
    end
    subgraph RM[Relationship Manager]
        A2[Review application<br/>for completeness]
        A3{Complete?}
        A8[Issue loan offer]
    end
    subgraph KYC[Compliance]
        A5[KYC / AML checks]
    end
    subgraph UW[Credit Underwriter]
        A6[Re-key financials into<br/>spreading tool]
        A7[Credit assessment]
        D1{Amount below €100k?}
        A7b[Delegated decision]
    end
    subgraph CC[Credit Committee]
        A7c[Weekly committee<br/>Thursdays]
    end
    subgraph LS[Legal & Ops]
        A10[Security & legal<br/>if secured]
        A11([Loan funded])
    end
    A1 --> A2 --> A3
    A3 -- "No (41%)" --> A4 --> A2
    A3 -- Yes --> A5 --> A6 --> A7 --> D1
    D1 -- Yes --> A7b --> A8
    D1 -- "No (33%)" --> A7c --> A8
    A8 --> A9
    A9 -- Yes --> A10 --> A11
    A9 -- No --> X([Lost to competitor])

    classDef pain fill:#f8d7d7,stroke:#d03b3b,color:#0b0b0b
    class A4,A6,A7c pain
```
Red steps are the main pain points.

## 2. Baseline performance
| KPI | Value |
|---|---|
| Applications per year | 5,995 |
| Funded / withdrawn / declined | 61.6% / **27.2%** / 11.2% |
| Median days to credit decision | **16.2** |
| Median days to funding | **28.0** |
| Decisions within 7 days | **2.1%** |
| Complete at first submission | **59%** |
| Requested lending withdrawn | **€161.9M** |
| Distinct process variants (top 8 cover only 59%) | High variability: the "happy path" is just 20% of cases |

## 3. Pain points with evidence
| # | Pain point (stakeholder voice) | Evidence from data | Impact |
|---|---|---|---|
| P1 | *"We chase documents constantly"* (RMs) | 41% incomplete on arrival; 3,883 document requests a year; median **+6 days per loop**; withdrawal rises from 22% (0 loops) to 47% (3+ loops) | Biggest single source of delay (22k case-days) |
| P2 | *"Big loans wait for committee"* (Underwriters) | ≥ €100k loans wait a median **7.1 days** (P90 13 days) for the weekly committee, against 0.3 days for delegated decisions | 33% of applications delayed by a week |
| P3 | *"I re-type every set of accounts"* (Underwriters) | Manual spreading about 45 min per case × 5,642 = **~4,200 hours a year**. Assessment stage = 19k case-days | Error risk, slow decisions |
| P4 | *"Two of us get all the hard files"* (Underwriters) | UW01 and UW02 carry **+56% and +45%** more than an even share | Queue of 3.2 days (median) after KYC |
| P5 | *"I don't know where my application is"* (61% of surveyed customers) | No status notifications in any channel | Customers shop around |
| P6 | *"We lose them even after approval"* (Sponsor) | Approved customers lost: **16%** when decided in < 10 days, **39%** at 25+ days | Approved, profitable lending lost |

## 4. Root cause analysis
```mermaid
mindmap
  root((Slow decisions<br/>and lost customers))
    Process
      No upfront document checklist
      Weekly committee batch
      Sequential hand-offs
    People
      Uneven case allocation
      Approval limits too low for experienced underwriters
    Technology
      No document upload portal
      Manual re-keying of financials
      No status tracking for customers
    Policy
      Committee threshold set at €100k in 2014, never reviewed
      No turnaround SLA
```

### 5 Whys: "Why do approved customers withdraw?"
1. **Why?** They accepted a competitor's offer while waiting.
2. **Why were they waiting?** The decision took a median of 16 days.
3. **Why 16 days?** Files bounce back for missing documents and large loans wait for a weekly committee.
4. **Why are files incomplete?** Customers aren't told upfront exactly what's needed, and paper channels have no validation.
5. **Why is there no upfront list or validation?** The process was designed for branch-only, paper applications. → **Root cause: a process designed for paper, not for digital or speed.**
