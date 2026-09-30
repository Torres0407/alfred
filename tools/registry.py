from tools import reminders, file_ops, web_search, notes, todos, calendar, system_control, confirmation, browser, web_automation, code_exec, documents, email_tool, music

TOOL_DEFINITIONS = [
            {
        "type": "function",
        "function": {
            "name": "add_reminder",
            "description": "Add a new reminder for the user.",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "What to remind the user about."},
                    "due": {"type": "string", "description": "Optional due date/time in strict ISO 8601 format, e.g. '2026-09-13T17:00:00'. Convert any natural language time the user gives (e.g. 'tomorrow at 5pm') into this exact format based on the current date/time."}
                },
                "required": ["text"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_reminders",
            "description": "List all of the user's current reminders.",
            "parameters": {"type": "object", "properties": {}}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_reminder",
            "description": "Delete a reminder by its id number.",
            "parameters": {
                "type": "object",
                "properties": {
                    "reminder_id": {"type": "integer", "description": "The id of the reminder to delete."}
                },
                "required": ["reminder_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "List files and folders inside the user's Alfred files folder (optionally a subfolder).",
            "parameters": {
                "type": "object",
                "properties": {
                    "subfolder": {"type": "string", "description": "Relative subfolder path, or empty for root."}
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read the contents of a text file inside the user's Alfred files folder.",
            "parameters": {
                "type": "object",
                "properties": {
                    "relative_path": {"type": "string", "description": "Relative path to the file."}
                },
                "required": ["relative_path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Create or overwrite a text file inside the user's Alfred files folder.",
            "parameters": {
                "type": "object",
                "properties": {
                    "relative_path": {"type": "string", "description": "Relative path to the file."},
                    "content": {"type": "string", "description": "Text content to write."}
                },
                "required": ["relative_path", "content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_file",
            "description": "Delete a file inside the user's Alfred files folder.",
            "parameters": {
                "type": "object",
                "properties": {
                    "relative_path": {"type": "string", "description": "Relative path to the file to delete."}
                },
                "required": ["relative_path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Search the web for current information, news, or anything outside your knowledge.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "The search query."}
                },
                "required": ["query"]
            }
        }
    },
        {
        "type": "function",
        "function": {
            "name": "add_note",
            "description": "Save a freeform note for the user.",
            "parameters": {
                "type": "object",
                "properties": {
                    "content": {"type": "string", "description": "The note content."}
                },
                "required": ["content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_notes",
            "description": "List all of the user's saved notes.",
            "parameters": {"type": "object", "properties": {}}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_note",
            "description": "Delete a note by its id number.",
            "parameters": {
                "type": "object",
                "properties": {
                    "note_id": {"type": "integer", "description": "The id of the note to delete."}
                },
                "required": ["note_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "add_todo",
            "description": "Add a new to-do task for the user.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task": {"type": "string", "description": "The task description."}
                },
                "required": ["task"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_todos",
            "description": "List all of the user's to-do tasks, showing which are done.",
            "parameters": {"type": "object", "properties": {}}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "complete_todo",
            "description": "Mark a to-do task as complete by its id.",
            "parameters": {
                "type": "object",
                "properties": {
                    "todo_id": {"type": "integer", "description": "The id of the to-do to mark complete."}
                },
                "required": ["todo_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_todo",
            "description": "Delete a to-do task by its id.",
            "parameters": {
                "type": "object",
                "properties": {
                    "todo_id": {"type": "integer", "description": "The id of the to-do to delete."}
                },
                "required": ["todo_id"]
            }
        }
    },
        {
        "type": "function",
        "function": {
            "name": "add_event",
            "description": "Add a calendar event with a specific start time (and optional end time).",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Event title."},
                    "start": {"type": "string", "description": "Start datetime in strict ISO 8601 format."},
                    "end": {"type": "string", "description": "Optional end datetime in ISO 8601 format."},
                    "notes": {"type": "string", "description": "Optional notes about the event."}
                },
                "required": ["title", "start"]
            }
        }
    },
        {
        "type": "function",
        "function": {
            "name": "list_events",
            "description": "List calendar events, optionally within a date range.",
            "parameters": {
                "type": "object",
                "properties": {
                    "from_date": {"type": ["string", "null"], "description": "Optional ISO date/datetime to filter events from. Use null if not filtering."},
                    "to_date": {"type": ["string", "null"], "description": "Optional ISO date/datetime to filter events to. Use null if not filtering."}
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_event",
            "description": "Delete a calendar event by its id.",
            "parameters": {
                "type": "object",
                "properties": {
                    "event_id": {"type": "integer", "description": "The id of the event to delete."}
                },
                "required": ["event_id"]
            }
        }
    },
        {
        "type": "function",
        "function": {
            "name": "open_app",
            "description": "Open an application on the computer by name (e.g. 'notepad', 'calc', 'chrome').",
            "parameters": {
                "type": "object",
                "properties": {
                    "app_name": {"type": "string", "description": "Name of the application to open."}
                },
                "required": ["app_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "take_screenshot",
            "description": "Take a screenshot of the current screen and save it.",
            "parameters": {"type": "object", "properties": {}}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_system_status",
            "description": "Get current CPU, RAM, and disk usage.",
            "parameters": {"type": "object", "properties": {}}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "set_volume",
            "description": "Set the system volume to a specific level.",
            "parameters": {
                "type": "object",
                "properties": {
                    "level": {"type": "integer", "description": "Volume level from 0 to 100."}
                },
                "required": ["level"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_volume",
            "description": "Get the current system volume level.",
            "parameters": {"type": "object", "properties": {}}
        }
    },
        {
        "type": "function",
        "function": {
            "name": "request_action",
            "description": "Request a potentially destructive system action (restart, shutdown, sleep, lock, close_app). This does NOT execute it — it only asks the user for confirmation. You must call this first for any of these actions, never assume permission.",
            "parameters": {
                "type": "object",
                "properties": {
                    "action": {"type": "string", "enum": ["restart", "shutdown", "sleep", "lock", "close_app"]},
                    "target": {"type": "string", "description": "For close_app, the name of the app to close. Omit for other actions."}
                },
                "required": ["action"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "confirm_action",
            "description": "Confirm and execute the most recently requested pending action. Only call this when the user has clearly said yes/confirm to a prior request_action prompt.",
            "parameters": {"type": "object", "properties": {}}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "cancel_action",
            "description": "Cancel the pending action if the user says no/cancel.",
            "parameters": {"type": "object", "properties": {}}
        }
    },
        {
        "type": "function",
        "function": {
            "name": "open_website",
            "description": "Open a specific website URL in the user's default browser.",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {"type": "string", "description": "The website URL to open."}
                },
                "required": ["url"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_google",
            "description": "Open a Google search for the given query in the browser.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "The search query."}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_youtube",
            "description": "Open a YouTube search for the given query in the browser.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "The search query."}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_github",
            "description": "Open a GitHub search for the given query in the browser.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "The search query."}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_webpage",
            "description": "Fetch and read the text content of a specific webpage URL, without opening a visible browser. Use this to summarize or answer questions about a page's content.",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {"type": "string", "description": "The webpage URL to read."}
                },
                "required": ["url"]
            }
        }
    },
        {
        "type": "function",
        "function": {
            "name": "navigate_browser",
            "description": "Open a real, controllable browser window and navigate to a URL. Use this (not open_website) when the user wants to interact with a page — click things, fill forms, etc.",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {"type": "string", "description": "URL to navigate to."}
                },
                "required": ["url"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_page_elements",
            "description": "Get a numbered list of clickable/fillable elements on the current page. Always call this before click_element or fill_element to know valid indexes.",
            "parameters": {"type": "object", "properties": {}}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "click_element",
            "description": "Click an element on the page by its index from get_page_elements.",
            "parameters": {
                "type": "object",
                "properties": {
                    "index": {"type": "integer", "description": "The index of the element to click."}
                },
                "required": ["index"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "fill_element",
            "description": "Type text into an input/textarea element by its index from get_page_elements.",
            "parameters": {
                "type": "object",
                "properties": {
                    "index": {"type": "integer", "description": "The index of the element to fill."},
                    "text": {"type": "string", "description": "The text to type."}
                },
                "required": ["index", "text"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "close_browser",
            "description": "Close the automated browser window.",
            "parameters": {"type": "object", "properties": {}}
        }
    },
        {
        "type": "function",
        "function": {
            "name": "list_code_files",
            "description": "List files in the user's code workspace (optionally a subfolder).",
            "parameters": {
                "type": "object",
                "properties": {
                    "subfolder": {"type": ["string", "null"], "description": "Optional subfolder path."}
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_code_file",
            "description": "Read the contents of a code file in the workspace.",
            "parameters": {
                "type": "object",
                "properties": {
                    "relative_path": {"type": "string", "description": "Relative path to the file."}
                },
                "required": ["relative_path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "write_code_file",
            "description": "Create or overwrite a code file in the workspace.",
            "parameters": {
                "type": "object",
                "properties": {
                    "relative_path": {"type": "string", "description": "Relative path to the file."},
                    "content": {"type": "string", "description": "The code content to write."}
                },
                "required": ["relative_path", "content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "run_python_file",
            "description": "Run a Python file from the code workspace and return its output, errors, and exit code.",
            "parameters": {
                "type": "object",
                "properties": {
                    "relative_path": {"type": "string", "description": "Relative path to the Python file to run."}
                },
                "required": ["relative_path"]
            }
        }
    },
        {
        "type": "function",
        "function": {
            "name": "run_shell_command",
            "description": "Run a shell/terminal command inside the code workspace (e.g. git commands, pip install, npm install). Use this for git operations: git init, git add, git commit, git push, git status, etc.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {"type": "string", "description": "The shell command to run."}
                },
                "required": ["command"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_project_structure",
            "description": "Create a new project folder with optional subfolders inside the code workspace.",
            "parameters": {
                "type": "object",
                "properties": {
                    "project_name": {"type": "string", "description": "Name of the project folder to create."},
                    "folders": {
                        "type": ["array", "null"],
                        "items": {"type": "string"},
                        "description": "Optional list of subfolder names to create inside the project."
                    }
                },
                "required": ["project_name"]
            }
        }
    },
        {
        "type": "function",
        "function": {
            "name": "read_pdf",
            "description": "Extract and read text from a PDF file in the user's Alfred files folder.",
            "parameters": {
                "type": "object",
                "properties": {
                    "relative_path": {"type": "string", "description": "Relative path to the PDF file."}
                },
                "required": ["relative_path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_word_doc",
            "description": "Extract and read text from a Word (.docx) file in the user's Alfred files folder.",
            "parameters": {
                "type": "object",
                "properties": {
                    "relative_path": {"type": "string", "description": "Relative path to the Word document."}
                },
                "required": ["relative_path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_excel",
            "description": "Read data from an Excel (.xlsx) file in the user's Alfred files folder.",
            "parameters": {
                "type": "object",
                "properties": {
                    "relative_path": {"type": "string", "description": "Relative path to the Excel file."},
                    "sheet_name": {"type": ["string", "null"], "description": "Optional specific sheet name to read."}
                },
                "required": ["relative_path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_csv",
            "description": "Read and summarize a CSV file in the user's Alfred files folder.",
            "parameters": {
                "type": "object",
                "properties": {
                    "relative_path": {"type": "string", "description": "Relative path to the CSV file."}
                },
                "required": ["relative_path"]
            }
        }
    },
        {
        "type": "function",
        "function": {
            "name": "research_topic",
            "description": "Perform in-depth research on a topic by searching multiple angles (overview, pros/cons, recent news, opinions) and returning combined results for you to synthesize into a comprehensive answer. Use this instead of web_search when the user wants thorough research, a comparison, or a detailed report — not a quick fact lookup.",
            "parameters": {
                "type": "object",
                "properties": {
                    "topic": {"type": "string", "description": "The topic to research."},
                    "angles": {
                        "type": ["array", "null"],
                        "items": {"type": "string"},
                        "description": "Optional specific search angles/queries. If omitted, sensible defaults are used."
                    }
                },
                "required": ["topic"]
            }
        }
    },
        {
        "type": "function",
        "function": {
            "name": "send_email",
            "description": "Send an email from the user's Gmail account.",
            "parameters": {
                "type": "object",
                "properties": {
                    "to": {"type": "string", "description": "Recipient email address."},
                    "subject": {"type": "string", "description": "Email subject line."},
                    "body": {"type": "string", "description": "Email body text."}
                },
                "required": ["to", "subject", "body"]
            }
        }
    },
        {
        "type": "function",
        "function": {
            "name": "list_recent_emails",
            "description": "List recent emails from the user's inbox, optionally filtered by a Gmail search query.",
            "parameters": {
                "type": "object",
                "properties": {
                    "max_results": {"type": ["integer", "null"], "description": "Max number of emails to return, default 10."},
                    "query": {"type": ["string", "null"], "description": "Optional Gmail search query (e.g. 'from:someone@example.com', 'is:unread')."}
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_email",
            "description": "Read the full content of a specific email by its id (get the id from list_recent_emails first).",
            "parameters": {
                "type": "object",
                "properties": {
                    "email_id": {"type": "string", "description": "The email's id."}
                },
                "required": ["email_id"]
            }
        }
    },
        {
        "type": "function",
        "function": {
            "name": "play_music",
            "description": "Play music on Spotify. If a query is given, searches and plays that song; otherwise resumes current playback.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": ["string", "null"], "description": "Song/artist to search and play, or null to resume."}
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "pause_music",
            "description": "Pause Spotify playback.",
            "parameters": {"type": "object", "properties": {}}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "skip_track",
            "description": "Skip to the next track on Spotify.",
            "parameters": {"type": "object", "properties": {}}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "previous_track",
            "description": "Go back to the previous track on Spotify.",
            "parameters": {"type": "object", "properties": {}}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_track",
            "description": "Get the currently playing track on Spotify.",
            "parameters": {"type": "object", "properties": {}}
        }
    },
]

TOOL_FUNCTIONS = {
    "add_reminder": reminders.add_reminder,
    "list_reminders": reminders.list_reminders,
    "delete_reminder": reminders.delete_reminder,
    "list_files": file_ops.list_files,
    "read_file": file_ops.read_file,
    "write_file": file_ops.write_file,
    "delete_file": file_ops.delete_file,
    "web_search": web_search.web_search,
    "add_note": notes.add_note,
    "list_notes": notes.list_notes,
    "delete_note": notes.delete_note,
    "add_todo": todos.add_todo,
    "list_todos": todos.list_todos,
    "complete_todo": todos.complete_todo,
    "delete_todo": todos.delete_todo,
    "add_event": calendar.add_event,
    "list_events": calendar.list_events,
    "delete_event": calendar.delete_event,
    "open_app": system_control.open_app,
    "take_screenshot": system_control.take_screenshot,
    "get_system_status": system_control.get_system_status,
    "set_volume": system_control.set_volume,
    "get_volume": system_control.get_volume,
    "request_action": confirmation.request_action,
    "confirm_action": confirmation.confirm_action,
    "cancel_action": confirmation.cancel_action,
    "open_website": browser.open_website,
    "search_google": browser.search_google,
    "search_youtube": browser.search_youtube,
    "search_github": browser.search_github,
    "read_webpage": browser.read_webpage,
    "navigate_browser": web_automation.navigate_browser,
    "get_page_elements": web_automation.get_page_elements,
    "click_element": web_automation.click_element,
    "fill_element": web_automation.fill_element,
    "close_browser": web_automation.close_browser,
    "list_code_files": code_exec.list_code_files,
    "read_code_file": code_exec.read_code_file,
    "write_code_file": code_exec.write_code_file,
    "run_python_file": code_exec.run_python_file,
    "run_shell_command": code_exec.run_shell_command,
    "create_project_structure": code_exec.create_project_structure,
    "read_pdf": documents.read_pdf,
    "read_word_doc": documents.read_word_doc,
    "read_excel": documents.read_excel,
    "read_csv": documents.read_csv,
    "research_topic": web_search.research_topic,
    "send_email": email_tool.send_email,
    "list_recent_emails": email_tool.list_recent_emails,
    "read_email": email_tool.read_email,
    "play_music": music.play_music,
    "pause_music": music.pause_music,
    "skip_track": music.skip_track,
    "previous_track": music.previous_track,
    "get_current_track": music.get_current_track,
}


def execute_tool(name: str, arguments: dict) -> str:
    if name not in TOOL_FUNCTIONS:
        return f"Error: unknown tool '{name}'"
    # Strip None values so functions can rely on their own defaults
    cleaned_args = {k: v for k, v in arguments.items() if v is not None}
    try:
        return TOOL_FUNCTIONS[name](**cleaned_args)
    except Exception as e:
        return f"Error running tool '{name}': {e}"