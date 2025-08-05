# Playbook: Update Plugin Description

## Objective
Read the plugin profile, understand its current description, and update it with a more detailed and informative description.

## Contextual Prompt Template

You are a plugin documentation improvement agent.
Your working directory is `{working_directory}`.

**Goal:** Read the `plugin-profile.yaml` file to understand the current plugin description, then update it with a more detailed and informative description that better explains the plugin's purpose and functionality. Your final answer should confirm the update and show both the old and new descriptions.

## Steps
1. Use the `read_file` tool to read the contents of `plugin-profile.yaml`
2. Identify the current description in the profile
3. Use the `edit_file` tool to update the description with a more detailed version
4. Use the `read_file` tool again to verify the update was successful
5. Confirm the operation was successful and show the comparison between old and new descriptions

## Notes
- The profile file is located in the plugin root directory
- The description field should be updated with more detailed information
- Preserve all other fields in the profile (name, version, mcp_profile, etc.)
- The new description should be more informative and helpful
- Report both the discovery and update steps in your final response

## Example Description Update
If the current description is "A test plugin", you might update it to:
"A comprehensive test plugin that demonstrates the plugin manager's capabilities for file operations and command execution. This plugin serves as a reference implementation for testing and validation purposes."