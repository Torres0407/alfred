import subprocess
import psutil
import pyautogui
import os
from datetime import datetime
from pycaw.pycaw import AudioUtilities

SCREENSHOTS_DIR = os.path.join(os.path.dirname(__file__), "..", "screenshots")
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)


def open_app(app_name: str) -> str:
    """
    Opens an application by name. Works for common apps registered
    with Windows (notepad, calculator, chrome, etc.) via the 'start' command.
    """
    try:
        subprocess.Popen(f"start {app_name}", shell=True)
        return f"Opening {app_name}."
    except Exception as e:
        return f"Couldn't open {app_name}: {e}"


def take_screenshot() -> str:
    filename = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    path = os.path.join(SCREENSHOTS_DIR, filename)
    img = pyautogui.screenshot()
    img.save(path)
    return f"Screenshot saved: {path}"


def get_system_status() -> str:
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory()
    disk = psutil.disk_usage("C:\\")

    return (
        f"CPU usage: {cpu}%\n"
        f"RAM usage: {ram.percent}% ({ram.used // (1024**3)}GB / {ram.total // (1024**3)}GB)\n"
        f"Disk usage (C:): {disk.percent}% ({disk.used // (1024**3)}GB / {disk.total // (1024**3)}GB)"
    )

def set_volume(level: int) -> str:
    """level: 0-100"""
    level = max(0, min(100, level))
    device = AudioUtilities.GetSpeakers()
    device.EndpointVolume.SetMasterVolumeLevelScalar(level / 100, None)
    return f"Volume set to {level}%."


def get_volume() -> str:
    device = AudioUtilities.GetSpeakers()
    current = device.EndpointVolume.GetMasterVolumeLevelScalar()
    return f"Current volume: {round(current * 100)}%"

def restart_computer() -> str:
    subprocess.Popen("shutdown /r /t 5", shell=True)
    return "Restarting the computer in 5 seconds."


def shutdown_computer() -> str:
    subprocess.Popen("shutdown /s /t 5", shell=True)
    return "Shutting down the computer in 5 seconds."


def sleep_computer() -> str:
    subprocess.Popen("rundll32.exe powrprof.dll,SetSuspendState 0,1,0", shell=True)
    return "Putting the computer to sleep."


def lock_computer() -> str:
    subprocess.Popen("rundll32.exe user32.dll,LockWorkStation", shell=True)
    return "Computer locked."


def close_app(app_name: str) -> str:
    if not app_name:
        return "No application specified to close."
    try:
        subprocess.Popen(f"taskkill /IM {app_name}.exe /F", shell=True)
        return f"Closed {app_name}."
    except Exception as e:
        return f"Couldn't close {app_name}: {e}"