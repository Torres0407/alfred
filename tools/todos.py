import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "memory", "db.sqlite3")


def _get_connection():
    return sqlite3.connect(DB_PATH)


def init_todos_table():
    conn = _get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            done INTEGER DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def add_todo(task: str) -> str:
    conn = _get_connection()
    conn.execute("INSERT INTO todos (task) VALUES (?)", (task,))
    conn.commit()
    conn.close()
    return f"To-do added: '{task}'"


def list_todos() -> str:
    conn = _get_connection()
    rows = conn.execute("SELECT id, task, done FROM todos ORDER BY id").fetchall()
    conn.close()

    if not rows:
        return "You have no to-dos."

    lines = []
    for tid, task, done in rows:
        mark = "[x]" if done else "[ ]"
        lines.append(f"{mark} ({tid}) {task}")
    return "\n".join(lines)


def complete_todo(todo_id: int) -> str:
    conn = _get_connection()
    cursor = conn.execute("UPDATE todos SET done = 1 WHERE id = ?", (todo_id,))
    conn.commit()
    conn.close()
    if cursor.rowcount == 0:
        return f"No to-do found with id {todo_id}."
    return f"To-do {todo_id} marked complete."


def delete_todo(todo_id: int) -> str:
    conn = _get_connection()
    cursor = conn.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
    conn.commit()
    conn.close()
    if cursor.rowcount == 0:
        return f"No to-do found with id {todo_id}."
    return f"To-do {todo_id} deleted."