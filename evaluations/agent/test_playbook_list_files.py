# evaluations/test_playbook_list_files.py

import pytest
import yaml
import os
import logging
from pathlib import Path

from .harness import EvaluationHarness
from packages.framework.factory import PluginFactory
from packages.framework.orchestrator import Orchestrator
from packages.framework.loaders import ProfileLoader, PlaybookLoader
from packages.framework.prompt_constructor import PromptConstructor
from packages.framework.tool_wrapper import wrap_tool
from packages.plugin_manager_agent import GeminiAgent
from packages.plugin_manager_agent.tools import TOOL_LIST

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Skip this entire test module if the API key is not available
pytestmark = pytest.mark.skipif(
    not os.getenv("GEMINI_API_KEY"),
    reason="GEMINI_API_KEY environment variable not set"
)

DUMMY_FILE_NAME = "dummy_file_for_listing_test.txt"

@pytest.fixture
def virtual_plugin_path(tmp_path: Path) -> Path:
    """Creates a simple virtual plugin and adds a dummy file."""
    profile_dir = tmp_path / "profile"
    profile_dir.mkdir()
    profile_path = profile_dir / "plugin-profile.yaml"
    
    profile_data = {"name": "List-Test-Plugin", "version": "1.0.0", "description": "A test plugin.", "mcp_profile": []}
    with open(profile_path, 'w') as f:
        yaml.dump(profile_data, f)

    template_dir = Path(__file__).parent.parent / "templates"
    factory = PluginFactory(template_dir=template_dir)
    
    output_dir = tmp_path / "plugins"
    plugin_path = factory.create(profile_path, output_dir)

    # Create a dummy file to be listed
    (plugin_path / DUMMY_FILE_NAME).write_text("hello")
    
    return plugin_path

@pytest.mark.timeout(120)
def test_list_files_playbook_and_validate_output(virtual_plugin_path: Path):
    """
    Tests that the agent can correctly list files and use the output
    in its final response.
    """
    # 1. Setup
    api_key = os.getenv("GEMINI_API_KEY")
    wrapped_tools = [wrap_tool(tool) for tool in TOOL_LIST]
    agent = GeminiAgent(api_key=api_key, working_directory=str(virtual_plugin_path), tools=wrapped_tools)
    orchestrator = Orchestrator(
        agent=agent,
        profile_loader=ProfileLoader(),
        playbook_loader=PlaybookLoader(),
        prompt_constructor=PromptConstructor()
    )
    harness = EvaluationHarness(orchestrator)

    # 2. Execute
    playbook_path = Path(__file__).parent.parent / "playbooks" / "playbook_list_files.md"
    
    final_response = harness.run_and_capture(
        playbook_path=playbook_path,
        plugin_path=virtual_plugin_path,
        env="virtual"
    )

    # 3. Assert
    assert DUMMY_FILE_NAME in final_response, \
        f"Agent's final response did not contain the dummy file name. Got: '{final_response}'"
