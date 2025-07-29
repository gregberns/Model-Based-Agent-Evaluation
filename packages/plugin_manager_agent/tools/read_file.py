from pathlib import Path

def read_file(path: str) -> str:
    """
    Reads the entire content of a specified file.

    Args:
        path (str): The absolute or relative path to the file.
    """
    print(f"Reading file: {path}")
    try:
        return Path(path).read_text()
    except Exception as e:
        return f"Error reading file: {e}"
