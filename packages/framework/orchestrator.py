# packages/framework/orchestrator.py

from pathlib import Path
from .loaders import ProfileLoader, PlaybookLoader
from .prompt_constructor import PromptConstructor
from packages.plugin_manager_agent import GeminiAgent

class Orchestrator:
    """
    The core engine that manages and executes a playbook by orchestrating
    the interaction between an agent and a set of tools.
    """

    def __init__(
        self,
        agent: GeminiAgent,
        profile_loader: ProfileLoader,
        playbook_loader: PlaybookLoader,
        prompt_constructor: PromptConstructor,
    ):
        self.agent = agent
        self.profile_loader = profile_loader
        self.playbook_loader = playbook_loader
        self.prompt_constructor = prompt_constructor

    def run(
        self,
        playbook_path: Path,
        plugin_path: Path,
        env: str,
        bug_description: str = ""
    ) -> str:
        """
        The main execution method to run a playbook on a plugin.

        Args:
            playbook_path: The path to the playbook markdown file.
            plugin_path: The root directory of the plugin to operate on.
            env: The execution environment ('virtual' or 'real').
            bug_description: The description of the bug for the fix_bug playbook.

        Returns:
            The final text summary from the agent.
        """
        # 1. Load profile and playbook
        profile = self.profile_loader.load(plugin_path)
        playbook = self.playbook_loader.load(playbook_path)

        # 2. Construct the initial prompt
        prompt = self.prompt_constructor.construct(
            playbook=playbook,
            profile=profile,
            env=env,
            bug_description=bug_description
        )

        # 3. Run the agent's execution generator
        # The agent's tools are expected to be pre-wrapped for observability.
        execution_generator = self.agent.execute(prompt)
        
        final_response = None
        while True:
            try:
                # Drive the generator forward
                next(execution_generator)
            except StopIteration as e:
                # The generator is exhausted, its return value is in the exception
                final_response = e.value
                break
        
        return final_response
