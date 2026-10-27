"""Simulate an SME loan origination event log for Harbour Bank Ireland (a fictional bank).

One row per process event, the format process-mining tools expect: case_id, activity, timestamp, resource.
The current ("as-is") process has the pain points the case study investigates:
  * ~40% of applications arrive incomplete and loop through document requests
  * re-keying of financial statements by underwriters
  * loans of €100k or more wait for a credit committee that meets once a week
  * customers withdraw more often the longer they wait

Outputs (data/): applications.csv, event_log.csv
"""
from pathlib import Path

import numpy as np
import pandas as pd

SEED = 17
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data"
rng = np.random.default_rng(SEED)

N_CASES = 6_000
START, END = pd.Timestamp("2025-10-01"), pd.Timestamp("2026-09-30")
CHANNELS = {"Online": 0.46, "Branch": 0.34, "Broker": 0.20}
SECTORS = {"Retail": 0.22, "Hospitality": 0.16, "Construction": 0.15, "Agri-food": 0.14,
           "Professional services": 0.13, "Manufacturing": 0.11, "Healthcare": 0.09}
PURPOSES = {"Working capital": 0.38, "Equipment": 0.27, "Premises": 0.15, "Expansion": 0.20}
COMMITTEE_LIMIT = 100_000
TEAM = {"Relationship manager": [f"RM{i:02d}" for i in range(1, 15)],
        "Credit underwriter": [f"UW{i:02d}" for i in range(1, 9)],
        "Compliance analyst": [f"KYC{i:02d}" for i in range(1, 5)],
        "Credit committee": ["CC"],
        "Legal & security": [f"LS{i:02d}" for i in range(1, 4)],
        "Loan operations": [f"OPS{i:02d}" for i in range(1, 5)]}
# Underwriter workload is uneven: two senior underwriters get the complex cases
UW_WEIGHTS = np.array([0.20, 0.18, 0.12, 0.11, 0.11, 0.10, 0.09, 0.09])


def business_hours_later(ts: pd.Timestamp, hours: float) -> pd.Timestamp:
    """Advance a timestamp by working hours (Mon-Fri, 09:00-17:30)."""
    t = ts
    remaining = hours
    while remaining > 0:
        if t.weekday() >= 5:
            t = (t + pd.Timedelta(days=7 - t.weekday())).normalize() + pd.Timedelta(hours=9)
            continue
        day_end = t.normalize() + pd.Timedelta(hours=17.5)
        if t < t.normalize() + pd.Timedelta(hours=9):
            t = t.normalize() + pd.Timedelta(hours=9)
        avail = (day_end - t).total_seconds() / 3600
        if avail <= 0:
            t = t.normalize() + pd.Timedelta(days=1, hours=9)
            continue
        step = min(avail, remaining)
        t += pd.Timedelta(hours=step)
        remaining -= step
        if remaining > 0:
            t = t.normalize() + pd.Timedelta(days=1, hours=9)
    return t


def wait_days(ts: pd.Timestamp, days: float) -> pd.Timestamp:
    return business_hours_later(ts, days * 8.5)


def next_committee(ts: pd.Timestamp) -> pd.Timestamp:
    """Credit committee sits Thursdays 14:00; papers must be in by Tuesday 17:00."""
    d = ts.normalize()
    cutoff_ok = ts.weekday() < 1 or (ts.weekday() == 1 and ts.hour < 17)
    days_to_thu = (3 - ts.weekday()) % 7
    if not cutoff_ok or days_to_thu == 0:
        days_to_thu = days_to_thu + 7 if days_to_thu < 3 or not cutoff_ok else days_to_thu
    return d + pd.Timedelta(days=days_to_thu, hours=14)


def pick(d: dict):
    return rng.choice(list(d), p=list(d.values()))


