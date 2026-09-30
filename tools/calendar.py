import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "memory", "db.sqlite3")


def _get_connection():
    return sqlite3.connect(DB_PATH)


def init_calendar_table():
    conn = _get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS calendar_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            start TEXT NOT NULL,
            end TEXT,
            notes TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def add_event(title: str, start: str, end: str = None, notes: str = None) -> str:
    """start/end should be ISO 8601 datetimes."""
    conn = _get_connection()
    conn.execute(
        "INSERT INTO calendar_events (title, start, end, notes) VALUES (?, ?, ?, ?)",
        (title, start, end, notes)
    )
    conn.commit()
    conn.close()
    end_str = f" to {end}" if end else ""
    return f"Event added: '{title}' at {start}{end_str}"


def list_events(from_date: str = None, to_date: str = None) -> str:
    """
    Lists events, optionally filtered by an ISO date range.
    If both are omitted, lists everything upcoming.
    """
    conn = _get_connection()
    query = "SELECT id, title, start, end, notes FROM calendar_events"
    params = []
    conditions = []

    if from_date:
        conditions.append("start >= ?")
        params.append(from_date)
    if to_date:
        conditions.append("start <= ?")
        params.append(to_date)

    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    query += " ORDER BY start"

    rows = conn.execute(query, params).fetchall()
    conn.close()

    if not rows:
        return "No events found."

    lines = []
    for eid, title, start, end, notes in rows:
        end_str = f" – {end}" if end else ""
        notes_str = f" ({notes})" if notes else ""
        lines.append(f"[{eid}] {title}: {start}{end_str}{notes_str}")
    return "\n".join(lines)


def delete_event(event_id: int) -> str:
    conn = _get_connection()
    cursor = conn.execute("DELETE FROM calendar_events WHERE id = ?", (event_id,))
    conn.commit()
    conn.close()
    if cursor.rowcount == 0:
        return f"No event found with id {event_id}."
    return f"Event {event_id} deleted."