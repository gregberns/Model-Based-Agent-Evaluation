import os
import subprocess

def execute_shell_command(command: str, timeout: int | None = None) -> str:
    """
    Executes a shell command in the current working directory.

    Args:
        command (str): The shell command to execute.
        timeout (int | None, optional): Timeout in seconds. Defaults to environment variable
                                     or 30 seconds if not specified.
    """
    print(f"Executing command: {command}")

    # Use environment variable for timeout in tests, or provided parameter, or default
    if timeout is None:
        timeout = int(os.getenv("SHELL_COMMAND_TIMEOUT", "30"))

    try:
        process = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return f"Exit Code: {process.returncode}\nSTDOUT:\n{process.stdout}\nSTDERR:\n{process.stderr}"
    except subprocess.TimeoutExpired:
        return f"Error executing command: Command '{command}' timed out after {timeout} seconds"
    except Exception as e:
        return f"Error executing command: {e}"
