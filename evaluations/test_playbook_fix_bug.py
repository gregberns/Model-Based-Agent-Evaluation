# evaluations/test_playbook_fix_bug.py

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

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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

@pytest.mark.timeout(180)
def test_fix_bug_playbook_on_virtual_plugin(virtual_plugin_path: Path):
    """
    Tests the full end-to-end flow of running the fix_bug playbook
    on a generated virtual plugin.
    """
    # 1. Setup all components
    api_key = os.getenv("GEMINI_API_KEY")
    
    orchestrator = Orchestrator(
        profile_loader=ProfileLoader(),
        playbook_loader=PlaybookLoader(),
        prompt_constructor=PromptConstructor()
    )
    
    harness = EvaluationHarness(orchestrator)

    # 2. Execute the playbook
    playbook_path = Path(__file__).parent.parent / "playbooks" / "playbook_fix_bug.md"
    
    harness.run_and_capture(
        playbook_path=playbook_path,
        plugin_path=virtual_plugin_path,
        env="virtual",
        api_key=api_key,
        bug_description="The test for the bug scenario is failing. Please fix it."
    )

    # 3. Assert
    events = harness.captured_events
    edit_profile_events = [
        e for e in events 
        if e.get("name") == "edit_file" and "plugin-profile.yaml" in e.get("args", {}).get("path", "")
    ]
    assert len(edit_profile_events) > 0, "Agent should have attempted to edit the plugin profile"
