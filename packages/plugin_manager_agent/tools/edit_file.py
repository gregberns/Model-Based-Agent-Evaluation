import difflib
from pathlib import Path

# This tool's design pattern is inspired by the FileEditTool from the motleycoder library:
# https://github.com/MotleyAI/motleycoder/blob/main/motleycoder/tools/file_edit_tool.py
def edit_file(file_path: str, search_block: str, replace_block: str) -> str:
    """
    Replaces a specified block of text in a file with a new block of text.

    This tool is for making precise changes to a file. If the `search_block`
    is not found exactly as provided, the tool will fail and suggest close
    matches to help with correction.

    Args:
        file_path (str): The path to the file to be edited.
        search_block (str): The exact block of text to search for in the file.
        replace_block (str): The block of text that will replace the `search_block`.
    """
    print(f"Editing file: {file_path}")
    try:
        # Ensure the path exists
        file = Path(file_path)
        if not file.exists():
            return f"Error: File not found at {file_path}"

        # Read the original content
        original_content = file.read_text()

        # Check if the search block exists
        if search_block not in original_content:
            # If not found, find close matches to help the agent self-correct
            lines = original_content.splitlines()
            search_lines = search_block.splitlines()
            
            # Find the best matching line from the file for the first line of the search block
            close_matches = difflib.get_close_matches(search_lines[0], lines, n=5, cutoff=0.6)
            
            error_message = (
                f"Error: The `search_block` was not found in {file_path}.\n"
                "Here are the closest matching lines from the file to help you correct the `search_block`:\n"
            )
            if close_matches:
                error_message += "\n".join(f"- `{match}`" for match in close_matches)
            else:
                error_message += "No close matches found."
            
            return error_message

        # Perform the replacement (only the first occurrence)
        new_content = original_content.replace(search_block, replace_block, 1)

        # Write the modified content back to the file
        file.write_text(new_content)

        return f"Successfully edited {file_path}."

    except Exception as e:
        return f"An unexpected error occurred: {e}"