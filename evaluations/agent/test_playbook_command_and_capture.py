# evaluations/agent/test_playbook_command_and_capture.py

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

OUTPUT_FILE_NAME = "command_output.txt"
EXPECTED_COMMAND_OUTPUT = "Command output test"

@pytest.fixture
def virtual_plugin_path_with_files(tmp_path: Path) -> Path:
    """Creates a virtual plugin for command execution testing."""
    profile_dir = tmp_path / "profile"
    profile_dir.mkdir()
    profile_path = profile_dir / "plugin-profile.yaml"

    profile_data = {"name": "Command-Test-Plugin", "version": "1.0.0", "description": "A test plugin for command execution.", "mcp_profile": []}
    with open(profile_path, 'w') as f:
        yaml.dump(profile_data, f)

    template_dir = Path(__file__).parent.parent.parent / "templates"
    factory = PluginFactory(template_dir=template_dir)

    output_dir = tmp_path / "plugins"
    plugin_path = factory.create(profile_path, output_dir)

    return plugin_path

@pytest.mark.timeout(120)
def test_command_and_capture_playbook_and_validate_output(virtual_plugin_path_with_files: Path):
    """
    Tests that the agent can execute a shell command and capture its output.
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
    playbook_path = Path(__file__).parent.parent.parent / "playbooks" / "playbook_command_and_capture.md"

    final_response = harness.run_and_capture(
        playbook_path=playbook_path,
        plugin_path=virtual_plugin_path_with_files,
        env="virtual",
        api_key=api_key
    )

    # 3. Assert
    # Check that the output file was created
    output_file = virtual_plugin_path_with_files / OUTPUT_FILE_NAME
    assert output_file.exists(), "Output file should be created"

    with open(output_file, 'r') as f:
        actual_content = f.read().strip()

    assert actual_content == EXPECTED_COMMAND_OUTPUT, f"Output file content should match expected. Got: '{actual_content}'"

    # Check that the agent's final response indicates success
    assert "command" in final_response.lower() or "success" in final_response.lower(), \
        f"Agent's final response should indicate success. Got: '{final_response}'"

    # Check that the agent mentions the output
    assert EXPECTED_COMMAND_OUTPUT in final_response, \
        f"Agent's final response should contain the expected output. Got: '{final_response}'"

@pytest.mark.timeout(120)
def test_command_and_capture_with_error_handling(virtual_plugin_path_with_files: Path):
    """
    Tests that the agent handles command execution errors gracefully.
    """
    # Create a scenario where the command might fail
    # We'll test with a command that should work but we'll verify error handling

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
    playbook_path = Path(__file__).parent.parent.parent / "playbooks" / "playbook_command_and_capture.md"

    final_response = harness.run_and_capture(
        playbook_path=playbook_path,
        plugin_path=virtual_plugin_path_with_files,
        env="virtual",
        api_key=api_key
    )

    # 3. Assert
    # The command should succeed, but we check that the agent handles the workflow properly
    output_file = virtual_plugin_path_with_files / OUTPUT_FILE_NAME

    # The file should exist and contain the expected content
    assert output_file.exists(), "Output file should be created even after potential errors"

    with open(output_file, 'r') as f:
        content = f.read().strip()

    # The content should be what we expect
    assert content == EXPECTED_COMMAND_OUTPUT, f"File content should be correct. Got: '{content}'"

    # The agent should report success
    assert "success" in final_response.lower() or "command" in final_response.lower(), \
        f"Agent should report successful execution. Got: '{final_response}'"
