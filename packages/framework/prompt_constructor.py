# packages/framework/prompt_constructor.py

from .loaders import Playbook
from .schema import PluginProfile

class PromptConstructor:
    """Constructs the initial prompt for the agent."""

    def construct(self, playbook: Playbook, profile: PluginProfile, env: str, **kwargs) -> str:
        """
        Constructs the final prompt string by injecting context into the playbook template.

        Args:
            playbook: The loaded playbook object.
            profile: The loaded plugin profile object.
            env: The execution environment ('virtual' or 'real').
            **kwargs: Additional placeholder values (e.g., bug_description).

        Returns:
            The fully rendered prompt string.
        """
        prompt = playbook.prompt_template

        # Basic placeholders
        prompt = prompt.replace("{environment}", env.title())
        # The agent's working directory is the plugin's root, so paths are relative to that.
        prompt = prompt.replace("{working_directory}", f"./")
        
        for key, value in kwargs.items():
            prompt = prompt.replace(f"{{{key}}}", value)

        # Environment-specific instructions
        if env == 'virtual':
            instructions = (
                "To modify the behavior of a Virtual Plugin, you must edit the "
                "`plugin-profile.yaml` file to change the defined success and failure scenarios. "
                "The Python code in `src/` is a generic interpreter and should not be modified."
            )
        elif env == 'real':
            instructions = (
                "To fix this bug, you must modify the source code in the `src/` directory "
                "to correctly handle this edge case."
            )
        else:
            raise ValueError(f"Invalid environment specified: {env}")
        
        prompt = prompt.replace("{environment_specific_instructions}", instructions)

        return prompt
