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