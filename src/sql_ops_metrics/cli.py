"""CLI: sql-ops report | query."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from sql_ops_metrics.db import connect, load_csv
from sql_ops_metrics.queries import run_query
from sql_ops_metrics.report import build_report, write_report


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="sql-ops")
    sub = parser.add_subparsers(dest="command", required=True)
    rep = sub.add_parser("report", help="Run all analytics queries and write JSON evidence")
    rep.add_argument("--csv", default=str(_repo_root() / "data" / "shipments.csv"))
    rep.add_argument("--report", default=str(_repo_root() / "evidence" / "sql-ops-report.json"))
    q = sub.add_parser("query", help="Run one named query")
    q.add_argument("name")
    q.add_argument("--csv", default=str(_repo_root() / "data" / "shipments.csv"))
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "query":
        conn = connect()
        load_csv(conn, args.csv)
        print(json.dumps(run_query(conn, args.name), indent=2))
        return 0
    report = build_report(args.csv)
    dest = write_report(report, args.report)
    print(
        json.dumps(
            {
                "rows_loaded": report["rows_loaded"],
                "headline": report["headline"],
                "passed": report["passed"],
                "report": str(dest),
            },
            indent=2,
        )
    )
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
