# packages/framework/tests/test_orchestrator.py

import pytest
from unittest.mock import MagicMock, patch
from pathlib import Path
from packages.framework.orchestrator import Orchestrator
from packages.framework.loaders import ProfileLoader, PlaybookLoader, Playbook
from packages.framework.prompt_constructor import PromptConstructor
from packages.framework.schema import PluginProfile

# Mock the agent class since it's now instantiated inside the orchestrator
@pytest.fixture(autouse=True)
def mock_gemini_agent():
    with patch('packages.framework.orchestrator.GeminiAgent') as mock:
        mock_instance = mock.return_value
        mock_instance.execute.return_value = "Final summary"
        yield mock

@pytest.fixture
def mock_profile_loader():
    """Provides a mock ProfileLoader."""
    loader = MagicMock(spec=ProfileLoader)
    loader.load.return_value = MagicMock(spec=PluginProfile)
    return loader

@pytest.fixture
def mock_playbook_loader():
    """Provides a mock PlaybookLoader."""
    loader = MagicMock(spec=PlaybookLoader)
    loader.load.return_value = MagicMock(spec=Playbook)
    return loader

@pytest.fixture
def mock_prompt_constructor():
    """Provides a mock PromptConstructor."""
    constructor = MagicMock(spec=PromptConstructor)
    constructor.construct.return_value = "This is the constructed prompt."
    return constructor

def test_orchestrator_initializes_correctly(
    mock_profile_loader, mock_playbook_loader, mock_prompt_constructor
):
    """Tests that the Orchestrator initializes with its dependencies."""
    orchestrator = Orchestrator(
        profile_loader=mock_profile_loader,
        playbook_loader=mock_playbook_loader,
        prompt_constructor=mock_prompt_constructor,
    )
    assert orchestrator.profile_loader is mock_profile_loader
    assert orchestrator.playbook_loader is mock_playbook_loader
    assert orchestrator.prompt_constructor is mock_prompt_constructor

def test_orchestrator_run_method_calls_dependencies_in_order(
    mock_gemini_agent, mock_profile_loader, mock_playbook_loader, mock_prompt_constructor
):
    """Tests the sequence of calls in the run method."""
    orchestrator = Orchestrator(
        profile_loader=mock_profile_loader,
        playbook_loader=mock_playbook_loader,
        prompt_constructor=mock_prompt_constructor,
    )

    playbook_path = Path("playbook.md")
    plugin_path = Path("plugin/")
    
    final_summary = orchestrator.run(
        playbook_path=playbook_path,
        plugin_path=plugin_path,
        env="virtual",
        api_key="test_key",
        bug_description="A bug"
    )

    # 1. Verify loaders were called
    mock_profile_loader.load.assert_called_once_with(plugin_path)
    mock_playbook_loader.load.assert_called_once_with(playbook_path)

    # 2. Verify prompt constructor was called
    mock_prompt_constructor.construct.assert_called_once()

    # 3. Verify agent was instantiated and its execute method was called
    mock_gemini_agent.assert_called_once()
    mock_gemini_agent.return_value.execute.assert_called_once_with("This is the constructed prompt.")
    
    # 4. Verify the final summary is returned
    assert final_summary == "Final summary"