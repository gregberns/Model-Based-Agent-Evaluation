# evaluations/agent/__init__.py

"""
Agent/Playbook Tests for Plugin Manager

This directory contains end-to-end agent and playbook tests for the plugin manager.
These tests:

- Focus on agent reasoning and playbook execution
- Require API key and are non-deterministic
- Test multi-step workflows and context handling
- Validate agent decision-making and tool orchestration
- Use the full orchestrator with Gemini agent integration

Test Naming Convention:
- test_playbook_<name>.py - Tests for specific playbook execution
- test_agent_<capability>.py - Tests for agent reasoning capabilities

Example: test_playbook_copy_file.py tests the copy_file playbook execution
"""
