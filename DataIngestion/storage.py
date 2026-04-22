"""SQLite persistence layer for Steam case price data.

All functions in this module operate on a single SQLite file located at
`DB_PATH`. The database stores one row per (case_name, timestamp) pair in the
`case_prices` table.

Schema (for reference while you implement):
    case_prices
      - case_name  TEXT     -- human-readable name, e.g. "KiloWatt Case"
      - timestamp  TEXT     -- ISO 8601, e.g. "2026-04-21 14:00:00"
      - price      REAL
      - volume     INTEGER
      - PRIMARY KEY (case_name, timestamp)
"""

from __future__ import annotations

import sqlite3
from datetime import datetime
from pathlib import Path


DB_PATH: Path = Path(__file__).parent / "market.db"


def init_db(db_path: Path = DB_PATH) -> None:
    """Create the `case_prices` table if it does not already exist.

    Safe to call on every run (idempotent). Should open a connection to
    `db_path`, execute a CREATE TABLE IF NOT EXISTS statement for the schema
    described at the top of this module, commit, and close.

    Hints:
      - `sqlite3.connect(db_path)` accepts a Path or str.
      - The composite primary key syntax is `PRIMARY KEY (col_a, col_b)` as a
        separate line inside the CREATE TABLE parens.
      - Wrap the connection in a `with` block to auto-commit on success.
    """

    with sqlite3.connect(db_path) as connection:

      c = connection.cursor()

      schema_sql = """CREATE TABLE IF NOT EXISTS case_prices( 
          name TEXT NOT NULL,
          date TEXT NOT NULL,
          price REAL NOT NULL,
          volume INT,
          PRIMARY KEY (name, date)
      );"""

      c.execute(schema_sql)

    connection.close()



def save_case_data(
    case_name: str,
    rows: list[list],
    db_path: Path = DB_PATH,
) -> None:
    """Persist one case's hourly price/volume rows to the database.

    Args:
        case_name: Clean, human-readable case name (no URL encoding).
        rows:      List of [datetime, price, volume] entries as produced by
                   the scraper in main.py.
        db_path:   Location of the SQLite file.

    Behavior:
      - Convert each row's `datetime` to an ISO 8601 string before writing.
      - Use a parameterized INSERT OR REPLACE so re-scraped hours overwrite
        previously stored values for the same (case_name, timestamp) pair.
      - Prefer `executemany` over a Python-level loop of `execute` calls.

    Hints:
      - `datetime.isoformat(sep=" ")` produces the format you want.
      - `executemany` takes an iterable of tuples, one tuple per row.
      - NEVER build the SQL string with f-strings. Use `?` placeholders.
    """

    with sqlite3.connect(db_path) as connection:
      c = connection.cursor()
      data = []
      for row in rows:
        entry = (case_name, row[0].isoformat(sep= " "), row[1], row[2])
        data.append(entry)
      
      command = "INSERT OR REPLACE INTO case_prices(name, date, price, volume) VALUES(?, ?, ?, ?)"

      c.executemany(command, data)

    connection.close()

    
