# Playbook: Command and Capture Output

## Objective
Execute a shell command and capture its output by reading it from a file.

## Contextual Prompt Template

You are a command execution and output capture agent.
Your working directory is `{working_directory}`.

**Goal:** Execute the command `echo "Command output test" > command_output.txt` to create a file with command output, then read and display the contents of that file. Your final answer should confirm that the command was executed successfully and show the captured output.

## Steps
1. Use the `execute_shell_command` tool to run `echo "Command output test" > command_output.txt`
2. Use the `list_files` tool to verify that `command_output.txt` was created
3. Use the `read_file` tool to read the contents of `command_output.txt`
4. Confirm the operation was successful and show the captured output

## Notes
- The echo command creates a file with the specified content
- The output file should be created in the current working directory
- Verify the file exists before attempting to read it
- Report both the command execution and output reading in your final response