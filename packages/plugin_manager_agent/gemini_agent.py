from google.generativeai.client import Client
import google.generativeai as genai
from google.generativeai import protos
from google.generativeai import types

from .tools import TOOL_LIST as DEFAULT_TOOL_LIST

class GeminiAgent:
    def __init__(self, api_key: str, working_directory: str, model_name: str = "gemini-pro", tools: list = None):
        self.working_directory = working_directory
        if not os.path.exists(self.working_directory):
            os.makedirs(self.working_directory)
        os.chdir(self.working_directory)
        
        # Use a client to specify the stable 'v1' API version
        client = Client(
            api_key=api_key,
            http_options=types.HttpOptions(api_version='v1')
        )
        
        if tools is None:
            tools = DEFAULT_TOOL_LIST
        
        self.tool_functions = {func.__name__: func for func in tools}
        self.model = genai.GenerativeModel(
            model_name=model_name,
            tools=tools,
            client=client
        )
        
        self.history = []

    def execute(self, prompt: str):
        """
        Executes a prompt, yielding tool calls and returning the final text response.
        """
        self.history.append(protos.Content(parts=[protos.Part(text=prompt)], role="user"))

        while True:
            response = self.model.generate_content(self.history)
            candidate = response.candidates[0]

            if not candidate.content.parts or not candidate.content.parts[0].function_call:
                if not candidate.content.parts:
                    final_text = ""
                else:
                    final_text = candidate.content.parts[0].text
                
                self.history.append(protos.Content(parts=[protos.Part(text=final_text)], role="model"))
                return final_text

            function_call = candidate.content.parts[0].function_call
            
            self.history.append(protos.Content(parts=[protos.Part(function_call=function_call)], role="model"))

            yield {
                "name": function_call.name,
                "args": dict(function_call.args),
            }

            tool_function = self.tool_functions.get(function_call.name)
            if not tool_function:
                raise ValueError(f"Tool '{function_call.name}' not found.")
            
            tool_response = tool_function(**dict(function_call.args))
            
            self.history.append(
                protos.Content(
                    parts=[
                        protos.Part(
                            function_response=protos.FunctionResponse(
                                name=function_call.name,
                                response={"result": tool_response},
                            )
                        )
                    ],
                    role="user"
                )
            )