import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "memory", "db.sqlite3")


def _get_connection():
    return sqlite3.connect(DB_PATH)


def init_reminders_table():
    conn = _get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            due TEXT,
            notified INTEGER DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Migration: add 'notified' column if the table already existed without it
    existing_columns = [row[1] for row in conn.execute("PRAGMA table_info(reminders)").fetchall()]
    if "notified" not in existing_columns:
        conn.execute("ALTER TABLE reminders ADD COLUMN notified INTEGER DEFAULT 0")

    conn.commit()
    conn.close()


def add_reminder(text: str, due: str = None) -> str:
    """
    due should be an ISO datetime string, e.g. '2026-09-13T17:00:00',
    if the user gave a specific time. Leave empty if no specific time.
    """
    conn = _get_connection()
    conn.execute(
        "INSERT INTO reminders (text, due) VALUES (?, ?)",
        (text, due)
    )
    conn.commit()
    conn.close()
    return f"Reminder added: '{text}'" + (f" (due: {due})" if due else "")


def list_reminders() -> str:
    conn = _get_connection()
    rows = conn.execute("SELECT id, text, due FROM reminders ORDER BY id").fetchall()
    conn.close()

    if not rows:
        return "You have no reminders."

    lines = []
    for rid, text, due in rows:
        due_str = f" (due: {due})" if due else ""
        lines.append(f"[{rid}] {text}{due_str}")
    return "\n".join(lines)


def delete_reminder(reminder_id: int) -> str:
    conn = _get_connection()
    cursor = conn.execute("DELETE FROM reminders WHERE id = ?", (reminder_id,))
    conn.commit()
    conn.close()
    if cursor.rowcount == 0:
        return f"No reminder found with id {reminder_id}."
    return f"Reminder {reminder_id} deleted."


def get_due_reminders() -> list[tuple]:
    """Returns (id, text) for reminders that are due and haven't been notified yet."""
    now = datetime.now().isoformat()
    conn = _get_connection()
    rows = conn.execute(
        "SELECT id, text FROM reminders WHERE due IS NOT NULL AND due <= ? AND notified = 0",
        (now,)
    ).fetchall()
    conn.close()
    return rows


def mark_notified(reminder_id: int):
    conn = _get_connection()
    conn.execute("UPDATE reminders SET notified = 1 WHERE id = ?", (reminder_id,))
    conn.commit()
    conn.close()