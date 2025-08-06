# Plugin Manager: AI-Driven Plugin Orchestration

### The Challenge: Automating Maintenance with Confidence

Let's say you maintain a large library of similar components—plugins, microservices, or internal tools. The overhead of keeping them all consistent is immense. Tasks like updating dependencies, enforcing coding patterns, or applying a simple security patch across every repository create a significant maintenance burden.

AI agents should be able to help with these common problems:

*   **Repetitive Toil**: Automating simple but time-consuming updates across many repositories.
*   **Cognitive Overload**: Freeing developers from the high mental load of context-switching between numerous components just to track, fix, and deploy simple changes.
*   **Slow Deployments**: Speeding up the lifecycle of simple fixes and updates.

The idea of unleashing an AI agent to handle these tasks is compelling, but we've all seen them fail unpredictably. Even for well-defined, repetitive tasks, a critical question remains: how do you validate that the agent will actually accomplish the task correctly?

Standard unit testing falls short. It can test a specific, deterministic function, but it can't validate the complex, multi-step reasoning of an AI agent. This leads to the central problem:

How do you guarantee a high-quality result from an agent when you can't reliably test its problem-solving process?

### The Solution: A "Wind Tunnel" for AI Agents

This project explores a methodology for building and testing AI agents in a safe, controlled environment. Instead of aiming them at live code, we test them in a simulation first.

To make this tangible, we use a "wind tunnel" analogy. A successful test requires three things: the object being tested, a set of instructions, and the testing environment itself.

1.  **The Virtual Plugin (The Model)**: This is the object we place *inside* the wind tunnel. It is a **behavioral model** that simulates a real piece of code—a "process mock." It is not the code itself, but a simplified, predictable representation for the agent to modify. In our analogy, this is the scale model of an airplane wing.

2.  **The Playbook (The Instructions)**: These are the agent's **execution instructions**. A playbook is a structured, version-controlled prompt that guides the agent through a complex workflow. It often serves as a template, combining reusable best practices with specific variables for the task (e.g., the details of a bug report). The Virtual Plugin is used to verify that these instructions are robust; the playbook is tuned and refined until an agent can follow it reliably, first in the simulation and eventually on real code.

3.  **The Orchestrator (The Wind Tunnel)**: This is the framework that runs the entire simulation. It provides the agent with a sandboxed set of tools, executes the instructions from the Playbook, and records every action the agent takes. It's the controlled environment that ensures tests are safe and results are measurable.

The workflow is simple: the **Orchestrator** uses a **Playbook** to guide an **AI Agent** in modifying a **Virtual Plugin**.

By having the agent operate on the virtual model first, we can validate its ability to follow instructions and solve problems correctly. It's a way to test and refine the agent's reasoning in a safe, repeatable environment.

> Think of this as a simulation framework where virtual plugins serve as the "wind tunnel" for testing AI orchestration systems before they encounter real-world complexity.

This approach builds confidence. When we finally deploy the agent to operate on a real plugin, we have already validated that it can follow the playbook and achieve the desired outcome.

### How It Works: From Model to Automated Workflow

The core idea of this project is to use a simplified *model* as a proxy for a real-world system, allowing us to safely test and develop our automation.

#### Why Use a Model? The Power of a Proxy

In machine learning, a model is a simplified representation of a complex system. It's not the system itself, but it behaves similarly enough to be a useful proxy for thought experiments and simulations.

Think of it this way: you could create a mental "model" of a close friend. You could ask that model, "Would my friend enjoy a surprise party?" Based on your knowledge, the model would give you a probable answer. It allows you to run an experiment and anticipate the real-world response without the risk of actually ruining a surprise.

Our **Virtual Plugin** is just such a model, but for a piece of software. It's a safe, predictable proxy that we can run experiments against. By instructing an agent to modify this model, we can validate whether our instructions (the Playbook) are clear and effective enough to achieve the desired result.

#### A Practical Example: From Production Error to Pull Request

With this model-based approach, we can orchestrate complex, real-world maintenance tasks. Imagine a new bug is reported by an error-tracking service like DataDog. We could deploy an agent to perform the following workflow:

1.  **Ingest the Error**: The agent is triggered by the new error. It uses a tool to pull the relevant details: the stack trace, error message, and the exact version of the code where the error occurred.

2.  **Create a Test Environment**: The agent checks out the specific Git commit from the production error and creates a new branch named after the issue (e.g., `fix/TICKET-123`).

3.  **Reproduce the Bug**: Using a "Test-Driven Development" Playbook, the agent first writes a new unit test that fails, successfully reproducing the reported bug in the local environment.

4.  **Research and Fix**: The agent uses its reasoning capabilities and available tools to analyze the source of the error. It then modifies the code to implement a fix.

5.  **Validate the Fix**: The agent runs the entire test suite, confirming that its new test now passes and that no existing tests have been broken (i.e., no regressions).

6.  **Submit for Review**: Finally, the agent commits the code, pushes the branch, and opens a Pull Request, summarizing the error and its fix in the description for a human engineer to review and merge.

This entire process is first perfected against a **Virtual Plugin**. We create a virtual model where the "bug" is a predictable, simulated failure. We tune the Playbook until the agent can successfully execute this workflow in the simulation. Only then do we have the confidence to deploy it against our real codebase.

## 🏗️ System Architecture

