# evaluations/agent/test_playbook_read_specific_file.py

import pytest
import tempfile
import os
import yaml
import logging
from pathlib import Path

from ..harness import EvaluationHarness
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

TARGET_FILE_NAME = "target_file.txt"
OTHER_FILE_NAME = "other_file.txt"
TARGET_FILE_CONTENT = """This is the target file content.
Line 2 of the target file.
Line 3 with some special characters: áéíóú 🚀
Final line of target."""

OTHER_FILE_CONTENT = "This is an unrelated file."

@pytest.fixture
def virtual_plugin_path_with_files(tmp_path: Path) -> Path:
    """Creates a virtual plugin with target and other files."""
    profile_dir = tmp_path / "profile"
    profile_dir.mkdir()
    profile_path = profile_dir / "plugin-profile.yaml"

    profile_data = {"name": "Read-Test-Plugin", "version": "1.0.0", "description": "A test plugin for file reading.", "mcp_profile": []}
    with open(profile_path, 'w') as f:
        yaml.dump(profile_data, f)

    template_dir = Path(__file__).parent.parent.parent / "templates"
    factory = PluginFactory(template_dir=template_dir)

    output_dir = tmp_path / "plugins"
    plugin_path = factory.create(profile_path, output_dir)

    # Create target file with test content
    target_file = plugin_path / TARGET_FILE_NAME
    target_file.write_text(TARGET_FILE_CONTENT)

    # Create other file with different content
    other_file = plugin_path / OTHER_FILE_NAME
    other_file.write_text(OTHER_FILE_CONTENT)

    return plugin_path

@pytest.mark.timeout(120)
def test_read_specific_file_playbook_and_validate_output(virtual_plugin_path_with_files: Path):
    """
    Tests that the agent can find and read a specific file from a directory.
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
    playbook_path = Path(__file__).parent.parent.parent / "playbooks" / "playbook_read_specific_file.md"

    final_response = harness.run_and_capture(
        playbook_path=playbook_path,
        plugin_path=virtual_plugin_path_with_files,
        env="virtual",
        api_key=api_key
    )

    # 3. Assert
    # Check that the target file still exists and has the expected content
    target_file = virtual_plugin_path_with_files / TARGET_FILE_NAME
    assert target_file.exists(), "Target file should still exist"

    with open(target_file, 'r') as f:
        actual_content = f.read()

    assert actual_content == TARGET_FILE_CONTENT, "Target file content should be unchanged"

    # Check that the other file still exists and has the expected content
    other_file = virtual_plugin_path_with_files / OTHER_FILE_NAME
    assert other_file.exists(), "Other file should still exist"

    with open(other_file, 'r') as f:
        other_content = f.read()

    assert other_content == OTHER_FILE_CONTENT, "Other file content should be unchanged"

    # Check that the agent's final response indicates success
    assert "target_file.txt" in final_response, "Agent should mention the target file name"
    assert TARGET_FILE_CONTENT.strip() in final_response or "found" in final_response.lower(), \
        f"Agent's final response should indicate the file was found and show its content. Got: '{final_response}'"

@pytest.mark.timeout(120)
def test_read_specific_file_not_found(virtual_plugin_path_with_files: Path):
    """
    Tests that the agent properly handles when the target file is not found.
    """
    # Remove the target file to simulate it not existing
    target_file = virtual_plugin_path_with_files / TARGET_FILE_NAME
    target_file.unlink()

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
    playbook_path = Path(__file__).parent.parent.parent / "playbooks" / "playbook_read_specific_file.md"

    final_response = harness.run_and_capture(
        playbook_path=playbook_path,
        plugin_path=virtual_plugin_path_with_files,
        env="virtual",
        api_key=api_key
    )

    # 3. Assert
    # Check that the agent's final response indicates the file was not found
    assert "not found" in final_response.lower() or "does not exist" in final_response.lower(), \
        f"Agent's final response should indicate the file was not found. Got: '{final_response}'"

    # Check that the agent mentions the file name they were looking for
    assert "target_file.txt" in final_response, "Agent should mention the target file name they were looking for"

    # Check that the other file still exists (should be unaffected)
    other_file = virtual_plugin_path_with_files / OTHER_FILE_NAME
    assert other_file.exists(), "Other file should still exist"
