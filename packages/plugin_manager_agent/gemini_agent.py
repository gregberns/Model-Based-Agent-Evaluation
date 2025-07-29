import os
import google.generativeai as genai
from .tools import TOOL_LIST as DEFAULT_TOOL_LIST
from google.generativeai.types import FunctionCall

class GeminiAgent:
    def __init__(self, api_key: str, working_directory: str, model_name: str = "gemini-pro", tools: list = None):
        self.working_directory = working_directory
        if not os.path.exists(self.working_directory):
            os.makedirs(self.working_directory)
        os.chdir(self.working_directory)
        
        genai.configure(api_key=api_key)
        
        if tools is None:
            tools = DEFAULT_TOOL_LIST
        
        # Create a mapping of tool names to their functions for easy lookup
        self.tool_functions = {func.__name__: func for func in tools}

        self.model = genai.GenerativeModel(
            model_name=model_name,
            tools=tools,
        )
        
        # We now disable automatic function calling to handle it manually
        self.chat = self.model.start_chat()

    def execute(self, prompt: str):
        """
        Executes a prompt, yielding tool calls and returning the final text response.

        This method is a generator that provides insights into the agent's operations.

        Yields:
            dict: A dictionary representing a tool call, with 'name' and 'args'.

        Returns:
            str: The final text response from the model.
        """
        response = self.chat.send_message(prompt)
        
        while response.candidates[0].content.parts[0].function_call:
            function_call = response.candidates[0].content.parts[0].function_call
            
            # Yield the tool call information to the user
            yield {
                "name": function_call.name,
                "args": dict(function_call.args),
            }

            # Execute the tool
            tool_function = self.tool_functions.get(function_call.name)
            if not tool_function:
                raise ValueError(f"Tool '{function_call.name}' not found.")
            
            tool_response = tool_function(**dict(function_call.args))
            
            # Send the tool's response back to the model
            response = self.chat.send_message(
                part=genai.Part(
                    function_response=genai.FunctionResponse(
                        name=function_call.name,
                        response={"result": tool_response},
                    )
                )
            )

        return response.text