# SQL Ops Metrics

[![CI](https://github.com/cmiedema25-rgb/sql-ops-metrics/actions/workflows/ci.yml/badge.svg)](https://github.com/cmiedema25-rgb/sql-ops-metrics/actions/workflows/ci.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-3776AB.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Tiny **SQLite analytics CLI** that loads a synthetic shipment board and retains
exact SQL + result evidence. Offline CI — stdlib only.

## Reviewer proof

| Outcome | Evidence | Reproduce |
| --- | --- | --- |
| 10 rows loaded; 6 delayed | [`evidence/sql-ops-report.json`](evidence/sql-ops-report.json) | `make report` |
| Delayed-by-customer + lane delay rate queries | same report (`sql` + `results`) | `make report` |

```bash
python -m pip install -e '.[dev]'
make verify
```

## Skills

- **SQL:** GROUP BY, CASE aggregates, delay-rate ratios on SQLite.
- **Python:** CLI, pytest, Ruff, Actions.

## Limitations

Synthetic 10-row CSV only — not a warehouse, warehouse dialect, or cloud BI ROI.
