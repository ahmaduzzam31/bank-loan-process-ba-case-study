#!/usr/bin/env bash
# Rebuild everything: simulated event log -> analysis -> business case -> dashboard.
set -euo pipefail
cd "$(dirname "$0")"
python src/generate_event_log.py
jupyter nbconvert --to notebook --execute --inplace notebooks/process_analysis.ipynb
python src/build_business_case.py
python src/build_dashboard.py
