"""Build retained JSON evidence for SQL query results."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from sql_ops_metrics.db import connect, load_csv
from sql_ops_metrics.queries import QUERIES, run_all


def build_report(csv_path: str | Path) -> dict[str, Any]:
    conn = connect()
    n = load_csv(conn, csv_path)
    results = run_all(conn)
    delayed_n = next(row["n"] for row in results["status_mix"] if row["status"] == "delayed")
    return {
        "rows_loaded": n,
        "queries": list(QUERIES),
        "sql": QUERIES,
        "results": results,
        "headline": {
            "delayed_loads": delayed_n,
            "customers_with_delay": len(results["delayed_by_customer"]),
            "lanes": len(results["lane_delay_rate"]),
        },
        "passed": n > 0 and delayed_n > 0,
    }


def write_report(report: dict[str, Any], dest: str | Path) -> Path:
    path = Path(dest)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return path
