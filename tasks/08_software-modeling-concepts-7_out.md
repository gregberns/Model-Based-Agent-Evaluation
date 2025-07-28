# The Virtual Plugin: A Blueprint for Agent-Driven Development (v7)

This document presents the definitive architecture for agent interaction, resolving the critical challenge of file modification. It is based on your feedback that building a custom, reliable `edit_file` tool is infeasible and that we must use a more robust pattern.

## 1. The Core Problem: The Fragility of "Edit" Tools

You were correct to challenge the assumption that we could build our own agent tools. A simple `edit_file` tool is doomed to fail due to:
*   **Ambiguity:** Replacing a string that appears multiple times.
*   **Context Drift:** After a first edit, line numbers or surrounding context for a second edit become invalid.
*   **Complexity:** A truly robust tool would essentially need to be a programmatic IDE, which is a massive project in itself.

## 2. The Solution: The "Full File Rewrite" Pattern

We will abandon the concept of an "edit" tool entirely. Instead, we will adopt a **Read-Modify-Write** pattern that leverages the large context window of our target model (Gemini 1.5 Pro) and relies on simple, highly reliable tools.

The agent's workflow for modifying a file will be:

1.  **Read:** The agent uses a `read_file(path)` tool to load the entire file's content into its context.
2.  **Modify:** The agent performs the "edit" entirely within its own context window. It reasons about the code and makes the necessary changes to its internal representation of the file.
3.  **Write:** The agent uses a `write_file(path, new_content)` tool to write the **entire, modified content** back to the disk, completely overwriting the original file.

### Why This Architecture is Superior

*   **Eliminates Ambiguity:** There is no ambiguity in a full rewrite. The agent's final, modified text is the new source of truth. This sidesteps all the problems of partial edits.
*   **Uses Simple, Robust Tools:** The only file system tools we need to provide are `read_file` and `write_file`. These can be implemented with near-perfect reliability using Python's standard `pathlib` library. We are not building complex or fragile logic.
*   **Maintains Full Observability:** Our "Observability Wrapper" pattern still works perfectly. The Orchestrator receives the `write_file` request from the agent. Before executing it, the Orchestrator can log the *entire new content*. This gives our `execution_trace.jsonl` a perfect, atomic, before-and-after snapshot of the change.
*   **Leverages Modern LLM Strengths:** This pattern is perfectly suited for models with large context windows. It puts the burden of reasoning about the change on the LLM—which is its core strength—rather than on a brittle tool.

## 3. The "Diff Patch" Pattern (Advanced Alternative)

Should we encounter files that are too large for the context window, or if we want to optimize for token usage, we can adopt a more advanced pattern without changing the core architecture.

1.  **Read:** Agent uses `read_file`.
2.  **Generate Diff:** The agent is prompted to generate a `diff` string in the standard unified format that represents the desired change.
3.  **Apply Patch:** The agent uses an `apply_patch(patch_string)` tool. The Orchestrator implements this tool using a standard Python `patch` library, which is highly reliable.

We will start with the "Full File Rewrite" pattern due to its simplicity and effectiveness, but keep the "Diff Patch" pattern as a viable future enhancement.

## 4. Finalized Tooling Strategy

Our `packages/framework/tools.py` will contain a small, curated set of robust, observable tools:

*   `read_file(path: str) -> str`
*   `write_file(path: str, content: str) -> str`
*   `list_directory(path: str) -> list[str]`
*   `run_shell_command(command: str) -> str`

Each of these functions will be a thin wrapper around Python's standard libraries, containing only the core logic and the calls to our logger to trace their execution. This provides a stable, reliable, and fully observable foundation for our agent framework.
