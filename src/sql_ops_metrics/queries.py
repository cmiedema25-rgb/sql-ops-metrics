"""Named analytics queries with retained SQL text."""

from __future__ import annotations

import sqlite3
from typing import Any

QUERIES: dict[str, str] = {
    "delayed_by_customer": """
        SELECT customer,
               COUNT(*) AS delayed_loads,
               ROUND(AVG(delay_hours), 2) AS avg_delay_hours,
               ROUND(SUM(revenue), 2) AS revenue_at_risk
        FROM shipments
        WHERE status = 'delayed'
        GROUP BY customer
        ORDER BY delayed_loads DESC, customer
    """,
    "lane_delay_rate": """
        SELECT origin || '->' || destination AS lane,
               COUNT(*) AS loads,
               SUM(CASE WHEN status = 'delayed' THEN 1 ELSE 0 END) AS delayed,
               ROUND(
                 1.0 * SUM(CASE WHEN status = 'delayed' THEN 1 ELSE 0 END) / COUNT(*),
                 4
               ) AS delay_rate
        FROM shipments
        GROUP BY origin, destination
        ORDER BY delay_rate DESC, lane
    """,
    "status_mix": """
        SELECT status, COUNT(*) AS n, ROUND(SUM(revenue), 2) AS revenue
        FROM shipments
        GROUP BY status
        ORDER BY n DESC
    """,
}


def run_query(conn: sqlite3.Connection, name: str) -> list[dict[str, Any]]:
    if name not in QUERIES:
        raise KeyError(f"unknown query: {name}")
    cur = conn.execute(QUERIES[name])
    return [dict(row) for row in cur.fetchall()]


def run_all(conn: sqlite3.Connection) -> dict[str, list[dict[str, Any]]]:
    return {name: run_query(conn, name) for name in QUERIES}
