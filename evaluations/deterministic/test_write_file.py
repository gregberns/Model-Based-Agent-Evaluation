# evaluations/test_write_file_isolated.py

import pytest
import tempfile
import os
from pathlib import Path

from packages.plugin_manager_agent.tools.write_file import write_file

class TestWriteFileIsolated:
    """Isolated tests for the write_file tool functionality."""

    def test_write_new_file(self):
        """Test writing to a new file."""
        with tempfile.TemporaryDirectory() as temp_dir:
            test_file = Path(temp_dir) / "new_file.txt"

            result = write_file(str(test_file), "Hello, World!")

            assert result == f"Successfully wrote 13 characters to {test_file}"
            assert test_file.exists()
            assert test_file.read_text() == "Hello, World!"

    def test_write_overwrite_existing_file(self):
        """Test overwriting an existing file."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as temp_file:
            temp_file.write("Original content")
            temp_file_path = temp_file.name

        try:
            result = write_file(temp_file_path, "New content")

            assert result == f"Successfully wrote 11 characters to {temp_file_path}"
            assert Path(temp_file_path).read_text() == "New content"
        finally:
            os.unlink(temp_file_path)

    def test_write_file_with_multiline_content(self):
        """Test writing multiline content."""
        content = """Line 1
Line 2
Line 3"""

        with tempfile.TemporaryDirectory() as temp_dir:
            test_file = Path(temp_dir) / "multiline.txt"

            result = write_file(str(test_file), content)

            assert result == f"Successfully wrote {len(content)} characters to {test_file}"
            assert test_file.read_text() == content

    def test_write_file_with_special_characters(self):
        """Test writing content with special characters and unicode."""
        content = "Special chars: áéíóú 🚀\nNew line\n\tTabbed"

        with tempfile.TemporaryDirectory() as temp_dir:
            test_file = Path(temp_dir) / "special_chars.txt"

            result = write_file(str(test_file), content)

            assert result == f"Successfully wrote {len(content)} characters to {test_file}"
            assert test_file.read_text() == content

    def test_write_file_with_spaces_in_path(self):
        """Test writing to a file with spaces in the path."""
        with tempfile.TemporaryDirectory() as temp_dir:
            test_file = Path(temp_dir) / "test file with spaces.txt"

            result = write_file(str(test_file), "Content with spaces")

            assert result == f"Successfully wrote 19 characters to {test_file}"
            assert test_file.exists()
            assert test_file.read_text() == "Content with spaces"

    def test_write_file_with_nested_directories(self):
        """Test writing to a file in nested directories."""
        with tempfile.TemporaryDirectory() as temp_dir:
            nested_file = Path(temp_dir) / "nested" / "deeply" / "test_file.txt"

            result = write_file(str(nested_file), "Nested content")

            assert result == f"Successfully wrote 14 characters to {nested_file}"
            assert nested_file.exists()
            assert nested_file.read_text() == "Nested content"
            # Verify parent directories were created
            assert (Path(temp_dir) / "nested").exists()
            assert (Path(temp_dir) / "nested" / "deeply").exists()

    def test_write_empty_file(self):
        """Test writing an empty file."""
        with tempfile.TemporaryDirectory() as temp_dir:
            test_file = Path(temp_dir) / "empty.txt"

            result = write_file(str(test_file), "")

            assert result == f"Successfully wrote 0 characters to {test_file}"
            assert test_file.exists()
            assert test_file.read_text() == ""

    def test_write_large_file(self):
        """Test writing a larger file (1MB)."""
        large_content = "A" * (1024 * 1024)  # 1MB of 'A's

        with tempfile.TemporaryDirectory() as temp_dir:
            test_file = Path(temp_dir) / "large_file.txt"

            result = write_file(str(test_file), large_content)

            assert result == f"Successfully wrote {len(large_content)} characters to {test_file}"
            assert test_file.exists()
            assert test_file.read_text() == large_content
            assert test_file.stat().st_size == 1024 * 1024

    def test_write_file_with_different_extensions(self):
        """Test writing files with different extensions."""
        test_cases = [
            ("test.py", "print('Hello Python')"),
            ("test.json", '{"key": "value"}'),
            ("test.md", "# Markdown Header"),
            ("test.yaml", "name: test"),
            ("test.xml", "<root><item>test</item></root>")
        ]

        for filename, content in test_cases:
            with tempfile.TemporaryDirectory() as temp_dir:
                test_file = Path(temp_dir) / filename

                result = write_file(str(test_file), content)

                assert result == f"Successfully wrote {len(content)} characters to {test_file}"
                assert test_file.exists()
                assert test_file.read_text() == content

    def test_write_file_with_invalid_path(self):
        """Test writing to an invalid path."""
        # Try to write to a path with invalid characters (platform dependent)
        invalid_path = "/invalid/path/that/should/not/exist/file?.txt"

        result = write_file(invalid_path, "test content")

        assert "Error writing to file" in result

    def test_write_file_read_back_verification(self):
        """Test writing content and reading it back to verify consistency."""
        original_content = "Original test content\nWith multiple lines\nAnd special chars: áéíóú 🚀"

        with tempfile.TemporaryDirectory() as temp_dir:
            test_file = Path(temp_dir) / "read_back_test.txt"

            # Write the content
            write_result = write_file(str(test_file), original_content)
            assert "Successfully wrote" in write_result

            # Read it back
            from packages.plugin_manager_agent.tools.read_file import read_file
            read_result = read_file(str(test_file))

            # Verify they match
            assert read_result == original_content
