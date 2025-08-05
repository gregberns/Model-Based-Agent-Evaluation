# evaluations/agent/test_playbook_update_description.py

import pytest
import tempfile
import os
import yaml
import logging
from pathlib import Path

from .harness import EvaluationHarness
from packages.framework.factory import PluginFactory
from packages.framework.orchestrator import Orchestrator
from packages.framework.loaders import ProfileLoader, PlaybookLoader
from packages.framework.prompt_constructor import PromptConstructor
from packages.framework.tool_wrapper import tool_wrapper_factory
from packages.plugin_manager_agent import GeminiAgent
from packages.plugin_manager_agent.tools import TOOL_LIST

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Skip this entire test module if the API key is not available
pytestmark = pytest.mark.skipif(
    not os.getenv("GEMINI_API_KEY"),
    reason="GEMINI_API_KEY environment variable not set"
)

ORIGINAL_DESCRIPTION = "A test plugin for demonstration purposes."
UPDATED_DESCRIPTION = "A comprehensive test plugin that demonstrates the plugin manager's capabilities for file operations, command execution, and profile management. This plugin serves as a reference implementation for testing and validation purposes, showcasing advanced reasoning capabilities and context-based modifications."

@pytest.fixture
def virtual_plugin_path_with_profile(tmp_path: Path) -> Path:
    """Creates a virtual plugin with a profile that needs description updating."""
    profile_dir = tmp_path / "profile"
    profile_dir.mkdir()
    profile_path = profile_dir / "plugin-profile.yaml"

    profile_data = {
        "name": "Description-Test-Plugin",
        "version": "1.0.0",
        "description": ORIGINAL_DESCRIPTION,
        "mcp_profile": []
    }
    with open(profile_path, 'w') as f:
        yaml.dump(profile_data, f)

    template_dir = Path(__file__).parent.parent.parent / "templates"
    factory = PluginFactory(template_dir=template_dir)

    output_dir = tmp_path / "plugins"
    plugin_path = factory.create(profile_path, output_dir)

    return plugin_path

@pytest.mark.timeout(120)
def test_update_description_playbook_and_validate_output(virtual_plugin_path_with_profile: Path):
    """
    Tests that the agent can read a plugin profile and update its description.
    """
    # 1. Setup
    api_key = os.getenv("GEMINI_API_KEY")
    orchestrator = Orchestrator(
        profile_loader=ProfileLoader(),
        playbook_loader=PlaybookLoader(),
        prompt_constructor=PromptConstructor(),
        hitl=False
    )
    harness = EvaluationHarness(orchestrator)

    # 2. Execute
    playbook_path = Path(__file__).parent.parent.parent / "playbooks" / "playbook_update_description.md"

    final_response = harness.run_and_capture(
        playbook_path=playbook_path,
        plugin_path=virtual_plugin_path_with_profile,
        env="virtual",
        api_key=api_key
    )

    # 3. Assert
    # Read the updated profile file
    profile_path = virtual_plugin_path_with_profile / "plugin-profile.yaml"
    assert profile_path.exists(), "Profile file should still exist"

    with open(profile_path, 'r') as f:
        profile_data = yaml.safe_load(f)

    # Check that the description was updated
    assert "description" in profile_data, "Profile should have a description field"
    updated_description = profile_data["description"]

    # The description should be different from the original
    assert updated_description != ORIGINAL_DESCRIPTION, \
        f"Description should have been updated. Original: '{ORIGINAL_DESCRIPTION}', Updated: '{updated_description}'"

    # The description should be more detailed/informative
    assert len(updated_description) > len(ORIGINAL_DESCRIPTION), \
        "Updated description should be longer/more detailed than the original"

    # Check that other fields were preserved
    assert profile_data["name"] == "Description-Test-Plugin", "Plugin name should be preserved"
    assert profile_data["version"] == "1.0.0", "Plugin version should be preserved"
    assert profile_data["mcp_profile"] == [], "MCP profile should be preserved"

    # Check that the agent's final response indicates success
    assert "description" in final_response.lower(), "Agent should mention description update"
    assert "update" in final_response.lower() or "success" in final_response.lower(), \
        f"Agent's final response should indicate successful update. Got: '{final_response}'"

    # Check that the agent mentions both old and new descriptions
    assert ORIGINAL_DESCRIPTION in final_response, \
        f"Agent should mention the original description. Got: '{final_response}'"
    assert updated_description in final_response, \
        f"Agent should mention the updated description. Got: '{final_response}'"

@pytest.mark.timeout(120)
def test_update_description_with_edge_case(virtual_plugin_path_with_profile: Path):
    """
    Tests that the agent handles edge cases in description updating gracefully.
    """
    # Create a profile with an empty description to test edge case handling
    profile_path = virtual_plugin_path_with_profile / "plugin-profile.yaml"

    with open(profile_path, 'w') as f:
        yaml.dump({
            "name": "Edge-Case-Plugin",
            "version": "1.0.0",
            "description": "",  # Empty description
            "mcp_profile": []
        }, f)

    # 1. Setup
    api_key = os.getenv("GEMINI_API_KEY")
    orchestrator = Orchestrator(
        profile_loader=ProfileLoader(),
        playbook_loader=PlaybookLoader(),
        prompt_constructor=PromptConstructor(),
        hitl=False
    )
    harness = EvaluationHarness(orchestrator)

    # 2. Execute
    playbook_path = Path(__file__).parent.parent.parent / "playbooks" / "playbook_update_description.md"

    final_response = harness.run_and_capture(
        playbook_path=playbook_path,
        plugin_path=virtual_plugin_path_with_profile,
        env="virtual",
        api_key=api_key
    )

    # 3. Assert
    # Read the updated profile file
    with open(profile_path, 'r') as f:
        profile_data = yaml.safe_load(f)

    # Check that the description was updated from empty
    assert "description" in profile_data, "Profile should have a description field"
    updated_description = profile_data["description"]

    # The description should no longer be empty
    assert updated_description != "", "Description should not be empty after update"
    assert len(updated_description) > 0, "Description should have content"

    # Check that the agent handled the empty description case
    assert "empty" in final_response.lower() or "blank" in final_response.lower() or "original" in final_response.lower(), \
        f"Agent should acknowledge the empty original description. Got: '{final_response}'"
