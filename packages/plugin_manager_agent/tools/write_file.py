from pathlib import Path

def write_file(path: str, content: str) -> str:
    """
    Writes content to a specified file, creating the file if it doesn't exist.

    This tool will create the file and write the provided content to it.
    If the file already exists, it will be overwritten with the new content.

    Args:
        path (str): The path to the file to be written.
        content (str): The content to write to the file.
    """
    print(f"Writing file: {path}")
    try:
        # Ensure the parent directory exists
        file_path = Path(path)
        file_path.parent.mkdir(parents=True, exist_ok=True)

        # Write the content
        file_path.write_text(content)

        return f"Successfully wrote {len(content)} characters to {path}"
    except Exception as e:
        return f"Error writing to file: {e}"
