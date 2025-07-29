import subprocess

def execute_shell_command(command: str) -> str:
    """
    Executes a shell command in the current working directory.

    Args:
        command (str): The shell command to execute.
    """
    print(f"Executing command: {command}")
    try:
        process = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30,
        )
        return f"Exit Code: {process.returncode}\nSTDOUT:\n{process.stdout}\nSTDERR:\n{process.stderr}"
    except Exception as e:
        return f"Error executing command: {e}"

