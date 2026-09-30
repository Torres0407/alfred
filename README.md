# 🦇 Alfred — A Multi-Provider, Voice-Controlled AI Agent

Alfred is a personal AI assistant built from scratch as a modular, tool-calling agent. It isn't a chatbot wrapper — it reasons about when to call real tools, executes real actions on a live system, and falls back gracefully across multiple LLM providers when one fails.

This project was built iteratively, day by day, with every feature tested end-to-end (including real bugs found and fixed live) rather than assumed to work.

---

## What Alfred Can Do

### 🗣️ Conversation & Memory
- Persistent conversation history across restarts (SQLite-backed)
- Multi-provider LLM routing with automatic fallback (Groq → Gemini)
- Rate-limit-aware retry logic with exponential backoff before falling back
- Honest fallback behavior — Alfred will never claim an action succeeded if it couldn't actually perform it

### 🎙️ Voice
- **Speech-to-text** via local `faster-whisper` (no cloud dependency, works offline)
- **Text-to-speech** via `edge-tts`, played back with `pygame`
- **Wake word detection** via `openWakeWord`, running continuously in the background
- Full hands-free loop: wake word → listen → transcribe → reason → act → speak → listen again

### 🧠 Personal Assistant Tools
- Reminders, timers, and alarms — with **real OS push notifications** via a background scheduler thread
- Notes and to-do lists
- Calendar (events, date-range queries)
- Sandboxed local file operations (read/write/list/delete, scoped to a dedicated folder)

### 💻 Computer Control
- Open applications, take screenshots, monitor CPU/RAM/disk
- System volume control (Windows Core Audio via `pycaw`)
- **Safety-gated destructive actions** — restart, shutdown, sleep, lock, and closing apps are never directly callable by the model. They're structurally routed through a `request_action` → `confirm_action` pattern, so no prompt injection or model misfire can trigger them without explicit user confirmation.

### 🌐 Browser & Web
- Open websites, run targeted searches (Google/YouTube/GitHub)
- Read and summarize webpage content without a visible browser
- **Full interactive browser automation** via Playwright — navigate, inspect page elements, click, and fill forms, driven by a numbered-element system the model can reliably reference

### 👨‍💻 Coding Agent
- Read/write/run code in a sandboxed workspace
- Full shell command execution (git, pip, npm, etc.) scoped to the workspace directory
- Project scaffolding (multi-folder structures)
- Proven write → run → error → fix → re-run loop — Alfred can write broken code, run it, correctly parse the real traceback, fix it, and re-run successfully

### 📄 Documents & Research
- Read PDF, Word (.docx), Excel (.xlsx), and CSV files
- Multi-angle research tool — runs several search queries on different facets of a topic and synthesizes results into one coherent answer

### 📧 Communication
- Send, list, and read Gmail messages via the **official Gmail API with OAuth2** — not browser automation, not credential handling. A one-time consent screen grants access; Alfred never sees or touches your password.

### 🎵 Entertainment
- Full Spotify playback control (play/pause/skip/search) via the official Spotify Web API with OAuth2

---

## Architecture

