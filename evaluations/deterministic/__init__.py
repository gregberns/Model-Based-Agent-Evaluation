# evaluations/deterministic/__init__.py

"""
Deterministic Tests for Plugin Manager Tools

This directory contains deterministic unit and integration tests for the individual
tools used by the plugin manager. These tests:

- Focus on tool functionality in isolation
- Are fast, reliable, and have no external dependencies
- Test edge cases, error handling, and performance
- Validate event emission and tool contracts
- Use direct tool function calls rather than agent orchestration

Test Naming Convention:
- test_<tool_name>.py - Tests for individual tool functionality

Example: test_read_file.py contains tests for the read_file tool
"""
