# evaluations/test_playbook_copy_file.py

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

SOURCE_FILE_NAME = "source_file.txt"
DESTINATION_FILE_NAME = "destination_file.txt"
SOURCE_CONTENT = """This is the source file content.
Line 2 of the source file.
Line 3 with some special characters: áéíóú 🚀
Final line of source."""

@pytest.fixture
def virtual_plugin_path_with_files(tmp_path: Path) -> Path:
    """Creates a virtual plugin with source and destination files."""
    profile_dir = tmp_path / "profile"
    profile_dir.mkdir()
    profile_path = profile_dir / "plugin-profile.yaml"

    profile_data = {"name": "Copy-Test-Plugin", "version": "1.0.0", "description": "A test plugin for file copying.", "mcp_profile": []}
    with open(profile_path, 'w') as f:
        yaml.dump(profile_data, f)

    template_dir = Path(__file__).parent.parent / "templates"
    factory = PluginFactory(template_dir=template_dir)

    output_dir = tmp_path / "plugins"
    plugin_path = factory.create(profile_path, output_dir)

    # Create source file with test content
    source_file = plugin_path / SOURCE_FILE_NAME
    source_file.write_text(SOURCE_CONTENT)

    # Create empty destination file
    destination_file = plugin_path / DESTINATION_FILE_NAME
    destination_file.write_text("")

    return plugin_path

@pytest.mark.timeout(120)
def test_copy_file_playbook_and_validate_output(virtual_plugin_path_with_files: Path):
    """
    Tests that the agent can copy file content from source to destination.
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
    playbook_path = Path(__file__).parent.parent / "playbooks" / "playbook_copy_file.md"

    final_response = harness.run_and_capture(
        playbook_path=playbook_path,
        plugin_path=virtual_plugin_path_with_files,
        env="virtual",
        api_key=api_key
    )

    # 3. Assert
    # Check that the destination file now contains the source content
    destination_file = virtual_plugin_path_with_files / DESTINATION_FILE_NAME
    assert destination_file.exists(), "Destination file should exist"

    with open(destination_file, 'r') as f:
        copied_content = f.read()

    assert copied_content == SOURCE_CONTENT, f"Copied content doesn't match source. Got: '{copied_content}'"

    # Check that the source file is unchanged
    source_file = virtual_plugin_path_with_files / SOURCE_FILE_NAME
    with open(source_file, 'r') as f:
        original_content = f.read()

    assert original_content == SOURCE_CONTENT, "Source file should be unchanged"

    # Check that the agent's final response confirms success
    assert "copy" in final_response.lower() or "success" in final_response.lower(), \
        f"Agent's final response should indicate success. Got: '{final_response}'"
