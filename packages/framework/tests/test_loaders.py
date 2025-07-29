# packages/framework/tests/test_loaders.py

import pytest
import yaml
from pathlib import Path
from pydantic import ValidationError
from packages.framework.loaders import ProfileLoader, PlaybookLoader

@pytest.fixture
def temp_plugin_dir(tmp_path: Path) -> Path:
    """Creates a temporary plugin directory with a valid profile for testing."""
    profile_data = {
        "name": "Test-Plugin",
        "version": "1.0.0",
        "description": "A test plugin.",
        "mcp_profile": [],
    }
    profile_path = tmp_path / "plugin-profile.yaml"
    with open(profile_path, 'w') as f:
        yaml.dump(profile_data, f)
    return tmp_path

@pytest.fixture
def temp_playbook_file(tmp_path: Path) -> Path:
    """Creates a temporary playbook file for testing."""
    content = """
# Playbook: Test

## Objective
Test objective.

## Contextual Prompt Template
Test template.
"""
    playbook_path = tmp_path / "playbook.md"
    playbook_path.write_text(content)
    return playbook_path

# --- ProfileLoader Tests ---

def test_profile_loader_success(temp_plugin_dir: Path):
    """Tests that the ProfileLoader successfully loads a valid profile."""
    loader = ProfileLoader()
    profile = loader.load(temp_plugin_dir)
    assert profile.name == "Test-Plugin"
    assert profile.version == "1.0.0"

def test_profile_loader_file_not_found():
    """Tests that ProfileLoader raises FileNotFoundError for a missing profile."""
    loader = ProfileLoader()
    with pytest.raises(FileNotFoundError):
        loader.load(Path("/non_existent_dir"))

def test_profile_loader_invalid_yaml(tmp_path: Path):
    """Tests that ProfileLoader raises ValidationError for an invalid profile."""
    (tmp_path / "plugin-profile.yaml").write_text("name: Test\nversion: 1") # Invalid version
    loader = ProfileLoader()
    with pytest.raises(ValidationError):
        loader.load(tmp_path)

# --- PlaybookLoader Tests ---

def test_playbook_loader_success(temp_playbook_file: Path):
    """Tests that the PlaybookLoader successfully loads a valid playbook."""
    loader = PlaybookLoader()
    playbook = loader.load(temp_playbook_file)
    assert playbook.objective == "Test objective."
    assert playbook.prompt_template == "Test template."

def test_playbook_loader_file_not_found():
    """Tests that PlaybookLoader raises FileNotFoundError for a missing playbook."""
    loader = PlaybookLoader()
    with pytest.raises(FileNotFoundError):
        loader.load(Path("/non_existent_playbook.md"))

def test_playbook_loader_malformed_content(tmp_path: Path):
    """Tests that PlaybookLoader raises ValueError for a malformed playbook."""
    (tmp_path / "playbook.md").write_text("# Just a title")
    loader = PlaybookLoader()
    with pytest.raises(ValueError):
        loader.load(tmp_path / "playbook.md")
