import os
from config import FILES_ROOT


def _safe_path(relative_path: str) -> str:
    """
    Resolves a relative path inside FILES_ROOT and blocks any attempt
    to escape it (e.g. via '../../' tricks).
    """
    full_path = os.path.abspath(os.path.join(FILES_ROOT, relative_path))
    if not full_path.startswith(os.path.abspath(FILES_ROOT)):
        raise ValueError("Access outside the Alfred files folder is not allowed.")
    return full_path


def list_files(subfolder: str = "") -> str:
    try:
        target = _safe_path(subfolder)
    except ValueError as e:
        return str(e)

    if not os.path.exists(target):
        return f"Folder '{subfolder}' does not exist."

    entries = os.listdir(target)
    if not entries:
        return "This folder is empty."

    lines = []
    for entry in entries:
        full = os.path.join(target, entry)
        tag = "[dir]" if os.path.isdir(full) else "[file]"
        lines.append(f"{tag} {entry}")
    return "\n".join(lines)


def read_file(relative_path: str) -> str:
    try:
        target = _safe_path(relative_path)
    except ValueError as e:
        return str(e)

    if not os.path.isfile(target):
        return f"File '{relative_path}' does not exist."

    try:
        with open(target, "r", encoding="utf-8") as f:
            content = f.read()
    except UnicodeDecodeError:
        return f"'{relative_path}' isn't a readable text file (might be binary)."

    if len(content) > 5000:
        return content[:5000] + "\n...[truncated, file is longer]"
    return content


def write_file(relative_path: str, content: str) -> str:
    try:
        target = _safe_path(relative_path)
    except ValueError as e:
        return str(e)

    os.makedirs(os.path.dirname(target), exist_ok=True)
    with open(target, "w", encoding="utf-8") as f:
        f.write(content)
    return f"Wrote {len(content)} characters to '{relative_path}'."


def delete_file(relative_path: str) -> str:
    try:
        target = _safe_path(relative_path)
    except ValueError as e:
        return str(e)

    if not os.path.isfile(target):
        return f"File '{relative_path}' does not exist."

    os.remove(target)
    return f"Deleted '{relative_path}'."