# 04 - Virtual Plugin Factory and Evaluation Plan (Refined)

This document specifies the system for generating virtual plugins and using them to evaluate the agent framework and playbooks.

## 1. Core Concept: The "Process Mock"

A Virtual Plugin is a **Process Mock**. It is a fully self-contained, simulated software component generated from a `plugin-profile.yaml`. Its purpose is not to perform any real work, but to provide a simple, deterministic environment for an agent to operate in.

This allows us to test the primary goal of the system: **the agent's ability to correctly follow a playbook.**

## 2. The Plugin Factory

The "Factory" is a script within the Orchestrator framework, likely located at `packages/framework/factory.py`.

### 2.1. Process
1.  **Input:** Takes a path to a directory containing a `plugin-profile.yaml`.
2.  **Scaffolding:** Creates the standard plugin directory structure (`src`, `tests`, `.history`).
3.  **Generate Mock Server:** Creates a generic `src/main.py`. This script is **the same for all virtual plugins**. Its only job is to:
    a. Read the `plugin-profile.yaml` in its directory.
    b. Expose a simple CLI that accepts a `tool_call` name and JSON arguments.
    c. Look up the corresponding scenario in the `behavioral_profile`.
    d. Print the `expected_log` to stdout/stderr and exit.
4.  **Generate Mock Tests:** Creates a `tests/test_virtual.py` that uses the `behavioral_profile` to generate `pytest` test cases for each success and failure scenario.

## 3. The Verification System: The Evaluation Harness

The primary method for testing our system is the **Evaluation Harness**. This is not just for unit tests, but for end-to-end evaluation of playbook execution. It will be located in a dedicated `/evaluations` directory to distinguish it from simple unit tests.

### 3.1. Evaluation Harness Process
An evaluation test will:
1.  Programmatically invoke the Plugin Factory to create a fresh virtual plugin instance for the test.
2.  Invoke the Orchestrator to run a specific playbook on the newly created virtual plugin.
3.  **Capture Events in Memory:** The test will register a listener to the Orchestrator's event system. Instead of writing to a file, it will capture all emitted events (`tool_requested`, `tool_completed`, etc.) in an in-memory list.
4.  **Assert Against Events:** After the Orchestrator finishes, the test will make assertions against the captured sequence of events to verify the agent's behavior was correct.

### 3.2. Example Assertions for a TDD Playbook Evaluation
- Assert that a `tool_requested` event for `execute_shell_command` with `pytest` occurred, and its corresponding `tool_completed` event shows a non-zero exit code.
- Assert that a `tool_requested` event for `edit_file` occurred.
- Assert that a subsequent `tool_requested` event for `execute_shell_command` with `pytest` occurred, and its `tool_completed` event shows an exit code of 0.
- Assert that a `tool_requested` event related to version bumping occurred (e.g., `edit_file` on `plugin-profile.yaml`).
- Assert that a `tool_requested` event for `edit_file` targeting `CHANGE_LOG.md` occurred.

## 4. Tradeoffs and Decisions

- **No Master Profile Directory:** The `/plugin_profiles` directory concept is removed. The `plugin-profile.yaml` is the source of truth and lives within its corresponding plugin directory, for both virtual and real plugins. The factory will operate on a template profile provided to it.
- **In-Memory Event Capture for Tests:** For evaluations, capturing events in memory is more efficient and cleaner than reading and parsing a log file from disk. The file-based `execution_trace.jsonl` is the output for manual runs, while the in-memory capture is for automated evaluations.
- **Dedicated `/evaluations` Directory:** This clarifies the distinction between low-level unit tests for the framework's internal logic (`packages/framework/tests`) and high-level, end-to-end tests of the agent's behavior (`/evaluations`).
