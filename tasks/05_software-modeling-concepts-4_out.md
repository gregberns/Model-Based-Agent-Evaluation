# The Virtual Plugin: A Blueprint for Agent-Driven Development (v4)

This document clarifies the final, critical details of the framework architecture, focusing on project structure and the mechanism for verifying agent actions through a unified playbook system.

## 1. Refined Project Structure

To follow idiomatic Python practices and maintain a clean separation of concerns, we will adopt the following project structure.

```
/poc-plugin-manager/
├── packages/
│   └── framework/
│       ├── __init__.py
│       ├── __main__.py         # Main CLI entrypoint
│       ├── orchestrator.py     # The core logic that runs playbooks and logs events
│       ├── schema.py           # Pydantic schemas for plugin-profile.yaml
│       └── ...
│
├── playbooks/
│   ├── playbook_tdd.md         # A single, high-level TDD playbook
│   └── playbook_fix_bug.md     # A single, high-level bug fix playbook
│
├── plugin_profiles/
│   └── image_processor.yaml    # The "master" profile for the image processor
│
├── plugins_virtual/
│   └── # Populated by the Plugin Factory for testing
│
└── plugins_real/
    └── # Populated by agents running playbooks on real code
```

-   **`packages/framework`**: The core application logic lives here. This is the engine that drives everything.
-   **`playbooks/`**: This top-level directory holds the **single, canonical set of playbooks** that are used for *both* virtual and real plugins.
-   **`plugin_profiles/`**: This directory contains the master `plugin-profile.yaml` files, which act as the initial blueprints for generating virtual plugins or bootstrapping real ones.

## 2. The Framework as Orchestrator and Logger

This is the key to understanding how agent actions are verified. The agent (e.g., Gemini CLI) is a powerful tool, but it operates within a larger system—our framework. The framework is the **Orchestrator**.

**The agent itself does not log anything.** The Orchestrator is responsible for two things:
1.  Giving the agent instructions from the playbook.
2.  Wrapping and observing all actions the agent takes that affect the environment.

When a playbook step says, "Run the test suite," the Orchestrator does the following:
1.  It sees the instruction.
2.  It invokes the agent with a tool like `run_shell_command("pytest")`.
3.  The `run_shell_command` tool executes, and the Orchestrator captures its entire result (stdout, stderr, exit code).
4.  The Orchestrator then writes a `command_run` event to the `execution_trace.jsonl` file with all the captured details.
5.  Finally, it passes the result back to the agent to inform its next step.

This means the agent can operate naturally, without any knowledge of the logging system. The framework transparently records its actions, creating the verifiable trace we need. The agent simply executes its task, and the framework acts as the "black box" flight recorder.

## 3. The Unified Playbook: One Playbook, Two Environments

The most critical concept is this: **the playbooks are identical for both virtual and real plugins.** We do not have a "virtual playbook" and a "real playbook." We have one `playbook_fix_bug.md`, and it works everywhere.

This is achieved by writing playbooks with **high-level, implementation-agnostic instructions.**

Consider the following instruction from `playbook_fix_bug.md`:

> **Instruction:** "A user reports that processing a zero-byte file incorrectly returns an 'InvalidFile' error. The desired behavior is for it to be handled gracefully, logging a warning and returning a default placeholder output. Your task is to write a failing test that reproduces this bug, then implement the necessary code changes to make the test pass."

Here is how a capable agent would interpret this **single instruction** in our two different environments:

---

### **Scenario A: The Virtual Environment**

1.  **Analyze Code:** The agent inspects the virtual plugin's `src/main.py`. It sees that the code is just a simple script that reads `plugin-profile.yaml` and uses a `match` statement on the input to decide which `behavioral_profile` scenario to simulate. There is no "real" logic.
2.  **Deduce Action:** The agent correctly deduces that the *only way* to "implement the necessary code changes" in this environment is to modify the `plugin-profile.yaml` itself. The source code is just a dumb interpreter of the profile.
3.  **Execute Playbook:**
    *   **Write Test:** The agent adds a test case that calls the tool with a zero-byte file and asserts that it does *not* receive an `InvalidFile` error. It runs `pytest`, and the Orchestrator logs that the test fails as expected.
    *   **"Fix" the Bug:** The agent edits the `plugin-profile.yaml`. It finds the `failure_scenarios` entry for this case and moves it to `success_scenarios`, updating the `expected_log` to the new desired warning message. The Orchestrator logs this `file_write` event.
    *   **Verify Fix:** The agent runs `pytest` again. The test now passes because the virtual plugin's code reads the modified profile and simulates the new "success" outcome. The Orchestrator logs the successful test run.

---

### **Scenario B: The Real Environment**

1.  **Analyze Code:** The agent inspects the real plugin's `src/main.py` and its imported modules (e.g., `src/image_logic.py`). It sees complex, real code for image processing.
2.  **Deduce Action:** The agent correctly deduces that to fix the bug, it must modify the Python source code itself to handle the zero-byte file edge case.
3.  **Execute Playbook:**
    *   **Write Test:** The agent adds a test case that creates a temporary zero-byte file, calls the image processing function, and asserts that it does not raise an `InvalidFile` exception. It runs `pytest`, and the Orchestrator logs the failing test.
    *   **Fix the Bug:** The agent edits `src/image_logic.py`. It adds a conditional check at the beginning of the function, like `if os.path.getsize(file_path) == 0:`. The Orchestrator logs this `file_write` event.
    *   **Verify Fix:** The agent runs `pytest` again. The test now passes because the real code handles the condition. The Orchestrator logs the successful test run.

---

### **Conclusion**

The playbook is the same. The agent's goal is the same. The *only* thing that changes is the agent's execution path based on the environment it finds itself in.

By testing the agent's ability to follow the high-level playbook in the simple, deterministic **virtual environment**, we gain high confidence that it can follow the **exact same playbook** in the complex real world. We are evaluating the agent's reasoning and process-following capabilities, which are transferable across both contexts.
