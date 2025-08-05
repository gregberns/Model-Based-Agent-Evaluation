# Evaluations Directory

This directory contains all tests for the Plugin Manager system, organized into two distinct categories: deterministic tests and agent/playbook tests.

## Directory Structure

```
evaluations/
├── deterministic/          # Unit and integration tests
│   ├── __init__.py
│   ├── test_read_file.py
│   ├── test_write_file.py
│   ├── test_list_files.py
│   ├── test_execute_shell_command.py
│   └── test_edit_file.py
├── agent/                  # End-to-end agent and playbook tests
│   ├── __init__.py
│   ├── test_playbook_copy_file.py
│   ├── test_playbook_fix_bug.py
│   └── test_playbook_list_files.py
├── harness.py              # Evaluation harness utilities
└── __init__.py
```

## Test Categories

### Deterministic Tests (`evaluations/deterministic/`)

These tests focus on validating individual tool functionality in isolation:

- **Purpose**: Unit and integration testing for tools
- **Characteristics**: Fast, reliable, no external dependencies
- **Testing Method**: Direct tool function calls
- **Coverage**: Tool functionality, event emission, error handling, performance
- **Examples**: `test_read_file.py`, `test_write_file.py`

**When to run**: Always, as part of regular development and CI/CD pipeline

**Command**:
```bash
pytest evaluations/deterministic/ -v
```

### Agent/Playbook Tests (`evaluations/agent/`)

These tests focus on validating agent reasoning and playbook execution:

- **Purpose**: End-to-end testing of agent capabilities and workflows
- **Characteristics**: Slower, require API key, non-deterministic
- **Testing Method**: Full orchestrator with Gemini agent integration
- **Coverage**: Agent reasoning, multi-step workflows, context handling
- **Examples**: `test_playbook_copy_file.py`, `test_playbook_fix_bug.py`

**Requirements**: 
- `GEMINI_API_KEY` environment variable set
- Internet connection for API calls

**When to run**: Before releases, when validating new playbooks, or during development

**Command**:
```bash
pytest evaluations/agent/ -v
```

## Running Tests

### All Tests
```bash
make test
```

### Deterministic Tests Only
```bash
pytest evaluations/deterministic/ -v
```

### Agent/Playbook Tests Only
```bash
pytest evaluations/agent/ -v
```

### Specific Test File
```bash
pytest evaluations/deterministic/test_read_file.py -v
pytest evaluations/agent/test_playbook_copy_file.py -v
```

## Test Development Guidelines

### Deterministic Tests
- Test individual tool functionality comprehensively
- Include edge cases and error conditions
- Validate event emission accuracy
- Measure performance for typical use cases
- Use direct function calls, not agent orchestration

### Agent/Playbook Tests
- Test complete workflows from start to finish
- Validate agent reasoning and decision-making
- Test context maintenance between tool calls
- Include realistic scenarios and edge cases
- Use the evaluation harness for consistent testing

## Test Naming Conventions

### Deterministic Tests
- Format: `test_<tool_name>.py`
- Example: `test_read_file.py`

### Agent/Playbook Tests
- Format: `test_playbook_<name>.py` or `test_agent_<capability>.py`
- Example: `test_playbook_copy_file.py`

## Integration with CI/CD

The deterministic tests should run on every commit and pull request as part of the CI pipeline. The agent/playbook tests should run before releases and when validating new playbook functionality.

## Adding New Tests

1. **For new tools**: Add tests to `evaluations/deterministic/` following the naming convention
2. **For new playbooks**: Add tests to `evaluations/agent/` following the naming convention
3. **Use the evaluation harness** for agent tests to ensure consistent execution
4. **Follow the existing test patterns** and maintain code quality standards