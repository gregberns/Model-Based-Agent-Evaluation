import os
import logging
from google import genai
from google.genai import types
from .tools import TOOL_LIST as DEFAULT_TOOL_LIST

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class GeminiAgent:
    def __init__(self, api_key: str, working_directory: str, model_name: str = "gemini-2.5-pro", tools: list = None):
        self.working_directory = working_directory
        if not os.path.exists(self.working_directory):
            os.makedirs(self.working_directory)
        os.chdir(self.working_directory)
        
        self.client = genai.Client(api_key=api_key)
        self.model_name = model_name
        
        if tools is None:
            tools = DEFAULT_TOOL_LIST
        
        self.tools = tools
        self.history = []

    def execute(self, prompt: str) -> str:
        """
        Executes a prompt using the SDK's automatic function calling.
        Tool calls are not yielded but are captured by the event wrappers.
        Returns the final text response from the model.
        """
        logging.info(f"Agent starting execution with prompt: {prompt[:200]}...")
        
        # Add the new user prompt to the history
        self.history.append(types.Content(role='user', parts=[types.Part.from_text(text=prompt)]))
        
        # With AFC enabled, the SDK handles the entire conversation loop.
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=self.history,
            config=types.GenerateContentConfig(tools=self.tools)
        )
        
        # Update the history with the model's response
        self.history.append(response.candidates[0].content)

        final_text = response.text
        logging.info(f"Agent finished with final response: {final_text[:200]}...")
        return final_text
