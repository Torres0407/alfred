import threading
import time
from plyer import notification
from tools.reminders import get_due_reminders, mark_notified
from config import ASSISTANT_NAME

CHECK_INTERVAL_SECONDS = 30


def _check_loop():
    while True:
        due = get_due_reminders()
        for reminder_id, text in due:
            print(f"\n🔔 [{ASSISTANT_NAME}] Reminder due: {text}\n")
            try:
                notification.notify(
                    title=f"{ASSISTANT_NAME} Reminder",
                    message=text,
                    timeout=10
                )
            except Exception as e:
                print(f"[scheduler] Notification failed: {e}")
            mark_notified(reminder_id)
        time.sleep(CHECK_INTERVAL_SECONDS)


def start_scheduler():
    thread = threading.Thread(target=_check_loop, daemon=True)
    thread.start()