# The Virtual Plugin: A Blueprint for Agent-Driven Development (v6)

This document provides the definitive technical architecture for the Orchestrator and Agent interaction. It resolves the critical challenge of observability by adopting an industry-standard "Observability Wrapper" pattern, which avoids re-implementing agent tools while providing a fully verifiable action trace.

## 1. The Core Architecture: The "Observability Wrapper" Pattern

We will not run a black-box CLI command. Instead, the **Orchestrator** (our Python framework) will programmatically control the **Agent** (the Gemini LLM) via its official Python SDK. The agent's ability to interact with the environment is provided by the Orchestrator through a mechanism known as **function calling**.

This solves the core problem: the Orchestrator doesn't need to guess what the agent did; it knows, because it is the one that executed the action on the agent's behalf.

### How It Works: A Detailed Flow

1.  **The Orchestrator Defines Tools:** We create a set of Python functions (`packages/framework/tools.py`) that will be exposed to the agent. These functions are thin wrappers around standard, robust Python libraries (`pathlib`, `subprocess`). Their only special capability is that they log their own execution to our `execution_trace.jsonl`.

    **Example: `packages/framework/tools.py`**
    ```python
    import subprocess
    from pathlib import Path
    from . import logger # Our event logger for the execution trace

    def write_file(path: str, content: str) -> str:
        """Writes content to a specified file."""
        logger.log_event("tool_requested", {"name": "write_file", "path": path})
        try:
            Path(path).write_text(content)
            result = f"Successfully wrote {len(content)} bytes to {path}"
            logger.log_event("tool_completed", {"name": "write_file", "result": result})
            return result
        except Exception as e:
            logger.log_event("tool_failed", {"name": "write_file", "error": str(e)})
            return f"Error writing to file: {e}"

    def run_shell_command(command: str) -> str:
        """Executes a shell command with a timeout."""
        logger.log_event("tool_requested", {"name": "run_shell_command", "command": command})
        try:
            process = subprocess.run(
                command, shell=True, capture_output=True, text=True, timeout=300
            )
            result = {"stdout": process.stdout, "stderr": process.stderr, "exit_code": process.returncode}
            logger.log_event("tool_completed", {"name": "run_shell_command", "result": result})
            return f"Command completed with exit code {process.returncode}.\nSTDOUT:\n{process.stdout}\nSTDERR:\n{process.stderr}"
        except Exception as e:
            logger.log_event("tool_failed", {"name": "run_shell_command", "error": str(e)})
            return f"Error running command: {e}"
    ```

2.  **The Orchestrator Manages the Agent Session:** The Orchestrator uses the Gemini Python SDK to control the agent in a "headless" mode. It explicitly tells the agent which tools it is allowed to request.

    **Conceptual Code in `packages/framework/orchestrator.py`**
    ```python
    import google.generativeai as genai
    from . import tools

    # Configure the SDK and create a model instance with our tools
    genai.configure(api_key="...")
    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro-latest",
        tools=[tools.write_file, tools.run_shell_command] # Pass our functions
    )
    chat = model.start_chat(enable_automatic_function_calling=False) # We want manual control

    def run_playbook(playbook_goal: str, context_prompt: str):
        # Start the conversation
        prompt = f"{playbook_goal}\n\n{context_prompt}"
        response = chat.send_message(prompt)

        # The main execution loop
        while response.candidates[0].content.parts[0].function_call:
            function_call = response.candidates[0].content.parts[0].function_call
            
            # The agent requested a tool. Find our corresponding Python function.
            tool_name = function_call.name
            tool_function = getattr(tools, tool_name)
            
            # Execute our wrapper function, which handles the action AND the logging.
            tool_result = tool_function(**function_call.args)

            # Send the result of the action back to the agent so it can decide the next step.
            response = chat.send_message(
                genai.types.Content(
                    parts=[genai.types.Part(
                        function_response=genai.types.FunctionResponse(
                            name=tool_name,
                            response={"result": tool_result}
                        )
                    )]
                )
            )
        
        # The loop exits when the agent responds with plain text, not a tool call.
        final_summary = response.text
        print(f"Agent finished with summary: {final_summary}")
    ```

### Summary of Benefits

This architecture is the industry-standard approach for building reliable agentic systems and it resolves all the issues we've identified:

*   **No Fragile Tool Re-implementation:** We use Python's robust, standard libraries for all environment interactions.
*   **Full, Reliable Observability:** The Orchestrator logs every action because it is the one executing it. The `execution_trace.jsonl` will be a perfect record of the agent's behavior.
*   **True Headless Operation:** This is the correct way to run an LLM in an automated, non-interactive fashion.
*   **Robust Process Control:** The Orchestrator is a normal Python program. It can implement timeouts for shell commands and network requests, preventing the system from hanging.

We now have a complete, technically sound, and feasible plan for the entire framework.
