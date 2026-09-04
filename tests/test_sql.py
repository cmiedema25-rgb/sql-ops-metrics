import json
from pathlib import Path

from sql_ops_metrics.cli import main
from sql_ops_metrics.db import connect, load_csv
from sql_ops_metrics.queries import run_query
from sql_ops_metrics.report import build_report

ROOT = Path(__file__).resolve().parents[1]


def test_load_and_delayed_by_customer() -> None:
    conn = connect()
    assert load_csv(conn, ROOT / "data/shipments.csv") == 10
    rows = run_query(conn, "delayed_by_customer")
    assert rows[0]["customer"] == "Northwind"
    assert rows[0]["delayed_loads"] == 3


def test_lane_delay_rate() -> None:
    conn = connect()
    load_csv(conn, ROOT / "data/shipments.csv")
    lanes = {row["lane"]: row for row in run_query(conn, "lane_delay_rate")}
    assert lanes["Austin->Seattle"]["delayed"] == 2
    assert lanes["Austin->Seattle"]["loads"] == 3


def test_report_and_cli(tmp_path: Path) -> None:
    report = build_report(ROOT / "data/shipments.csv")
    assert report["headline"]["delayed_loads"] == 6
    assert report["passed"]
    dest = tmp_path / "sql-ops-report.json"
    assert main(["report", "--csv", str(ROOT / "data/shipments.csv"), "--report", str(dest)]) == 0
    payload = json.loads(dest.read_text(encoding="utf-8"))
    assert payload["rows_loaded"] == 10
