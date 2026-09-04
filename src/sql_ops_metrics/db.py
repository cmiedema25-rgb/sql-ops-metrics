"""Load fixture CSV into an in-memory (or file) SQLite database."""

from __future__ import annotations

import csv
import sqlite3
from pathlib import Path

SCHEMA = """
CREATE TABLE shipments (
  load_id TEXT PRIMARY KEY,
  customer TEXT NOT NULL,
  origin TEXT NOT NULL,
  destination TEXT NOT NULL,
  status TEXT NOT NULL,
  delay_hours INTEGER NOT NULL,
  revenue REAL NOT NULL
);
"""


def connect(path: str | Path | None = None) -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:" if path is None else str(path))
    conn.row_factory = sqlite3.Row
    return conn


def load_csv(conn: sqlite3.Connection, csv_path: str | Path) -> int:
    conn.executescript(SCHEMA)
    rows = list(csv.DictReader(Path(csv_path).read_text(encoding="utf-8").splitlines()))
    conn.executemany(
        """
        INSERT INTO shipments
        (load_id, customer, origin, destination, status, delay_hours, revenue)
        VALUES (:load_id, :customer, :origin, :destination, :status, :delay_hours, :revenue)
        """,
        [
            {
                **row,
                "delay_hours": int(row["delay_hours"]),
                "revenue": float(row["revenue"]),
            }
            for row in rows
        ],
    )
    conn.commit()
    return len(rows)
