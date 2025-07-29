# packages/framework/orchestrator.py

from pathlib import Path
from .loaders import ProfileLoader, PlaybookLoader
from .prompt_constructor import PromptConstructor
from .tool_wrapper import tool_wrapper_factory
from packages.plugin_manager_agent import GeminiAgent
from packages.plugin_manager_agent.tools import TOOL_LIST

class Orchestrator:
    """
    The core engine that manages and executes a playbook.
    """

    def __init__(
        self,
        profile_loader: ProfileLoader,
        playbook_loader: PlaybookLoader,
        prompt_constructor: PromptConstructor,
        hitl: bool = False
    ):
        self.profile_loader = profile_loader
        self.playbook_loader = playbook_loader
        self.prompt_constructor = prompt_constructor
        self.hitl = hitl

    def run(
        self,
        playbook_path: Path,
        plugin_path: Path,
        env: str,
        api_key: str,
        **kwargs
    ) -> str:
        """
        The main execution method to run a playbook on a plugin.
        """
        # 1. Load profile and playbook
        profile = self.profile_loader.load(plugin_path)
        playbook = self.playbook_loader.load(playbook_path)

        # 2. Construct the initial prompt
        prompt = self.prompt_constructor.construct(
            playbook=playbook,
            profile=profile,
            env=env,
            **kwargs
        )

        # 3. Instantiate the agent with HITL-aware tools
        tool_wrapper = tool_wrapper_factory(hitl=self.hitl)
        wrapped_tools = [tool_wrapper(tool) for tool in TOOL_LIST]
        
        agent = GeminiAgent(
            api_key=api_key,
            working_directory=str(plugin_path),
            tools=wrapped_tools
        )

        # 4. Run the agent's execution method
        final_response = agent.execute(prompt)
        
        return final_response