### Core Components

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Playbooks     │    │   Orchestrator  │    │   AI Agent      │
│                 │    │                 │    │                 │
│ • TDD Workflow  │───▶│ • Event System  │───▶│ • Gemini Agent  │
│ • Bug Fixing    │    │ • Tool Wrappers │    │ • Function Call  │
│ • Version Bump  │    │ • Process Coord │    │ • Reasoning     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Virtual Plugins │    │   Tools         │    │ Real Plugins    │
│                 │    │                 │    │                 │
│ • Behavioral    │    │ • read_file    │    │ • Production    │
│   Profiles      │    │ • write_file   │    │   Implementations │
│ • Process Mocks │    │ • list_files   │    │ • Real Code     │
│ • Test Harness  │    │ • shell_cmd    │    │ • CHANGE_LOG.md │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Key Innovation: Execution Traces

How do we validate that agents follow playbooks correctly? We use **Execution Traces** - structured logs that capture:

- `command_run`: Commands executed with exit codes and output
- `file_write`: Files modified during execution
- `version_change`: Version increments and changelog updates
- `tool_calls`: Agent tool usage and parameters

This creates a deterministic way to validate agent behavior, providing confidence in the testing framework and enabling reliable comparisons between virtual and real plugin scenarios.

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Gemini API key (via environment variable, .env file, or command line)
- Virtual environment setup

### Installation
```bash
make install-deps
```

### Configuration

The system supports multiple API key sources (in order of priority):

1. **Command Line**: `--api-key YOUR_KEY`
2. **Project .env**: Add `GEMINI_API_KEY=your_key` to `.env`
3. **Environment Variable**: `export GEMINI_API_KEY=your_key`
4. **Home .env**: Add `GEMINI_API_KEY=your_key` to `~/.env`

### Running Tests

#### Deterministic Tests (Fast, Reliable)
```bash
# All deterministic tests
pytest evaluations/deterministic/ -v

# Specific tool tests
pytest evaluations/deterministic/test_read_file.py -v
```

#### Agent/Playbook Tests (Slower, Require API Key)
```bash
# All agent tests (requires GEMINI_API_KEY)
pytest evaluations/agent/ -v

# Specific playbook tests
pytest evaluations/agent/test_playbook_copy_file.py -v
```

### Running Playbooks

Execute playbooks on real plugins:

```bash
# Basic usage
python -m packages.framework my-first-plugin playbook_list_files

# With bug description
python -m packages.framework my-first-plugin playbook_fix_bug --bug "Fix whitespace issue"

# With custom API key
python -m packages.framework my-first-plugin playbook_fix_bug --api-key YOUR_KEY

# Enable Human-in-the-Loop
python -m packages.framework my-first-plugin playbook_fix_bug --hitl
```

## 📁 Project Structure

```
poc-plugin-manager/
├── packages/                    # Core framework
│   ├── framework/              # Orchestrator and core components
│   │   ├── __main__.py         # CLI entrypoint
│   │   ├── orchestrator.py     # Main execution engine
│   │   ├── tool_wrapper.py     # Tool event wrapping
│   │   └── utils/              # Utilities (API key management)
│   └── plugin_manager_agent/   # Agent implementation
│       ├── gemini_agent.py     # Gemini AI integration
│       └── tools/              # Available tools
├── playbooks/                  # Standardized instruction sets
│   ├── playbook_copy_file.md   # File copying workflow
│   ├── playbook_fix_bug.md     # Bug fixing workflow
│   └── playbook_update_description.md  # Profile modification
├── templates/                  # Virtual plugin templates
├── evaluations/                # Test suites
│   ├── deterministic/          # Unit/integration tests
│   └── agent/                  # End-to-end agent tests
├── plugins_real/               # Real production plugins
└── .env                        # Configuration (contains API key)
```

## 🧪 Available Playbooks

### Tool Combination Workflows
- **`playbook_copy_file.md`**: Copy file content using `read_file` + `write_file`
- **`playbook_read_specific_file.md`**: Find and read specific files using `list_files` + `read_file`
- **`playbook_command_and_capture.md`**: Execute commands and capture output

### Reasoning Workflows
- **`playbook_update_description.md`**: Modify plugin profiles based on context
- **`playbook_fix_bug.md`**: Complex bug fixing with multiple reasoning steps

### Simple Operations
- **`playbook_list_files.md`**: Basic directory listing

## 🔧 Development Workflow

1. **Tool Validation**: Test individual tools in isolation
2. **Combination Testing**: Validate simple tool combinations
3. **Reasoning Development**: Build context-based operations
4. **Complex Integration**: Progress to multi-step workflows

### Quality Assurance

- **Deterministic Tests**: 100% passing, fast execution
- **Agent Tests**: Validate reasoning capabilities (require API key)
- **Execution Traces**: Verify agent behavior correctness
- **Documentation**: Comprehensive inline documentation

## 📚 Documentation

- [Project Plan](docs/project-plan/00_master_plan.md) - High-level architecture
- [Next Steps](NEXT_STEPS.md) - Current development focus
- [Tasks](TASKS.md) - Detailed implementation tasks
- [Evaluations Guide](evaluations/README.md) - Testing strategy

### Key Benefits

### For AI Tool Development
+- **Safe Testing**: Experiment with agent capabilities without risking production systems
+- **Rapid Development**: Quick iteration cycles for playbook and agent refinement
+- **Reproducible Scenarios**: Consistent conditions for debugging and validation

### For Testing Frameworks
+- **Behavioral Testing**: Validate how agents follow processes rather than just checking outputs
+- **Deterministic Validation**: Execution traces provide reliable test results
+- **Cross-Environment Testing**: Ensure consistent behavior across virtual and real systems

### For Quality Assurance
+- **Comprehensive Testing**: Covers tool functionality, agent reasoning, and process execution
+- **Fast Feedback**: Deterministic tests provide quick insights and validation
+- **Risk Reduction**: Catch and resolve issues in virtual environments before real deployment

This project explores a testing approach for AI orchestration systems: using Virtual Plugins as behavioral models, validated through execution traces, enabling safe and reproducible AI agent development.