```
alfred/
├── main.py                 # CLI entry point (text + voice modes)
├── config.py                # Central settings, .env loader
│
├── brain/
│   ├── router.py             # Multi-provider routing, tool-call loop, rate-limit retry, fallback
│   ├── router_lite.py         # Trimmed router for the hosted "Alfred Lite" demo
│   └── providers/
│       ├── groq_client.py     # Primary LLM provider
│       └── gemini_client.py   # Fallback provider
│
├── voice/
│   ├── listen.py              # Speech-to-text (faster-whisper)
│   ├── speak.py                # Text-to-speech (edge-tts + pygame)
│   └── wake_word.py            # Wake word detection (openWakeWord)
│
├── tools/
│   ├── registry.py              # Tool definitions + dispatch (full version)
│   ├── registry_lite.py          # Trimmed tool registry (hosted demo — no system/local tools)
│   ├── reminders.py, notes.py, todos.py, calendar.py
│   ├── file_ops.py                # Sandboxed local file access
│   ├── documents.py                # PDF/Word/Excel/CSV reading
│   ├── web_search.py                # Tavily → Serper fallback search + multi-angle research
│   ├── browser.py, web_automation.py # Static page reading + full Playwright automation
│   ├── system_control.py              # Safe system control (apps, screenshots, volume, monitoring)
│   ├── confirmation.py                 # Confirmation gate for destructive actions
│   ├── code_exec.py                     # Sandboxed coding agent tools
│   ├── email_tool.py                     # Gmail API integration
│   └── music.py                           # Spotify API integration
│
├── memory/
│   ├── store.py               # Conversation persistence, context windowing
│   └── db.sqlite3
│
├── server/
│   ├── api.py                  # FastAPI backend for the hosted "Alfred Lite" demo
│   └── static/index.html        # Minimal chat UI
│
└── scheduler (in tools/reminders.py + a background thread in main.py)
    → checks for due reminders every 30s and fires real OS notifications
```

---

## Design Decisions Worth Knowing

**Multi-provider fallback is genuinely hardened, not just wired up.** Early versions of the fallback broke in subtle ways — Gemini attempting malformed function calls because it inherited tool-oriented system prompt text, oversized tool results blowing past Groq's token-per-minute limit, and (most importantly) a version that let Gemini's fallback *fabricate* claims that actions had succeeded when they hadn't. All of these were found through live testing and fixed. The current fallback strips tool-call history and tool instructions before handing off to Gemini, and explicitly instructs it to say "I can't do that right now" rather than invent a plausible-sounding success.

**Destructive system actions are structurally gated, not just prompted to be careful.** `restart_computer()`, `shutdown_computer()`, etc. are never exposed to the LLM as callable tools. Only `request_action()` and `confirm_action()` are — meaning there's no phrasing, injection, or model error that can skip confirmation.

**Every sandboxed tool (files, code) validates paths against directory traversal**, not just trusting the model to behave.

**"Alfred Lite" (hosted demo) is a deliberately reduced version**, not a shortcut. It drops everything that depends on a specific local machine — system control, local file access, browser automation, Spotify (device-targeted), and real push notifications (no "desktop" to notify in a hosted context) — while keeping the tool-calling brain, reminders/notes/todos/calendar, and web research fully functional.

---

## Running It Yourself

### Full local version (all features)
1. Clone the repo, create a virtual environment, `pip install -r requirements.txt`
2. Set up API keys in `.env`: `GROQ_API_KEY`, `GEMINI_API_KEY`, `TAVILY_API_KEY`, `SERPER_API_KEY`
3. For Gmail: create a Google Cloud project, enable the Gmail API, download OAuth credentials as `credentials.json`
4. For Spotify: create a Spotify Developer app, add credentials to `.env`
5. Run `python main.py` — choose text or voice-activated mode

### Hosted demo version (Alfred Lite)
A trimmed, always-available web version runs at **[your Render URL here]** — chat, reminders, notes, to-dos, calendar, and web research, no installation required.

---

## What This Project Demonstrates

- LLM tool-calling / function-calling architecture, including multi-round tool loops
- Multi-provider LLM routing with real failure-mode hardening (not just a try/except)
- OAuth2 integration with real third-party APIs (Google Gmail, Spotify)
- Local voice pipeline engineering (STT, TTS, wake-word, all running locally)
- Real browser automation (Playwright) with a model-usable element-reference system
- Windows system-level integration (audio via `pycaw`, process/system monitoring via `psutil`)
- Deliberate safety design for destructive/irreversible actions
- SQLite-backed persistent state and conversation memory
- Deploying a Python web service (FastAPI on Render) with environment-based secrets

---

## Status

Built in-progress across 9 phases (of a planned 12): core conversation loop, full personal-assistant toolkit, voice, computer control, browser control, a coding agent, document/research tools, communication (email), and entertainment (Spotify) are complete and tested. Remaining planned phases: multi-agent orchestration and a live status dashboard.