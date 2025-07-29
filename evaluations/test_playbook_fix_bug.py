# evaluations/test_playbook_fix_bug.py

import pytest
import yaml
import os
from pathlib import Path

from evaluations.harness import EvaluationHarness
from packages.framework.factory import PluginFactory
from packages.framework.orchestrator import Orchestrator
from packages.framework.loaders import ProfileLoader, PlaybookLoader
from packages.framework.prompt_constructor import PromptConstructor
from packages.framework.tool_wrapper import wrap_tool
from packages.plugin_manager_agent import GeminiAgent
from packages.plugin_manager_agent.tools import TOOL_LIST

# Skip this entire test module if the API key is not available
pytestmark = pytest.mark.skipif(
    not os.getenv("GEMINI_API_KEY"),
    reason="GEMINI_API_KEY environment variable not set"
)

@pytest.fixture
def virtual_plugin_path(tmp_path: Path) -> Path:
    """Creates a complete virtual plugin for a full end-to-end test."""
    profile_dir = tmp_path / "profile"
    profile_dir.mkdir()
    profile_path = profile_dir / "plugin-profile.yaml"
    
    profile_data = {
        "name": "Virtual-Test-Plugin",
        "version": "1.0.0",
        "description": "A virtual plugin for testing.",
        "mcp_profile": [],
        "behavioral_profile": {
            "success_scenarios": [],
            "failure_scenarios": [
                {
                    "description": "This is the bug we want the agent to fix.",
                    "tool_call": "run_bug_scenario",
                    "inputs": {},
                    "expected_log": "ERROR: Bug triggered"
                }
            ]
        }
    }
    with open(profile_path, 'w') as f:
        yaml.dump(profile_data, f)

    template_dir = Path(__file__).parent.parent / "templates"
    factory = PluginFactory(template_dir=template_dir)
    
    output_dir = tmp_path / "plugins"
    return factory.create(profile_path, output_dir)

def test_fix_bug_playbook_on_virtual_plugin(virtual_plugin_path: Path):
    """
    Tests the full end-to-end flow of running the fix_bug playbook
    on a generated virtual plugin.
    """
    # 1. Setup all components
    api_key = os.getenv("GEMINI_API_KEY")
    
    # Wrap the real tools for observability
    wrapped_tools = [wrap_tool(tool) for tool in TOOL_LIST]
    
    agent = GeminiAgent(
        api_key=api_key,
        working_directory=str(virtual_plugin_path),
        tools=wrapped_tools
    )
    
    orchestrator = Orchestrator(
        agent=agent,
        profile_loader=ProfileLoader(),
        playbook_loader=PlaybookLoader(),
        prompt_constructor=PromptConstructor()
    )
    
    harness = EvaluationHarness(orchestrator)

    # 2. Execute the playbook
    playbook_path = Path(__file__).parent.parent / "playbooks" / "playbook_fix_bug.md"
    
    events = harness.run_and_capture(
        playbook_path=playbook_path,
        plugin_path=virtual_plugin_path,
        env="virtual",
        bug_description="The test for the bug scenario is failing. Please fix it."
    )

    # Print the captured events for debugging
    print("\n--- Captured Events ---")
    import json
    print(json.dumps(events, indent=2))
    print("-----------------------\n")

    # 3. Assert against the captured events
    # This is a high-level assertion to prove the concept. More detailed assertions
    # can be added to verify each step of the playbook.
    
    # Check that the agent tried to edit the profile
    edit_profile_events = [
        e for e in events 
        if e.get("name") == "edit_file" and "plugin-profile.yaml" in e.get("args", {}).get("file_path", "")
    ]
    assert len(edit_profile_events) > 0, "Agent should have attempted to edit the plugin profile"

    # Check that the agent tried to edit the changelog
    edit_changelog_events = [
        e for e in events 
        if e.get("name") == "edit_file" and "CHANGE_LOG.md" in e.get("args", {}).get("file_path", "")
    ]
    assert len(edit_changelog_events) > 0, "Agent should have attempted to edit the CHANGE_LOG.md"

    # Check that the agent ran the tests
    run_test_events = [
        e for e in events 
        if e.get("name") == "execute_shell_command" and "pytest" in e.get("args", {}).get("command", "")
    ]
    assert len(run_test_events) > 0, "Agent should have run pytest"