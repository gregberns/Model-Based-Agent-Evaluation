# evaluations/test_read_file_isolated.py

import pytest
import tempfile
import os
from pathlib import Path

from packages.plugin_manager_agent.tools.read_file import read_file

class TestReadFileIsolated:
    """Isolated tests for the read_file tool functionality."""

    def test_read_existing_file(self):
        """Test reading an existing file with simple content."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as temp_file:
            temp_file.write("Hello, World!")
            temp_file_path = temp_file.name

        try:
            result = read_file(temp_file_path)
            assert result == "Hello, World!"
        finally:
            os.unlink(temp_file_path)

    def test_read_file_with_multiline_content(self):
        """Test reading a file with multiline content."""
        content = """Line 1
Line 2
Line 3"""

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as temp_file:
            temp_file.write(content)
            temp_file_path = temp_file.name

        try:
            result = read_file(temp_file_path)
            assert result == content
        finally:
            os.unlink(temp_file_path)

    def test_read_file_with_special_characters(self):
        """Test reading a file with special characters and unicode."""
        content = "Special chars: áéíóú 🚀\nNew line\n\tTabbed"

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt', encoding='utf-8') as temp_file:
            temp_file.write(content)
            temp_file_path = temp_file.name

        try:
            result = read_file(temp_file_path)
            assert result == content
        finally:
            os.unlink(temp_file_path)

    def test_read_nonexistent_file(self):
        """Test reading a non-existent file."""
        nonexistent_path = "/path/that/does/not/exist.txt"
        result = read_file(nonexistent_path)
        assert "Error reading file" in result
        assert "No such file or directory" in result or "does not exist" in result

    def test_read_file_with_spaces_in_path(self):
        """Test reading a file with spaces in the path."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, prefix='test file', suffix='.txt') as temp_file:
            temp_file.write("Content with spaces")
            temp_file_path = temp_file.name

        try:
            result = read_file(temp_file_path)
            assert result == "Content with spaces"
        finally:
            os.unlink(temp_file_path)

    def test_read_file_with_relative_path(self):
        """Test reading a file using relative path."""
        original_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as temp_dir:
            os.chdir(temp_dir)

            test_file = Path("relative_test.txt")
            test_file.write_text("Relative path content")

            try:
                result = read_file("relative_test.txt")
                assert result == "Relative path content"
            finally:
                os.chdir(original_cwd)

    def test_read_empty_file(self):
        """Test reading an empty file."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as temp_file:
            temp_file.write("")
            temp_file_path = temp_file.name

        try:
            result = read_file(temp_file_path)
            assert result == ""
        finally:
            os.unlink(temp_file_path)

    def test_read_large_file(self):
        """Test reading a larger file (1MB)."""
        large_content = "A" * (1024 * 1024)  # 1MB of 'A's

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as temp_file:
            temp_file.write(large_content)
            temp_file_path = temp_file.name

        try:
            result = read_file(temp_file_path)
            assert result == large_content
            assert len(result) == 1024 * 1024
        finally:
            os.unlink(temp_file_path)

    def test_read_file_with_different_extensions(self):
        """Test reading files with different extensions."""
        test_cases = [
            ("test.py", "print('Hello Python')"),
            ("test.json", '{"key": "value"}'),
            ("test.md", "# Markdown Header"),
            ("test.yaml", "name: test"),
            ("test.xml", "<root><item>test</item></root>")
        ]

        for filename, content in test_cases:
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=filename) as temp_file:
                temp_file.write(content)
                temp_file_path = temp_file.name

            try:
                result = read_file(temp_file_path)
                assert result == content
            finally:
                os.unlink(temp_file_path)
