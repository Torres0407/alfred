import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "memory", "db.sqlite3")


def _get_connection():
    return sqlite3.connect(DB_PATH)


def init_notes_table():
    conn = _get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def add_note(content: str) -> str:
    conn = _get_connection()
    conn.execute("INSERT INTO notes (content) VALUES (?)", (content,))
    conn.commit()
    conn.close()
    return f"Note saved: '{content}'"


def list_notes() -> str:
    conn = _get_connection()
    rows = conn.execute("SELECT id, content FROM notes ORDER BY id").fetchall()
    conn.close()

    if not rows:
        return "You have no notes."

    lines = [f"[{nid}] {content}" for nid, content in rows]
    return "\n".join(lines)


def delete_note(note_id: int) -> str:
    conn = _get_connection()
    cursor = conn.execute("DELETE FROM notes WHERE id = ?", (note_id,))
    conn.commit()
    conn.close()
    if cursor.rowcount == 0:
        return f"No note found with id {note_id}."
    return f"Note {note_id} deleted."