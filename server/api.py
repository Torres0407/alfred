from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from datetime import datetime

from brain.router_lite import route
from memory.store import init_db, save_message, get_recent_context
from tools.reminders import init_reminders_table
from tools.notes import init_notes_table
from tools.todos import init_todos_table
from tools.calendar import init_calendar_table

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

init_db()
init_reminders_table()
init_notes_table()
init_todos_table()
init_calendar_table()


class ChatRequest(BaseModel):
    message: str


@app.post("/chat")
def chat(req: ChatRequest):
    system_prompt = {
        "role": "system",
        "content": (
            f"You are Alfred, a helpful personal AI assistant demo. Be concise and direct. "
            f"Current date/time: {datetime.now().isoformat()}. "
            f"Convert natural language times to ISO 8601 for reminders/events."
        )
    }
    save_message("user", req.message)
    history = [system_prompt] + get_recent_context()
    reply = route(history)
    save_message("assistant", reply)
    return {"reply": reply}


@app.get("/", response_class=HTMLResponse)
def index():
    with open("server/static/index.html", "r", encoding="utf-8") as f:
        return f.read()