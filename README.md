# SQL Ops Metrics

[![CI](https://github.com/cmiedema25-rgb/sql-ops-metrics/actions/workflows/ci.yml/badge.svg)](https://github.com/cmiedema25-rgb/sql-ops-metrics/actions/workflows/ci.yml)

Small SQLite analytics CLI: load a shipment board CSV, run delay metrics queries, and keep the exact SQL + results in a report. Stdlib only.

## Install

```bash
python -m pip install -e '.[dev]'
make verify
```

## Usage

```bash
make report   # writes evidence/sql-ops-report.json
```

Includes delayed-by-customer and lane delay-rate style queries. Ships with a tiny synthetic CSV for local runs — point it at your own export for real boards.

## License

MIT
