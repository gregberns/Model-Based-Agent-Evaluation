# Playbook: Copy File

## Objective
Copy the content of one file to another file.

## Contextual Prompt Template

You are a file copying agent.
Your working directory is `{working_directory}`.

**Goal:** Copy the content of `source_file.txt` to `destination_file.txt`. Your final answer should confirm that the copy operation was successful and optionally show the first few lines of the copied content.

## Steps
1. Use the `read_file` tool to read the content of `source_file.txt`
2. Use the `write_file` tool to write that content to `destination_file.txt`
3. Confirm the operation was successful