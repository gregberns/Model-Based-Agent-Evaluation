# 03 - Agent Playbooks Plan

This document specifies the design and function of Agent Playbooks.

## 1. Core Concept

An Agent Playbook is a version-controlled markdown file that contains a high-level, implementation-agnostic goal for an AI Agent to achieve. Playbooks define the "what" and "why," leaving the "how" to the agent's reasoning capabilities.

There is a **single, canonical set of playbooks** stored in the root `/playbooks` directory. These same playbooks are used for tasks in both the `virtual` and `real` plugin environments.

## 2. Playbook Structure

A playbook is a simple markdown file with two main sections:

1.  **Objective:** A clear, concise statement of the overall goal.
2.  **Contextual Prompts:** A template for the initial prompt that the Orchestrator will send to the Agent. This template will have placeholders for environment-specific information.

### Example: `playbooks/playbook_fix_bug.md`
```markdown
# Playbook: Fix a Bug

## Objective
To identify, test, and resolve a bug in a plugin, following a Test-Driven Development (TDD) methodology.

## Contextual Prompt Template

You are an expert software engineer operating in a **{environment} Environment**.
Your working directory is `{working_directory}`.

**Goal:** A user has reported the following bug: "{bug_description}".
Your task is to resolve this bug. You must follow these steps:
1.  Write a single new test that fails because of the bug.
2.  Run the test suite to confirm the new test fails and all other tests pass.
3.  Modify the system to make the new test pass.
4.  Run the test suite again to confirm all tests now pass.
5.  Increment the plugin's version according to Semantic Versioning.
6.  Update the `CHANGE_LOG.md` with a description of the fix.

**IMPORTANT CONTEXT FOR {environment} ENVIRONMENT:**
{environment_specific_instructions}
```

## 3. Context Injection by the Orchestrator

The power of the unified playbook system comes from the Orchestrator's role in injecting context. Before starting a playbook, the Orchestrator will populate the placeholders in the prompt template.

- **`{environment}`:** Will be replaced with either "Virtual" or "Real".
- **`{working_directory}`:** The absolute path to the plugin being worked on.
- **`{bug_description}`:** The specific details of the bug to be fixed.
- **`{environment_specific_instructions}`:** This is the most critical part. The Orchestrator will inject a different set of instructions based on the environment.
    - **For Virtual:** "To modify the behavior of a Virtual Plugin, you must edit the `plugin-profile.yaml` file..."
    - **For Real:** "To fix this bug, you must modify the Python source code in the `src/` directory..."

## 4. Tradeoffs and Decisions

- **High-Level vs. Low-Level Instructions:** Playbooks are intentionally high-level. We are not scripting the agent's every move. This approach tests the agent's reasoning ability. If the agent cannot follow these high-level steps, the abstraction is wrong, and we need to adjust the playbook or the agent's capabilities.
- **Markdown for Playbooks:** Markdown is used for its readability and ease of version control. It is the perfect format for storing what are essentially complex, templated prompts.
- **Unified Playbooks:** The decision to use a single set of playbooks is a core architectural principle. It forces us to test the agent's true reasoning capabilities in a controlled environment, giving us high confidence that the same reasoning will apply in the real world. It prevents "teaching to the test" where a virtual-only playbook wouldn't be representative of a real task.
