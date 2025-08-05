# evaluations/test_list_files_isolated.py

import pytest
import tempfile
import os
from pathlib import Path

from packages.plugin_manager_agent.tools.list_files import list_files

class TestListFilesIsolated:
    """Isolated tests for the list_files tool functionality."""

    def test_list_current_directory(self):
        """Test listing files in the current directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            original_cwd = os.getcwd()
            os.chdir(temp_dir)

            # Create some test files and directories
            (Path(temp_dir) / "file1.txt").write_text("content1")
            (Path(temp_dir) / "file2.py").write_text("content2")
            (Path(temp_dir) / "subdir").mkdir()
            (Path(temp_dir) / "subdir" / "nested.txt").write_text("nested")

            try:
                result = list_files(".")

                # Should contain our created items
                assert "file1.txt" in result
                assert "file2.py" in result
                assert "subdir" in result
            finally:
                os.chdir(original_cwd)

    def test_list_specific_directory(self):
        """Test listing files in a specific directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create test directory structure
            test_dir = Path(temp_dir) / "test_dir"
            test_dir.mkdir()

            (test_dir / "file1.txt").write_text("content1")
            (test_dir / "file2.py").write_text("content2")
            (test_dir / "subdir").mkdir()

            # Also create files in temp_dir to ensure they don't appear
            (Path(temp_dir) / "other_file.txt").write_text("other")

            result = list_files(str(test_dir))

            # Should only contain items from test_dir
            assert "file1.txt" in result
            assert "file2.py" in result
            assert "subdir" in result
            assert "other_file.txt" not in result

    def test_list_empty_directory(self):
        """Test listing an empty directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = list_files(str(temp_dir))
            # Should return empty string or just the directory listing
            assert result == "" or result.strip() == ""

    def test_list_nonexistent_directory(self):
        """Test listing a non-existent directory."""
        nonexistent_path = "/path/that/does/not/exist"
        result = list_files(nonexistent_path)
        # The function returns empty string for non-existent directories
        assert result == ""

    def test_list_directory_with_various_files(self):
        """Test listing directory with different types of files."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create various files
            test_files = [
                "README.md",
                "config.json",
                "main.py",
                "test.txt",
                "data.csv",
                "script.sh",
                "Dockerfile",
                ".gitignore",
                "requirements.txt"
            ]

            for filename in test_files:
                (Path(temp_dir) / filename).write_text(f"content of {filename}")

            result = list_files(str(temp_dir))

            # All files should be listed
            for filename in test_files:
                assert filename in result

    def test_list_directory_with_spaces_in_name(self):
        """Test listing directory with spaces in the name."""
        with tempfile.TemporaryDirectory() as temp_dir:
            space_dir = Path(temp_dir) / "directory with spaces"
            space_dir.mkdir()

            (space_dir / "file.txt").write_text("content")

            result = list_files(str(space_dir))

            assert "file.txt" in result

    def test_list_nested_directories(self):
        """Test listing directories with nested structure."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create nested structure
            (Path(temp_dir) / "level1").mkdir()
            (Path(temp_dir) / "level1" / "level2").mkdir()
            (Path(temp_dir) / "level1" / "level2" / "level3").mkdir()

            (Path(temp_dir) / "level1" / "file1.txt").write_text("content1")
            (Path(temp_dir) / "level1" / "level2" / "file2.txt").write_text("content2")
            (Path(temp_dir) / "level1" / "level2" / "level3" / "file3.txt").write_text("content3")

            result = list_files(str(Path(temp_dir) / "level1"))

            # Should list level2 directory and file1.txt
            assert "level2" in result
            assert "file1.txt" in result
            assert "file2.txt" not in result  # Should not list nested files

    def test_list_hidden_files(self):
        """Test listing directory with hidden files."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create hidden and regular files
            (Path(temp_dir) / ".hidden").write_text("hidden content")
            (Path(temp_dir) / "regular.txt").write_text("regular content")
            (Path(temp_dir) / ".gitignore").write_text("git ignore")

            result = list_files(str(temp_dir))

            # Should list hidden files as well
            assert ".hidden" in result
            assert ".gitignore" in result
            assert "regular.txt" in result

    def test_list_large_directory(self):
        """Test listing a directory with many files."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create many files
            for i in range(100):
                (Path(temp_dir) / f"file_{i:03d}.txt").write_text(f"content {i}")

            result = list_files(str(temp_dir))

            # Should contain all files
            for i in range(100):
                assert f"file_{i:03d}.txt" in result

    def test_list_relative_path(self):
        """Test listing using relative path from current directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            original_cwd = os.getcwd()
            os.chdir(temp_dir)

            # Create subdirectory and file
            subdir = Path("subdir")
            subdir.mkdir()
            (subdir / "test.txt").write_text("content")

            try:
                result = list_files("subdir")
                assert "test.txt" in result
            finally:
                os.chdir(original_cwd)

    def test_list_absolute_path(self):
        """Test listing using absolute path."""
        with tempfile.TemporaryDirectory() as temp_dir:
            test_file = Path(temp_dir) / "absolute_test.txt"
            test_file.write_text("content")

            result = list_files(str(temp_dir))

            assert "absolute_test.txt" in result

    def test_list_format_consistency(self):
        """Test that the format is consistent and readable."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create files with different names
            test_files = ["a.txt", "b.py", "c.md", "1.json", "2.yaml"]

            for filename in test_files:
                (Path(temp_dir) / filename).write_text("content")

            result = list_files(str(temp_dir))

            # Each file should be on its own line
            lines = result.strip().split('\n')
            assert len(lines) == len(test_files)

            # All files should be present
            for filename in test_files:
                assert filename in result

    def test_list_files_only_no_directories(self):
        """Test that the function lists both files and directories."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create both files and directories
            (Path(temp_dir) / "file1.txt").write_text("content")
            (Path(temp_dir) / "subdir").mkdir()
            (Path(temp_dir) / "subdir" / "nested.txt").write_text("nested")

            result = list_files(str(temp_dir))

            # Should list both files and directories
            assert "file1.txt" in result
            assert "subdir" in result
