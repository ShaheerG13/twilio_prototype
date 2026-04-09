import sqlite3
from datetime import datetime

DB_PATH = "incidents.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            caller TEXT NOT NULL,
            category TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Open',
            created_at TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


def log_incident(caller, category):
    conn = get_connection()
    conn.execute(
        "INSERT INTO incidents (caller, category, created_at) VALUES (?, ?, ?)",
        (caller, category, datetime.now().isoformat()),
    )
    conn.commit()
    conn.close()


def get_all_incidents():
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM incidents ORDER BY created_at DESC"
    ).fetchall()
    conn.close()
    return rows
