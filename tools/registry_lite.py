from tools import reminders, notes, todos, calendar, web_search

TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "add_reminder",
            "description": "Add a new reminder for the user.",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {"type": "string"},
                    "due": {"type": ["string", "null"], "description": "ISO 8601 datetime, or null."}
                },
                "required": ["text"]
            }
        }
    },
    {"type": "function", "function": {"name": "list_reminders", "description": "List all reminders.", "parameters": {"type": "object", "properties": {}}}},
    {
        "type": "function",
        "function": {
            "name": "delete_reminder",
            "description": "Delete a reminder by id.",
            "parameters": {"type": "object", "properties": {"reminder_id": {"type": "integer"}}, "required": ["reminder_id"]}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "add_note",
            "description": "Save a note.",
            "parameters": {"type": "object", "properties": {"content": {"type": "string"}}, "required": ["content"]}
        }
    },
    {"type": "function", "function": {"name": "list_notes", "description": "List all notes.", "parameters": {"type": "object", "properties": {}}}},
    {
        "type": "function",
        "function": {
            "name": "add_todo",
            "description": "Add a to-do task.",
            "parameters": {"type": "object", "properties": {"task": {"type": "string"}}, "required": ["task"]}
        }
    },
    {"type": "function", "function": {"name": "list_todos", "description": "List to-dos.", "parameters": {"type": "object", "properties": {}}}},
    {
        "type": "function",
        "function": {
            "name": "complete_todo",
            "description": "Mark a to-do complete.",
            "parameters": {"type": "object", "properties": {"todo_id": {"type": "integer"}}, "required": ["todo_id"]}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "add_event",
            "description": "Add a calendar event.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "start": {"type": "string"},
                    "end": {"type": ["string", "null"]},
                    "notes": {"type": ["string", "null"]}
                },
                "required": ["title", "start"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_events",
            "description": "List calendar events.",
            "parameters": {"type": "object", "properties": {"from_date": {"type": ["string", "null"]}, "to_date": {"type": ["string", "null"]}}}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Search the web for current information.",
            "parameters": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "research_topic",
            "description": "In-depth multi-angle research on a topic.",
            "parameters": {"type": "object", "properties": {"topic": {"type": "string"}, "angles": {"type": ["array", "null"], "items": {"type": "string"}}}, "required": ["topic"]}
        }
    },
]

TOOL_FUNCTIONS = {
    "add_reminder": reminders.add_reminder,
    "list_reminders": reminders.list_reminders,
    "delete_reminder": reminders.delete_reminder,
    "add_note": notes.add_note,
    "list_notes": notes.list_notes,
    "add_todo": todos.add_todo,
    "list_todos": todos.list_todos,
    "complete_todo": todos.complete_todo,
    "add_event": calendar.add_event,
    "list_events": calendar.list_events,
    "web_search": web_search.web_search,
    "research_topic": web_search.research_topic,
}


def execute_tool(name: str, arguments: dict) -> str:
    if name not in TOOL_FUNCTIONS:
        return f"Error: unknown tool '{name}'"
    cleaned_args = {k: v for k, v in arguments.items() if v is not None}
    try:
        return TOOL_FUNCTIONS[name](**cleaned_args)
    except Exception as e:
        return f"Error running tool '{name}': {e}"