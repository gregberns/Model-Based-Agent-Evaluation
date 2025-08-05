# Virtual Plugin Example: Image Processor

This example demonstrates how a Virtual Plugin works as a "Process Mock" to test AI agent behavior.

## What is a Virtual Plugin?

A Virtual Plugin is **NOT** a real implementation. It's a **behavioral blueprint** that defines how a plugin should respond to various inputs. This allows us to test AI agents safely without needing complex, real-world code.

## Plugin Profile Structure

The `plugin-profile.yaml` defines the plugin's behavioral profile:

```yaml
name: "image-processor"
version: "1.0.0"
description: "Virtual image processing plugin for testing agent behavior"
mcp_profile: []

behavioral_profile:
  success_scenarios:
    - description: "Successfully resize a normal image"
      tool_call: "resize_image"
      inputs: { source_file: "images/photo.jpg", width: 800, height: 600 }
      expected_log: "INFO: Image resized to 800x600"
      
    - description: "Apply watermark to image"
      tool_call: "apply_watermark"
      inputs: { source_file: "images/photo.jpg", text: "© 2025" }
      expected_log: "INFO: Watermark applied"
      
  failure_scenarios:
    - description: "Resize a zero-byte file causes an error"
      tool_call: "resize_image"
      inputs: { source_file: "test_data/empty.png", width: 800, height: 600 }
      expected_error: "InvalidFile"
      expected_log: "ERROR: File is empty or corrupted"
```

## Virtual Plugin Implementation

The virtual plugin itself is a simple script that reads the profile and simulates behavior:

```python
# src/main.py (Virtual Plugin)
import yaml
import sys
from pathlib import Path

def main():
    # Load the behavioral profile
    profile_path = Path(__file__).parent / "plugin-profile.yaml"
    with open(profile_path, 'r') as f:
        profile = yaml.safe_load(f)
    
    # Simulate tool execution based on behavioral profile
    for scenario in profile.get('behavioral_profile', {}).get('success_scenarios', []):
        print(scenario['expected_log'])
    
    for scenario in profile.get('behavioral_profile', {}).get('failure_scenarios', []):
        print(scenario['expected_log'])
        if scenario.get('expected_error'):
            print(f"ERROR: {scenario['expected_error']}")

if __name__ == "__main__":
    main()
```

## How AI Agents Interact with Virtual Plugins

### Scenario: Fixing the "Empty File" Bug

**1. Initial State (Bug Exists)**
The virtual plugin has a failure scenario for empty files:

```yaml
failure_scenarios:
  - description: "Resize a zero-byte file causes an error"
    tool_call: "resize_image"
    inputs: { source_file: "test_data/empty.png", width: 800, height: 600 }
    expected_error: "InvalidFile"
    expected_log: "ERROR: File is empty or corrupted"
```

**2. Agent Receives Playbook**
The agent gets a playbook like:

```markdown
# Playbook: Fix Empty File Bug

## Objective
Fix the bug where resizing zero-byte files causes an error.

## Steps
1. Read the plugin profile to understand the current behavior
2. Modify the profile to handle empty files gracefully
3. Verify the fix works by checking the updated behavior
```

**3. Agent Takes Action**
The agent doesn't write real code. Instead, it **modifies the behavioral profile**:

```yaml
# Updated plugin-profile.yaml
success_scenarios:
  - description: "Resize empty file by returning placeholder"
    tool_call: "resize_image"
    inputs: { source_file: "test_data/empty.png", width: 800, height: 600 }
    expected_log: "INFO: Empty file detected, returning placeholder"

failure_scenarios:
  # This scenario is removed - the bug is "fixed"!
```

**4. Verification**
The test harness runs the virtual plugin again and confirms:
- The old failure scenario no longer occurs
- The new success scenario works correctly
- The agent's "fix" is validated

## Why This Approach Works

### Tests Agent Process, Not Code
- **Traditional**: Tests if code implementation works
- **Virtual Plugin**: Tests if agent follows correct processes

### Safe and Fast
- No complex dependencies needed
- Fast execution for rapid testing
- No risk of breaking real systems

### Validates Real Skills
- Reading and modifying configuration files
- Understanding error conditions
- Implementing version management
- Updating documentation

### Scales to Real Plugins
The same agent skills used on virtual plugins work directly on real plugins:
- Reading real codebases
- Making actual code changes
- Managing real version numbers
- Updating real CHANGELOG files

## Testing with Execution Traces

The system records agent actions to verify correct playbook execution:

```json
// .history/execution_trace.jsonl
{"event": "file_write", "path": "plugin-profile.yaml", "timestamp": "2025-01-15T10:30:00Z"}
{"event": "version_change", "old": "1.0.0", "new": "1.0.1", "timestamp": "2025-01-15T10:30:01Z"}
{"event": "file_write", "path": "CHANGELOG.md", "timestamp": "2025-01-15T10:30:02Z"}
```

This creates deterministic tests that validate agent behavior, making the entire system robust and reliable.