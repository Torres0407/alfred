import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "db.sqlite3")
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "schema.sql")


def _get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = _get_connection()
    with open(SCHEMA_PATH, "r") as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()


def save_message(role: str, content: str):
    if not content:
        content = "(no response)"
    conn = _get_connection()
    conn.execute(
        "INSERT INTO messages (role, content) VALUES (?, ?)",
        (role, content)
    )
    conn.commit()
    conn.close()


def get_recent_context(limit: int = 10) -> list[dict]:
    """
    Returns the last `limit` messages in chronological order,
    formatted for the LLM: [{"role": ..., "content": ...}, ...]
    """
    conn = _get_connection()
    cursor = conn.execute(
        "SELECT role, content FROM messages ORDER BY id DESC LIMIT ?",
        (limit,)
    )
    rows = cursor.fetchall()
    conn.close()

    rows.reverse()
    messages = [{"role": role, "content": content} for role, content in rows]

    # Safety net: if total content is still very large (e.g. one huge tool
    # result), trim from the oldest messages until it's reasonable.
    def total_len(msgs):
        return sum(len(m["content"]) for m in msgs)

    while len(messages) > 2 and total_len(messages) > 6000:
        messages.pop(0)

    return messages