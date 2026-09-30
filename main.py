from datetime import datetime
from brain.router import route
from config import ASSISTANT_NAME
from memory.store import init_db, save_message, get_recent_context
from tools.reminders import init_reminders_table
from tools.scheduler import start_scheduler
from tools.notes import init_notes_table
from tools.todos import init_todos_table
from tools.calendar import init_calendar_table
from voice.speak import speak
from config import VOICE_ENABLED
from voice.listen import listen_once
from voice.wake_word import wait_for_wake_word

def main():
    init_db()
    init_reminders_table()
    init_notes_table()
    init_todos_table()
    init_calendar_table()
    start_scheduler()

    def build_system_prompt():
        return {
            "role": "system",
            "content": (
                f"You are {ASSISTANT_NAME}, a helpful personal AI assistant. Be concise and direct. "
                f"The current date and time is {datetime.now().isoformat()}. "
                f"When the user asks to set a reminder, timer, or alarm — these all use the same add_reminder tool. "
                f"A 'timer' (e.g. 'set a timer for 10 minutes') means due = now + that duration. "
                f"An 'alarm' (e.g. 'wake me up at 7am') means due = the next occurrence of that clock time. "
                f"Always convert the time to strict ISO 8601 format based on the current date/time given above."
                f"For restart, shutdown, sleep, lock, or closing an app, you must ALWAYS call request_action first and wait for the user to explicitly confirm before calling confirm_action. Never skip this step."
                f"For quick factual lookups, use web_search. For in-depth research, comparisons, or when the user wants a thorough report on a topic, use research_topic instead, then synthesize the multiple results into one clear, well-organized answer citing key points from different searches."
            )
        }

    def handle_turn(user_input: str):
        save_message("user", user_input)
        history = [build_system_prompt()] + get_recent_context()
        reply = route(history)
        save_message("assistant", reply)
        print(f"{ASSISTANT_NAME}: {reply}\n")
        if VOICE_ENABLED:
            speak(reply)

    mode = input("Type 'v' for voice-activated mode, or press Enter for text mode: ").strip().lower()

    if mode == "v":
        print(f"{ASSISTANT_NAME} is listening for 'Hey Mycroft'... (Ctrl+C to quit)\n")
        while True:
            wait_for_wake_word()
            print("🔔 Wake word detected!")
            user_input = listen_once()
            print(f"You (voice): {user_input}")
            if not user_input:
                continue
            if user_input.lower() in ("exit", "quit"):
                print(f"{ASSISTANT_NAME}: Goodbye.")
                break
            handle_turn(user_input)
    else:
        print(f"{ASSISTANT_NAME} is online. Type 'exit' to quit.\n")
        while True:
            raw_input_ = input("You (or type 'v' to speak): ").strip()
            if raw_input_.lower() == "v":
                user_input = listen_once()
                print(f"You (voice): {user_input}")
            else:
                user_input = raw_input_
            if not user_input:
                continue
            if user_input.lower() in ("exit", "quit"):
                print(f"{ASSISTANT_NAME}: Goodbye.")
                break
            handle_turn(user_input)


if __name__ == "__main__":
    main()