def simulate_case(i: int):
    case = f"SME-{100000 + i}"
    channel, sector, purpose = pick(CHANNELS), pick(SECTORS), pick(PURPOSES)
    amount = float(np.clip(np.round(np.exp(rng.normal(np.log(70_000), 0.75)) / 1000) * 1000, 10_000, 750_000))
    secured = amount >= 150_000 or purpose == "Premises" or rng.random() < 0.15
    t = START + pd.Timedelta(seconds=int(rng.integers(0, int((END - START).total_seconds()))))
    t = business_hours_later(t, 0.1)
    rm = rng.choice(TEAM["Relationship manager"])
    ev = []

    def log(activity, ts, resource, role):
        ev.append((case, activity, ts, resource, role))

    log("Application submitted", t, "CUSTOMER" if channel == "Online" else rm, "Customer" if channel == "Online" else "Relationship manager")
    t = wait_days(t, rng.gamma(1.5, 0.6))
    log("Application reviewed for completeness", t, rm, "Relationship manager")

    # Document chase loop: incomplete applications (worse on paper channels)
    p_incomplete = {"Online": 0.32, "Branch": 0.45, "Broker": 0.50}[channel]
    loops = 0
    while rng.random() < (p_incomplete if loops == 0 else 0.38) and loops < 4:
        loops += 1
        log("Missing documents requested", t, rm, "Relationship manager")
        t = wait_days(t, rng.gamma(2.2, 1.9))           # customer gathers documents
        log("Documents received", t, "CUSTOMER", "Customer")
    elapsed = (t - ev[0][2]).days
    if rng.random() < 0.02 + 0.035 * loops + 0.004 * elapsed:
        log("Application withdrawn", wait_days(t, 0.5), "CUSTOMER", "Customer")
        return ev, dict(case_id=case, channel=channel, sector=sector, purpose=purpose, amount_eur=amount,
                        secured=secured, doc_loops=loops, outcome="Withdrawn")

    log("KYC/AML checks started", wait_days(t, rng.gamma(1.4, 0.7)), rng.choice(TEAM["Compliance analyst"]), "Compliance analyst")
    t = wait_days(ev[-1][2], rng.gamma(2.0, 0.6))
    log("KYC/AML checks completed", t, ev[-1][3], "Compliance analyst")

    uw = rng.choice(TEAM["Credit underwriter"], p=UW_WEIGHTS)
    t = wait_days(t, rng.gamma(2.0, 1.4))               # queue for an underwriter
    log("Credit assessment started", t, uw, "Credit underwriter")
    t = business_hours_later(t, rng.gamma(3.0, 1.6))     # manual re-keying of financials
    log("Financials re-keyed into spreading tool", t, uw, "Credit underwriter")
    t = wait_days(t, rng.gamma(2.0, 1.0 + amount / 400_000))
    log("Credit assessment completed", t, uw, "Credit underwriter")

    risk = rng.normal(0, 1) - 0.15 * loops + (0.3 if sector in ("Healthcare", "Professional services") else 0) \
        - (0.35 if sector in ("Hospitality", "Construction") else 0)
    if amount >= COMMITTEE_LIMIT:
        t = next_committee(t)
        log("Credit committee decision", t, "CC", "Credit committee")
    else:
        t = wait_days(t, rng.gamma(1.2, 0.5))
        log("Delegated authority decision", t, uw, "Credit underwriter")

    elapsed = (t - ev[0][2]).days
    if risk < -1.35:
        log("Application declined", wait_days(t, 0.3), rm, "Relationship manager")
        return ev, dict(case_id=case, channel=channel, sector=sector, purpose=purpose, amount_eur=amount,
                        secured=secured, doc_loops=loops, outcome="Declined")
    # Some customers have already gone elsewhere by the time the decision arrives
    if rng.random() < 0.01 + 0.0075 * elapsed:
        log("Application withdrawn", wait_days(t, 0.5), "CUSTOMER", "Customer")
        return ev, dict(case_id=case, channel=channel, sector=sector, purpose=purpose, amount_eur=amount,
                        secured=secured, doc_loops=loops, outcome="Withdrawn")

    t = wait_days(t, rng.gamma(1.6, 0.7))
    log("Loan offer issued", t, rm, "Relationship manager")
    t = wait_days(t, rng.gamma(1.8, 1.6))
    if rng.random() < 0.06 + 0.004 * elapsed:
        log("Offer declined by customer", t, "CUSTOMER", "Customer")
        return ev, dict(case_id=case, channel=channel, sector=sector, purpose=purpose, amount_eur=amount,
                        secured=secured, doc_loops=loops, outcome="Withdrawn")
    log("Offer accepted", t, "CUSTOMER", "Customer")

    if secured:
        ls = rng.choice(TEAM["Legal & security"])
        t = wait_days(t, rng.gamma(2.0, 1.5))
        log("Security & legal review started", t, ls, "Legal & security")
        t = wait_days(t, rng.gamma(3.0, 2.0))
        log("Security perfected", t, ls, "Legal & security")
    t = wait_days(t, rng.gamma(1.5, 0.8))
    log("Loan funded", t, rng.choice(TEAM["Loan operations"]), "Loan operations")
    return ev, dict(case_id=case, channel=channel, sector=sector, purpose=purpose, amount_eur=amount,
                    secured=secured, doc_loops=loops, outcome="Funded")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    events, cases = [], []
    for i in range(N_CASES):
        ev, info = simulate_case(i)
        events.extend(ev)
        cases.append(info)
    log = pd.DataFrame(events, columns=["case_id", "activity", "timestamp", "resource", "role"])
    log = log.sort_values(["case_id", "timestamp"]).reset_index(drop=True)
    apps = pd.DataFrame(cases)
    first = log.groupby("case_id").timestamp.min().rename("submitted_at")
    apps = apps.merge(first, on="case_id").sort_values("submitted_at")
    apps = apps[apps.submitted_at <= END]
    log = log[log.case_id.isin(apps.case_id)]
    log.to_csv(OUT / "event_log.csv", index=False)
    apps.to_csv(OUT / "applications.csv", index=False)
    print(f"{len(apps):,} applications | {len(log):,} events | outcomes: {apps.outcome.value_counts().to_dict()}")


if __name__ == "__main__":
    main()
