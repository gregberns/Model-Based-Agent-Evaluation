from pathlib import Path

def list_files(path: str = ".") -> str:
    """
    Lists all files and directories in a specified path.

    Args:
        path (str): The directory path to list. Defaults to the current directory.
    """
    print(f"Listing files in: {path}")
    try:
        files = [str(p) for p in Path(path).glob("*")]
        return "\n".join(files)
    except Exception as e:
        return f"Error listing files: {e}"

