import os
import subprocess
from config import CODE_WORKSPACE


def _safe_path(relative_path: str) -> str:
    full_path = os.path.abspath(os.path.join(CODE_WORKSPACE, relative_path))
    if not full_path.startswith(os.path.abspath(CODE_WORKSPACE)):
        raise ValueError("Access outside the code workspace is not allowed.")
    return full_path


def list_code_files(subfolder: str = "") -> str:
    try:
        target = _safe_path(subfolder)
    except ValueError as e:
        return str(e)

    if not os.path.exists(target):
        return f"Folder '{subfolder}' does not exist."

    lines = []
    for root, dirs, files in os.walk(target):
        dirs[:] = [d for d in dirs if d not in (".git", "__pycache__", "node_modules", "venv")]
        rel_root = os.path.relpath(root, target)

        for d in dirs:
            path = d if rel_root == "." else os.path.join(rel_root, d)
            lines.append(f"[dir] {path}")

        for f in files:
            path = f if rel_root == "." else os.path.join(rel_root, f)
            lines.append(f"[file] {path}")

    if not lines:
        return "This workspace folder is empty."
    return "\n".join(lines)


def read_code_file(relative_path: str) -> str:
    try:
        target = _safe_path(relative_path)
    except ValueError as e:
        return str(e)

    if not os.path.isfile(target):
        return f"File '{relative_path}' does not exist."

    with open(target, "r", encoding="utf-8") as f:
        content = f.read()

    if len(content) > 8000:
        content = content[:8000] + "\n...[truncated]"
    return content


def write_code_file(relative_path: str, content: str) -> str:
    try:
        target = _safe_path(relative_path)
    except ValueError as e:
        return str(e)

    os.makedirs(os.path.dirname(target), exist_ok=True)
    with open(target, "w", encoding="utf-8") as f:
        f.write(content)
    return f"Wrote {len(content)} characters to '{relative_path}'."


def run_python_file(relative_path: str, timeout: int = 15) -> str:
    try:
        target = _safe_path(relative_path)
    except ValueError as e:
        return str(e)

    if not os.path.isfile(target):
        return f"File '{relative_path}' does not exist."

    try:
        result = subprocess.run(
            ["python", target],
            cwd=CODE_WORKSPACE,
            capture_output=True,
            text=True,
            timeout=timeout
        )
    except subprocess.TimeoutExpired:
        return f"Execution timed out after {timeout} seconds."

    output = f"Exit code: {result.returncode}\n"
    if result.stdout:
        output += f"--- stdout ---\n{result.stdout}\n"
    if result.stderr:
        output += f"--- stderr ---\n{result.stderr}\n"
    return output

def run_shell_command(command: str, timeout: int = 20) -> str:
    """
    Runs a shell command inside the code workspace. Used for git,
    pip installs, running dev servers briefly, etc.
    """
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=CODE_WORKSPACE,
            capture_output=True,
            text=True,
            timeout=timeout
        )
    except subprocess.TimeoutExpired:
        return f"Command timed out after {timeout} seconds."

    output = f"Exit code: {result.returncode}\n"
    if result.stdout:
        output += f"--- stdout ---\n{result.stdout}\n"
    if result.stderr:
        output += f"--- stderr ---\n{result.stderr}\n"
    return output


def create_project_structure(project_name: str, folders: list[str] = None) -> str:
    """Creates a new project folder with optional subfolders inside the workspace."""
    try:
        project_path = _safe_path(project_name)
    except ValueError as e:
        return str(e)

    os.makedirs(project_path, exist_ok=True)
    created = [project_name]

    if folders:
        for folder in folders:
            folder_path = os.path.join(project_path, folder)
            os.makedirs(folder_path, exist_ok=True)
            created.append(f"{project_name}/{folder}")

    return f"Created project structure:\n" + "\n".join(created)