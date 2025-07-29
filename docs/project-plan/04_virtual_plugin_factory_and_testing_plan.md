# 04 - Virtual Plugin Factory and Testing Plan

This document specifies the system for generating virtual plugins and using them to test the agent framework and playbooks.

## 1. Core Concept: The "Process Mock"

A Virtual Plugin is a **Process Mock**. It is a fully self-contained, simulated software component generated from a `plugin-profile.yaml`. Its purpose is not to perform any real work, but to provide a simple, deterministic environment for an agent to operate in.

This allows us to test the primary goal of the system: **the agent's ability to correctly follow a playbook.**

## 2. The Plugin Factory

The "Factory" is a script within the Orchestrator framework, executed via a `Makefile` command (e.g., `make generate-virtual-plugin PROFILE=my-plugin`).

### 2.1. Process
1.  **Input:** Takes the path to a master `plugin-profile.yaml` from the `/plugin_profiles` directory.
2.  **Scaffolding:** Creates a new directory in `/plugins_virtual/my-plugin/`.
3.  **Copy Profile:** Copies the master profile into the new directory.
4.  **Generate Mock Server:** Creates a generic `src/main.py`. This script is **the same for all virtual plugins**. Its only job is to:
    a. Read the `plugin-profile.yaml` in its directory.
    b. Expose a simple CLI that accepts a `tool_call` name and JSON arguments.
    c. Look up the corresponding scenario in the `behavioral_profile`.
    d. Print the `expected_log` to stdout/stderr and exit.
5.  **Generate Mock Tests:** Creates a `tests/test_virtual.py` that uses the `behavioral_profile` to generate `pytest` test cases for each success and failure scenario.

## 3. The Verification System: The "Execution Trace"

The primary output of a playbook run in a virtual environment is the **Execution Trace** (`.history/execution_trace.jsonl`). This file is a log of every action the agent requested and the result of that action.

### 3.1. Test Harness
A separate test harness (e.g., `pytest packages/framework/tests/test_playbooks.py`) will be responsible for verifying the correctness of a playbook execution.

The test harness will:
1.  Invoke the Orchestrator to run a specific playbook (e.g., `playbook_fix_bug.md`) on a freshly generated virtual plugin.
2.  After the Orchestrator finishes, the test harness will parse the resulting `execution_trace.jsonl`.
3.  It will then make assertions against the sequence of events in the trace.

### 3.2. Example Assertions for a TDD Playbook Test
- Assert that a `tool_requested` event for `run_shell_command` with `pytest` occurred, and the corresponding `tool_completed` event shows a non-zero exit code.
- Assert that a `tool_requested` event for `PatchFile` occurred.
- Assert that a subsequent `tool_requested` event for `run_shell_command` with `pytest` occurred, and the `tool_completed` event shows an exit code of 0.
- Assert that a `tool_requested` event related to version bumping occurred.
- Assert that a `tool_requested` event for `WriteFile` targeting `CHANGE_LOG.md` occurred.

## 4. Tradeoffs and Decisions

- **Generated Mocks vs. Real Code:** The decision to use a generic, generated mock server is crucial. It ensures that the agent *must* interact with the `plugin-profile.yaml` to change behavior, as there is no other logic to modify. This creates a simple, deterministic environment for testing the agent's core reasoning.
- **JSONL for Traces:** JSON Lines (`.jsonl`) is chosen for the execution trace format because it is a structured, append-only format that is easy for both machines and humans to read.
- **Separate Test Harness:** The verification logic is kept separate from the Orchestrator. The Orchestrator's only job is to run playbooks and log events. The test harness's only job is to analyze those logs. This separation of concerns keeps the framework clean.
