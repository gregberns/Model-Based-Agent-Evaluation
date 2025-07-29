import os
from dotenv import load_dotenv
from pathlib import Path
from packages.plugin_manager_agent import GeminiAgent
from packages.plugin_manager_agent.tools import TOOL_LIST

def main():
    # Load environment variables from .env file
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "YOUR_API_KEY_HERE":
        raise ValueError("GEMINI_API_KEY not found or not set in .env file. Please create a .env file and add your key.")

    # Define the agent's working directory
    project_root = Path(__file__).parent.parent
    workspace_path = project_root / "packages" / "poc_workspace"
    
    print(f"Agent starting in working directory: {workspace_path}")

    # Instantiate the agent
    agent = GeminiAgent(
        api_key=api_key,
        working_directory=str(workspace_path),
        model_name="gemini-2.5-pro",
        tools=TOOL_LIST,
    )

    # Example of a multi-step task
    prompt = (
        "First, create a new file called 'hello.txt' with the content 'Hello, World!'. "
        "Then, read the file back to me to confirm its content."
    )
    
    print(f"\n--- Executing Prompt ---\n{prompt}\n------------------------\n")
    
    # The `execute` method is now a generator that yields tool calls
    execution_generator = agent.execute(prompt)
    
    final_response = None
    try:
        while True:
            # The generator yields tool calls until the final text response is returned
            tool_call = next(execution_generator)
            print(f"--- Tool Call ---\nName: {tool_call['name']}\nArgs: {tool_call['args']}\n-----------------")
    except StopIteration as e:
        # The final text response is in the return value of the generator
        final_response = e.value

    print(f"\n--- Agent Finished ---\n{final_response}\n----------------------")

if __name__ == "__main__":
    main()
