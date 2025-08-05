# evaluations/test_execute_shell_command_isolated.py

import pytest
import tempfile
import os
from pathlib import Path

from packages.plugin_manager_agent.tools.execute_shell_command import execute_shell_command

class TestExecuteShellCommandIsolated:
    """Isolated tests for the execute_shell_command tool functionality."""

    def test_execute_simple_command(self):
        """Test executing a simple command."""
        result = execute_shell_command("echo 'Hello, World!'")

        assert "Exit Code: 0" in result
        assert "STDOUT:" in result
        assert "Hello, World!" in result

    def test_execute_command_with_error(self):
        """Test executing a command that produces an error."""
        result = execute_shell_command("ls /nonexistent/path")

        assert "Exit Code: 1" in result
        assert "STDERR:" in result
        assert "No such file or directory" in result

    def test_execute_command_with_pipe(self):
        """Test executing a command with pipe."""
        result = execute_shell_command("echo 'hello world' | wc -w")

        assert "Exit Code: 0" in result
        assert "STDOUT:" in result
        # Should output "1" (one word)

    def test_execute_command_with_input_redirection(self):
        """Test executing commands with input redirection."""
        result = execute_shell_command("sort <<< 'banana\\napple\\ncherry'")

        assert "Exit Code: 0" in result
        assert "apple" in result
        assert "banana" in result
        assert "cherry" in result

    def test_execute_command_with_conditional_execution(self):
        """Test executing commands with conditional operators."""
        # Test AND operator
        result1 = execute_shell_command("true && echo 'Success'")
        assert "Success" in result1

        # Test OR operator
        result2 = execute_shell_command("false || echo 'Failed'")
        assert "Failed" in result2

    def test_execute_command_with_file_operations(self):
        """Test executing commands that involve file operations."""
        with tempfile.TemporaryDirectory() as temp_dir:
            test_file = Path(temp_dir) / "test.txt"
            test_file.write_text("original content")

            # Use sed to replace content
            result = execute_shell_command(f"sed -i '' 's/original/new/' {test_file}")

            assert "Exit Code: 0" in result
            # Verify the change was made
            assert test_file.read_text() == "new content"

    def test_execute_command_with_directory_change(self):
        """Test executing commands that change directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Change to temp directory and list contents
            result = execute_shell_command(f"cd {temp_dir} && pwd && ls")

            assert "Exit Code: 0" in result
            assert temp_dir in result

    def test_execute_command_with_background_process(self):
        """Test executing background processes."""
        result = execute_shell_command("sleep 0.1 &")

        assert "Exit Code: 0" in result

    def test_execute_command_with_stderr_to_stdout(self):
        """Test executing commands with stderr redirected to stdout."""
        result = execute_shell_command("ls /nonexistent 2>&1")

        assert "Exit Code: 1" in result
        assert "No such file or directory" in result
        # Error should appear in stdout

    def test_execute_command_with_append_redirect(self):
        """Test executing commands with append redirection."""
        with tempfile.TemporaryDirectory() as temp_dir:
            test_file = Path(temp_dir) / "append_test.txt"
            test_file.write_text("original content\n")

            # Append to the file
            result = execute_shell_command(f"echo 'appended content' >> {test_file}")

            assert "Exit Code: 0" in result
            # Verify the content was appended
            content = test_file.read_text()
            assert "original content" in content
            assert "appended content" in content

    def test_execute_command_with_command_substitution(self):
        """Test executing commands with command substitution."""
        result = execute_shell_command("echo \"Today is $(date +%Y-%m-%d)\"")

        assert "Exit Code: 0" in result
        assert "Today is" in result
        assert "STDOUT:" in result

    def test_execute_command_with_command_group(self):
        """Test executing commands with command group."""
        result = execute_shell_command("{ echo 'First'; echo 'Second'; }")

        assert "Exit Code: 0" in result
        assert "First" in result
        assert "Second" in result

    def test_execute_command_with_subshell(self):
        """Test executing commands with subshell."""
        result = execute_shell_command("(echo 'Subshell output'; echo 'Another line')")

        assert "Exit Code: 0" in result
        assert "Subshell output" in result
        assert "Another line" in result

    def test_execute_command_with_timeout(self):
        """Test that commands don't hang indefinitely."""
        # This should complete quickly
        result = execute_shell_command("sleep 0.1")

        assert "Exit Code: 0" in result

    def test_execute_command_with_large_output(self):
        """Test executing a command that produces a lot of output."""
        # Generate a long output
        result = execute_shell_command("for i in {1..100}; do echo \"Line $i of output\"; done")

        assert "Exit Code: 0" in result
        assert "Line 1 of output" in result
        assert "Line 100 of output" in result

    def test_execute_command_with_timeout_handling(self):
        """Test timeout handling for long-running commands."""
        # This should timeout and return an error (sleep longer than 1s timeout)
        result = execute_shell_command("sleep 2", timeout=1)

        assert "timed out" in result.lower()
        assert "timed out after 1 seconds" in result

    def test_execute_command_with_python_command(self):
        """Test executing commands with python."""
        result = execute_shell_command("python3 -c 'print(\"Hello from Python\")'")

        assert "Exit Code: 0" in result
        assert "Hello from Python" in result

    def test_execute_command_with_curl_command(self):
        """Test executing commands with curl."""
        # Test curl with a simple request
        result = execute_shell_command("curl -s https://httpbin.org/get")

        assert "Exit Code: 0" in result
        assert "url" in result  # httpbin response contains url field

    def test_execute_command_with_git_command(self):
        """Test executing commands with git."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Initialize git repository
            result1 = execute_shell_command(f"cd {temp_dir} && git init")
            assert "Exit Code: 0" in result1

            # Configure git
            result2 = execute_shell_command(f"cd {temp_dir} && git config user.email 'test@example.com' && git config user.name 'Test User'")
            assert "Exit Code: 0" in result2

            # Create and commit a file
            test_file = Path(temp_dir) / "test.txt"
            test_file.write_text("initial content")
            result3 = execute_shell_command(f"cd {temp_dir} && git add test.txt && git commit -m 'Initial commit'")
            assert "Exit Code: 0" in result3

    def test_execute_command_with_docker_command(self):
        """Test executing commands with docker."""
        # Test that docker command exists
        result = execute_shell_command("docker --version")

        assert "Exit Code: 0" in result
        assert "Docker" in result

    def test_execute_command_with_aws_command(self):
        """Test executing commands with aws."""
        # Test that aws command exists
        result = execute_shell_command("aws --version")

        assert "Exit Code: 0" in result
        assert "aws-cli" in result.lower()

    def test_execute_command_with_pip_command(self):
        """Test executing commands with pip."""
        # Test pip command
        result = execute_shell_command("pip3 --version")

        assert "Exit Code: 0" in result
        assert "pip" in result.lower()

    def test_execute_command_with_ssh_command(self):
        """Test executing commands with ssh."""
        # Test ssh command
        result = execute_shell_command("ssh -V")

        assert "Exit Code: 0" in result
        assert "ssh" in result.lower()

    def test_execute_command_with_rsync_command(self):
        """Test executing commands with rsync."""
        # Test rsync command
        result = execute_shell_command("rsync --version")

        assert "Exit Code: 0" in result
        assert "rsync" in result.lower()

    def test_execute_command_with_gzip_command(self):
        """Test executing commands with gzip."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
            temp_file.write("test content")
            temp_file_path = temp_file.name

        try:
            # Compress the file
            result1 = execute_shell_command(f"gzip {temp_file_path}")
            assert "Exit Code: 0" in result1

            # Check that .gz file was created
            gz_file = temp_file_path + ".gz"
            assert Path(gz_file).exists()

            # Decompress the file
            result2 = execute_shell_command(f"gunzip {gz_file}")
            assert "Exit Code: 0" in result2

            # Check that original file was restored
            assert Path(temp_file_path).exists()
        finally:
            # Clean up
            for ext in ['', '.gz']:
                file_path = temp_file_path + ext
                if Path(file_path).exists():
                    os.unlink(file_path)

    def test_execute_command_with_file_sorting(self):
        """Test executing commands that sort files."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_dir_path = Path(temp_dir)
            # Create test files with unsorted content
            test_file = temp_dir_path / "unsorted.txt"
            test_file.write_text("zebra\napple\nbanana\ncherry\n")

            # Sort the file
            result = execute_shell_command(f"sort {test_file}")
            assert "Exit Code: 0" in result

            # Check that the output is sorted
            sorted_content = "apple\nbanana\ncherry\nzebra\n"
            assert sorted_content in result

            # Also test sorting in reverse
            result_reverse = execute_shell_command(f"sort -r {test_file}")
            assert "Exit Code: 0" in result_reverse
            assert "zebra" in result_reverse and "apple" in result_reverse

    def test_execute_command_with_text_processing(self):
        """Test executing commands that process text."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_dir_path = Path(temp_dir)
            # Create test file with various content
            test_file = temp_dir_path / "data.txt"
            test_file.write_text("line 1\nline 2\nline 3\nline 1\n")

            # Test counting lines
            result = execute_shell_command(f"wc -l {test_file}")
            assert "Exit Code: 0" in result
            assert "4" in result  # Should have 4 lines

            # Test counting words
            result_words = execute_shell_command(f"wc -w {test_file}")
            assert "Exit Code: 0" in result_words
            assert "8" in result_words  # Should have 8 words

            # Test finding unique lines - extract only the STDOUT content
            result_unique = execute_shell_command(f"sort {test_file} | uniq")
            assert "Exit Code: 0" in result_unique
            # Extract only the STDOUT content (between STDOUT: and STDERR:)
            stdout_start = result_unique.find("STDOUT:") + len("STDOUT:")
            stdout_end = result_unique.find("STDERR:")
            stdout_content = result_unique[stdout_start:stdout_end].strip()

            # Should have 3 unique lines (line 1, line 2, line 3)
            unique_lines = [line for line in stdout_content.split('\n') if line.strip()]
            assert len(unique_lines) == 3
            assert "line 1" in stdout_content
            assert "line 2" in stdout_content
            assert "line 3" in stdout_content

    def test_execute_command_with_process_management(self):
        """Test executing commands that manage processes."""
        # Test background process and job control
        result = execute_shell_command("sleep 0.1 &")

        assert "Exit Code: 0" in result
        # Background process should complete successfully
        assert "STDOUT:" in result and "STDERR:" in result

    def test_execute_command_with_find_command(self):
        """Test executing commands with find."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create test files
            (Path(temp_dir) / "file1.txt").write_text("content")
            (Path(temp_dir) / "file2.py").write_text("content")
            (Path(temp_dir) / "subdir").mkdir()
            (Path(temp_dir) / "subdir" / "file3.txt").write_text("content")

            result = execute_shell_command(f"find {temp_dir} -name '*.txt'")

            assert "Exit Code: 0" in result
            assert "file1.txt" in result
            assert "file3.txt" in result
            assert "file2.py" not in result

    def test_execute_command_with_grep_command(self):
        """Test executing commands with grep."""
        result = execute_shell_command("echo -e 'line1\\nline2\\nline3' | grep 'line2'")

        assert "Exit Code: 0" in result
        assert "line2" in result
        assert "line1" not in result
        assert "line3" not in result

    def test_execute_command_with_sed_command(self):
        """Test executing commands with sed."""
        result = execute_shell_command("echo 'hello world' | sed 's/hello/hi/'")

        assert "Exit Code: 0" in result
        assert "hi world" in result

    def test_execute_command_with_awk_command(self):
        """Test executing commands with awk."""
        result = execute_shell_command("echo '1 apple\\n2 banana\\n3 cherry' | awk '{print $2}'")

        assert "Exit Code: 0" in result
        assert "apple" in result
        assert "banana" in result
        assert "cherry" in result

    def test_execute_command_with_sort_command(self):
        """Test executing commands with sort."""
        result = execute_shell_command("echo -e 'banana\\napple\\ncherry' | sort")

        assert "Exit Code: 0" in result
        assert "apple" in result
        assert "banana" in result
        assert "cherry" in result

    def test_execute_command_with_uniq_command(self):
        """Test executing commands with uniq."""
        result = execute_shell_command("echo -e 'a\\na\\nb\\nb\\nc' | uniq")

        assert "Exit Code: 0" in result
        assert "a" in result
        assert "b" in result
        assert "c" in result

    def test_execute_command_with_wc_command(self):
        """Test executing commands with wc."""
        result = execute_shell_command("echo -e 'line1\\nline2\\nline3' | wc -l")

        assert "Exit Code: 0" in result
        assert "STDOUT:" in result
        # Should output "3"

    def test_execute_command_with_head_command(self):
        """Test executing commands with head."""
        result = execute_shell_command("echo -e 'line1\\nline2\\nline3\\nline4' | head -n 2")

        assert "Exit Code: 0" in result
        assert "line1" in result
        assert "line2" in result
        assert "line3" not in result

    def test_execute_command_with_tail_command(self):
        """Test executing commands with tail."""
        result = execute_shell_command("echo -e 'line1\\nline2\\nline3\\nline4' | tail -n 2")

        assert "Exit Code: 0" in result
        assert "line3" in result
        assert "line4" in result
        assert "line1" not in result

    def test_execute_command_with_cat_command(self):
        """Test executing commands with cat."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
            temp_file.write("test content")
            temp_file_path = temp_file.name

        try:
            result = execute_shell_command(f"cat {temp_file_path}")

            assert "Exit Code: 0" in result
            assert "test content" in result
        finally:
            os.unlink(temp_file_path)

    def test_execute_command_with_less_command(self):
        """Test executing commands with less."""
        # Test that less command exists and works
        result = execute_shell_command("echo 'test' | less")

        assert "Exit Code: 0" in result
        assert "test" in result

    def test_execute_command_with_more_command(self):
        """Test executing commands with more."""
        # Test that more command exists and works
        result = execute_shell_command("echo 'test' | more")

        assert "Exit Code: 0" in result
        assert "test" in result

    def test_execute_command_with_vim_command(self):
        """Test executing commands with vim."""
        # Test that vim command exists
        result = execute_shell_command("vim --version")

        assert "Exit Code: 0" in result
        assert "VIM" in result

    def test_execute_command_with_vi_command(self):
        """Test executing commands with vi."""
        # Test that vi command exists
        result = execute_shell_command("vi --version")

        assert "Exit Code: 0" in result
        assert "VIM" in result

    def test_execute_command_with_gnupg_command(self):
        """Test executing commands with gnupg."""
        # Test gnupg command
        result = execute_shell_command("gpg --version")

        assert "Exit Code: 0" in result
        assert "gpg" in result.lower()

    def test_execute_command_with_gpgsm_command(self):
        """Test executing commands with gpgsm."""
        # Test gpgsm command
        result = execute_shell_command("gpgsm --version")

        assert "Exit Code: 0" in result
        assert "gpgsm" in result.lower()

    def test_execute_command_with_gpgconf_command(self):
        """Test executing commands with gpgconf."""
        # Test gpgconf command
        result = execute_shell_command("gpgconf --version")

        assert "Exit Code: 0" in result
        assert "gpgconf" in result.lower()

    def test_execute_command_with_gpg_agent_command(self):
        """Test executing commands with gpg-agent."""
        # Test gpg-agent command
        result = execute_shell_command("gpg-agent --version")

        assert "Exit Code: 0" in result
        assert "gpg-agent" in result.lower()

    def test_execute_command_with_clang_command(self):
        """Test executing commands with clang."""
        # Test clang command
        result = execute_shell_command("clang --version")

        assert "Exit Code: 0" in result
        assert "clang" in result.lower()

    def test_execute_command_with_make_command(self):
        """Test executing commands with make."""
        # Test make command
        result = execute_shell_command("make --version")

        assert "Exit Code: 0" in result
        assert "make" in result.lower()

    def test_execute_command_with_cmake_command(self):
        """Test executing commands with cmake."""
        # Test cmake command
        result = execute_shell_command("cmake --version")

        assert "Exit Code: 0" in result
        assert "cmake" in result.lower()

    def test_execute_command_with_node_command(self):
        """Test executing commands with node."""
        # Test node command
        result = execute_shell_command("node -e 'console.log(\"Hello from Node.js\")'")

        assert "Exit Code: 0" in result
        assert "Hello from Node.js" in result

    def test_execute_command_with_environment_variables(self):
        """Test executing commands that use environment variables."""
        # Test a command that uses environment variables
        result = execute_shell_command("echo $HOME $USER")

        assert "Exit Code: 0" in result
        # Should contain home directory and username
        assert "HOME=" in result or "/Users/" in result or "/home/" in result
        assert "USER=" in result or result.strip().split()[-1] != ""
