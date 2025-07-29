# packages/framework/tests/test_prompt_constructor.py

import pytest
from packages.framework.loaders import Playbook
from packages.framework.schema import PluginProfile
from packages.framework.prompt_constructor import PromptConstructor

@pytest.fixture
def sample_playbook() -> Playbook:
    """Provides a sample Playbook object for testing."""
    return Playbook(
        objective="Test objective",
        prompt_template="""
Env: {environment}
Dir: {working_directory}
Bug: {bug_description}
Instructions: {environment_specific_instructions}
"""
    )

@pytest.fixture
def sample_profile() -> PluginProfile:
    """Provides a sample PluginProfile object for testing."""
    return PluginProfile(
        name="Test-Plugin",
        version="1.0.0",
        description="A test plugin.",
        mcp_profile=[]
    )

def test_prompt_constructor_virtual_env(sample_playbook, sample_profile):
    """Tests that the prompt is correctly constructed for the virtual environment."""
    constructor = PromptConstructor()
    prompt = constructor.construct(
        playbook=sample_playbook,
        profile=sample_profile,
        env="virtual",
        bug_description="A test bug"
    )

    assert "Env: Virtual" in prompt
    assert "Dir: ./" in prompt
    assert "Bug: A test bug" in prompt
    assert "edit the `plugin-profile.yaml` file" in prompt

def test_prompt_constructor_real_env(sample_playbook, sample_profile):
    """Tests that the prompt is correctly constructed for the real environment."""
    constructor = PromptConstructor()
    prompt = constructor.construct(
        playbook=sample_playbook,
        profile=sample_profile,
        env="real",
        bug_description="Another bug"
    )

    assert "Env: Real" in prompt
    assert "Dir: ./" in prompt
    assert "Bug: Another bug" in prompt
    assert "modify the source code in the `src/` directory" in prompt

def test_prompt_constructor_invalid_env_raises_error(sample_playbook, sample_profile):
    """Tests that an invalid environment raises a ValueError."""
    constructor = PromptConstructor()
    with pytest.raises(ValueError):
        constructor.construct(
            playbook=sample_playbook,
            profile=sample_profile,
            env="invalid_env"
        )
