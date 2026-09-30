_pending_action = None  # {"action": str, "target": str|None}

ACTIONS = {
    "restart": "restart the computer",
    "shutdown": "shut down the computer",
    "sleep": "put the computer to sleep",
    "lock": "lock the computer",
    "close_app": "close an application",
}


def request_action(action: str, target: str = None) -> str:
    global _pending_action
    if action not in ACTIONS:
        return f"Unknown action '{action}'."

    _pending_action = {"action": action, "target": target}
    description = ACTIONS[action]
    if target:
        description += f" ({target})"
    return f"Are you sure you want to {description}? Say 'confirm' to proceed, or 'cancel' to stop."


def confirm_action() -> str:
    global _pending_action
    if not _pending_action:
        return "There's no pending action to confirm."

    from tools import system_control
    action = _pending_action["action"]
    target = _pending_action["target"]
    _pending_action = None

    if action == "restart":
        return system_control.restart_computer()
    elif action == "shutdown":
        return system_control.shutdown_computer()
    elif action == "sleep":
        return system_control.sleep_computer()
    elif action == "lock":
        return system_control.lock_computer()
    elif action == "close_app":
        return system_control.close_app(target)
    return "Something went wrong executing the confirmed action."


def cancel_action() -> str:
    global _pending_action
    if not _pending_action:
        return "There's no pending action to cancel."
    _pending_action = None
    return "Action cancelled."