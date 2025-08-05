# evaluations/test_edit_file_isolated.py

import pytest
import tempfile
import os
from pathlib import Path

from packages.plugin_manager_agent.tools.edit_file import edit_file

class TestEditFileIsolated:
    """Isolated tests for the edit_file tool functionality."""

    def test_edit_existing_file_exact_match(self):
        """Test editing an existing file with exact match."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as temp_file:
            temp_file.write("Original content\nLine 2\nLine 3")
            temp_file_path = temp_file.name

        try:
            result = edit_file(
                temp_file_path,
                "Original content\nLine 2\nLine 3",
                "New content\nLine 2 updated\nLine 3"
            )

            assert "Successfully edited" in result
            # Verify the content was changed
            with open(temp_file_path, 'r') as f:
                content = f.read()
                assert content == "New content\nLine 2 updated\nLine 3"
        finally:
            os.unlink(temp_file_path)

    def test_edit_file_partial_match(self):
        """Test editing a file with partial match."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as temp_file:
            temp_file.write("Line 1\nLine 2\nLine 3\nLine 4")
            temp_file_path = temp_file.name

        try:
            result = edit_file(
                temp_file_path,
                "Line 2\nLine 3",
                "Line 2 modified\nLine 3 modified"
            )

            assert "Successfully edited" in result
            # Verify the content was changed
            with open(temp_file_path, 'r') as f:
                content = f.read()
                assert content == "Line 1\nLine 2 modified\nLine 3 modified\nLine 4"
        finally:
            os.unlink(temp_file_path)

    def test_edit_file_single_line(self):
        """Test editing a single line in a file."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as temp_file:
            temp_file.write("Hello World\nGoodbye World")
            temp_file_path = temp_file.name

        try:
            result = edit_file(
                temp_file_path,
                "Hello World",
                "Hello Universe"
            )

            assert "Successfully edited" in result
            # Verify the content was changed
            with open(temp_file_path, 'r') as f:
                content = f.read()
                assert content == "Hello Universe\nGoodbye World"
        finally:
            os.unlink(temp_file_path)

    def test_edit_file_with_special_characters(self):
        """Test editing a file with special characters."""
        content = "Line with special chars: áéíóú 🚀\nAnother line"
        new_content = "Modified special chars: áéíóú 🚀\nAnother line modified"

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt', encoding='utf-8') as temp_file:
            temp_file.write(content)
            temp_file_path = temp_file.name

        try:
            result = edit_file(temp_file_path, content, new_content)

            assert "Successfully edited" in result
            # Verify the content was changed
            with open(temp_file_path, 'r', encoding='utf-8') as f:
                actual_content = f.read()
                assert actual_content == new_content
        finally:
            os.unlink(temp_file_path)

    def test_edit_file_not_found(self):
        """Test editing a non-existent file."""
        nonexistent_path = "/path/that/does/not/exist.txt"
        result = edit_file(
            nonexistent_path,
            "search content",
            "replace content"
        )

        assert "Error: File not found" in result

    def test_edit_file_no_match(self):
        """Test editing a file when search block is not found."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as temp_file:
            temp_file.write("Line 1\nLine 2\nLine 3")
            temp_file_path = temp_file.name

        try:
            result = edit_file(
                temp_file_path,
                "Nonexistent content",
                "Replacement content"
            )

            assert "Error: The `search_block` was not found" in result
            # Verify the file content was not changed
            with open(temp_file_path, 'r') as f:
                content = f.read()
                assert content == "Line 1\nLine 2\nLine 3"
        finally:
            os.unlink(temp_file_path)

    def test_edit_file_multiple_matches(self):
        """Test editing a file when search block appears multiple times."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as temp_file:
            temp_file.write("Repeat\nRepeat\nRepeat")
            temp_file_path = temp_file.name

        try:
            result = edit_file(
                temp_file_path,
                "Repeat",
                "Changed"
            )

            assert "Successfully edited" in result
            # Verify only the first occurrence was changed
            with open(temp_file_path, 'r') as f:
                content = f.read()
                assert content == "Changed\nRepeat\nRepeat"
        finally:
            os.unlink(temp_file_path)

    def test_edit_file_empty_search_block(self):
        """Test editing a file with empty search block."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as temp_file:
            temp_file.write("Content")
            temp_file_path = temp_file.name

        try:
            result = edit_file(
                temp_file_path,
                "",
                "New content"
            )

            # This should work - replacing empty string with content
            assert "Successfully edited" in result
            # Verify the content was changed (empty string replacement prepends)
            with open(temp_file_path, 'r') as f:
                content = f.read()
                assert content == "New contentContent"
        finally:
            os.unlink(temp_file_path)

    def test_edit_file_empty_replace_block(self):
        """Test editing a file by replacing content with empty string."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as temp_file:
            temp_file.write("Line 1\nLine 2\nLine 3")
            temp_file_path = temp_file.name

        try:
            result = edit_file(
                temp_file_path,
                "Line 2",
                ""
            )

            assert "Successfully edited" in result
            # Verify the content was changed
            with open(temp_file_path, 'r') as f:
                content = f.read()
                assert content == "Line 1\n\nLine 3"
        finally:
            os.unlink(temp_file_path)

    def test_edit_file_with_spaces_in_path(self):
        """Test editing a file with spaces in the path."""
        with tempfile.TemporaryDirectory() as temp_dir:
            test_file = Path(temp_dir) / "test file with spaces.txt"
            original_content = "Original content"
            new_content = "New content"

            test_file.write_text(original_content)

            result = edit_file(
                str(test_file),
                original_content,
                new_content
            )

            assert "Successfully edited" in result
            # Verify the content was changed
            assert test_file.read_text() == new_content

    def test_edit_file_with_newlines(self):
        """Test editing a file with multiple newlines."""
        content = "Line 1\n\nLine 3\nLine 4"
        new_content = "Line 1\nModified Line 2\n\nLine 3\nLine 4"

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as temp_file:
            temp_file.write(content)
            temp_file_path = temp_file.name

        try:
            result = edit_file(
                temp_file_path,
                content,
                new_content
            )

            assert "Successfully edited" in result
            # Verify the content was changed
            with open(temp_file_path, 'r') as f:
                actual_content = f.read()
                assert actual_content == new_content
        finally:
            os.unlink(temp_file_path)

    def test_edit_file_close_match_suggestion(self):
        """Test that close matches are suggested when exact match is not found."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as temp_file:
            temp_file.write("Line 1\nLine 2\nLine 3")
            temp_file_path = temp_file.name

        try:
            result = edit_file(
                temp_file_path,
                "Line 22",  # Close but not exact match
                "Replacement"
            )

            assert "Error: The `search_block` was not found" in result
            assert "closest matching lines" in result
            assert "Line 2" in result  # Should suggest Line 2 as close match
        finally:
            os.unlink(temp_file_path)

    def test_edit_file_very_large_content(self):
        """Test editing a file with large content."""
        # Create a file with 10KB of content
        large_content = "Line {}\n".format("A" * 100) * 50  # ~5KB
        new_content = "Modified Line {}\n".format("B" * 100) * 50

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as temp_file:
            temp_file.write(large_content)
            temp_file_path = temp_file.name

        try:
            result = edit_file(
                temp_file_path,
                large_content,
                new_content
            )

            assert "Successfully edited" in result
            # Verify the content was changed
            with open(temp_file_path, 'r') as f:
                content = f.read()
                assert content == new_content
        finally:
            os.unlink(temp_file_path)

    def test_edit_file_unicode_content(self):
        """Test editing a file with unicode content."""
        content = "Unicode test: 你好 🌍 世界\nSpecial: áéíóú 🚀"
        new_content = "Unicode modified: 你好 🌍 修改版\nSpecial: áéíóú 🚀✨"

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt', encoding='utf-8') as temp_file:
            temp_file.write(content)
            temp_file_path = temp_file.name

        try:
            result = edit_file(
                temp_file_path,
                content,
                new_content
            )

            assert "Successfully edited" in result
            # Verify the content was changed
            with open(temp_file_path, 'r', encoding='utf-8') as f:
                actual_content = f.read()
                assert actual_content == new_content
        finally:
            os.unlink(temp_file_path)

    def test_edit_file_consecutive_matches(self):
        """Test editing a file with consecutive identical lines."""
        content = "Line\nLine\nLine"
        new_content = "Modified\nModified\nModified"

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as temp_file:
            temp_file.write(content)
            temp_file_path = temp_file.name

        try:
            result = edit_file(
                temp_file_path,
                content,
                new_content
            )

            assert "Successfully edited" in result
            # Verify the content was changed
            with open(temp_file_path, 'r') as f:
                actual_content = f.read()
                assert actual_content == new_content
        finally:
            os.unlink(temp_file_path)

    def test_edit_file_with_tabs(self):
        """Test editing a file with tab characters."""
        content = "Line 1\tTabbed\nLine 2\tMore tabs"
        new_content = "Modified 1\tTabbed\nLine 2\tMore tabs"

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as temp_file:
            temp_file.write(content)
            temp_file_path = temp_file.name

        try:
            result = edit_file(
                temp_file_path,
                content,
                new_content
            )

            assert "Successfully edited" in result
            # Verify the content was changed
            with open(temp_file_path, 'r') as f:
                actual_content = f.read()
                assert actual_content == new_content
        finally:
            os.unlink(temp_file_path)
