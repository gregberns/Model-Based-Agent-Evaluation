# The Wind Tunnel: Model-Based Agent Evaluation

#### **Abstract**

The industry is moving rapidly toward the use of Large Language Model (LLM) based AI agents to automate complex software engineering tasks. However, a fundamental challenge remains: how can we reliably evaluate the behavior of non-deterministic agents before deploying them to production systems? Traditional software testing paradigms are insufficient for assessing the multi-step, emergent reasoning processes of these agents.

This paper introduces **The Wind Tunnel**, a methodology for **model-based agent evaluation**. We propose a system centered on a **"process mock"**—a behavioral model of a target system (which we term a **Virtual Plugin**). By instructing an agent to perform tasks on this simplified, deterministic model, we can rigorously evaluate its ability to follow complex instructions (a **Playbook**) within a controlled environment (the **Orchestrator**).

This repository serves as a reference implementation of this methodology. Using the domain of automated plugin maintenance as a concrete example, we provide the code and workflows to demonstrate how this approach enables reliable, reproducible evaluation of agent-driven automation. The goal is to provide engineers with a practical pattern for developing and assessing their own robust, agent-based systems.

---

### Context

For engineers not steeped in Machine Learning concepts:

A model can be thought of like a mock or stub. It is a simplified representation of a component, system, environment... really anything - a person even.

A model can be placed in an environment/system, and the system can perform actions upon the model as if it were the real thing. This is similar to how an HTTP mock simulates an HTTP request.

The "Virtual Plugins" described below are the Mocks. The "Playbooks" (prompts) are what are being modified. The Agent and Orchestrator are the execution environment. And the objective is to 'test' or evaluate that the Playbooks and Agents reliably execute the desired actions.

---

### The Challenge: Automating Maintenance with Confidence

Maintaining a large library of similar components, plugins, microservices, or internal tools can be a challenge. There's a large overhead to maintaining consistency throughout the system. Tasks like updating dependencies, enforcing coding patterns, or applying a simple security patch across every repository create a significant maintenance burden.

AI agents should be able to help with these common problems:

*   **Repetitive Toil**: Automating simple but time-consuming updates across many repositories.
*   **Cognitive Overload**: Freeing developers from the high mental load of context-switching between numerous components just to track, fix, and deploy simple changes.
*   **Slow Deployments**: Speeding up the lifecycle of simple fixes and updates.

The idea of unleashing an AI agent to handle these tasks is compelling! But the unpredictability, inconsistency, and need for hand-holding of Agents should make every team lead nervous. Especially for well-defined, repetitive tasks, a critical question remains: how do you validate that the agent will actually accomplish the task correctly?

Standard unit testing falls short. It can test a specific, deterministic function, but it can't validate the complex, multi-step reasoning of an AI agent. This leads to the central problem:

How do you guarantee a high-quality result from an agent when you can't reliably test its problem-solving process?

### The Solution: A "Wind Tunnel" for AI Agents

This project explores a methodology for building and testing AI agents in a safe, controlled environment. Instead of aiming them at live code, we test them in a simulation first.

To make this tangible, we use a "wind tunnel" analogy. A successful test requires three things: the object being tested, a set of instructions, and the testing environment itself.

1.  **The Virtual Plugin (The Model)**: This is the object we place *inside* the wind tunnel. It is a **behavioral model** that simulates a real piece of code — a "process mock." It is not the production code itself, but a simplified, predictable representation for the agent to act upon. In our analogy, this is the scale model of an airplane wing.

2.  **The Playbook (The Instructions)**: These are the agent's **execution instructions**. A playbook is a structured, version-controlled prompt that guides the agent through a task - from a simple action to a complex workflow. It often serves as a template, combining reusable best practices with specific variables for the task (e.g., task description, prod errors, logs). The Virtual Plugin is used to verify that these instructions are robust; the playbook is tuned and refined until an agent can follow it reliably, first in the simulation and eventually on real code.

3.  **The Orchestrator (The Wind Tunnel)**: This is the framework that runs the entire simulation. It provides the agent with a sandboxed set of tools, executes the instructions from the Playbook, and records every action the agent takes. It's the controlled environment that ensures tests are safe and results are measurable.

The workflow is simple: the **Orchestrator** uses a **Playbook** to guide an **AI Agent** in modifying a **Virtual Plugin**.

By having the agent operate on the virtual model first, we can validate its ability to follow instructions and solve problems correctly. It's a way to test and refine the agent's reasoning in a safe, repeatable environment.

> Think of this as a simulation framework where prompts (Playbooks) are placed in a "wind tunnel" for testing AI orchestration systems before they encounter real-world complexity.

This approach builds confidence. When we finally deploy the agent to production, we have already validated that it can follow the playbook and achieve the desired outcome.

### How It Works: From Model to Automated Workflow

The following example breaks down a complex bug fix into distinct steps. Each step can be individually tested and validated using a dedicated playbook. Those steps can be composed into a larger automated workflow for an agent to execute. This approach ensures that even a frontier model, which might otherwise deviate from conventions, follows a precise, engineered process.

1.  **Ingest and Prioritize the Error**: A playbook instructs the agent to query a monitoring tool (like DataDog) for active production issues. The agent chooses a high-priority error and gathers the necessary context: the software version, stack trace, and logs.

2.  **Create a Test Environment**: The agent checks out the specific Git commit from the error report and creates a new branch for the fix (e.g., `fix/TICKET-123`).

3.  **Research and Reproduce the Bug**: The agent researches the likely source of the error based on the ingested data. To confirm its understanding, it writes a new unit test that programmatically reproduces the bug and verifies that this new test fails as expected.

4.  **Implement and Validate the Fix**: Following a "Test-Driven Development" playbook, the agent modifies the application code to resolve the issue. It then re-runs the new test to confirm it now passes and executes the full test suite to ensure the change introduced no regressions.

5.  **Submit for Review**: Finally, the agent commits the code, pushes the branch, and opens a Pull Request, summarizing the error and its fix in the description for a human engineer to review and merge.

This entire process is first perfected against a model (Virtual Plugin). We use different models to simulate the specific behaviors the agent needs to handle at each stage. For instance, one Virtual Plugin can simulate the API responses from the monitoring tool, while another models the file system for the agent to check out and modify. We tune the playbook for each step against its corresponding model until the agent can successfully execute each part of the workflow. Only then do we have the confidence to deploy it against our real codebase.

## 🏗️ System Architecture

### Core Components

The system's architecture is designed to be safe and testable by separating the "thinking" from the "doing." This is achieved by having a central **Orchestrator** that mediates every action the **AI Agent** takes.

```
        ┌────────────┐
        │      Playbook      │
        │   (The Mission)    │
        └───────┬────┘
                     │ (1. Provides Goal)
                     ▼
    ┌────────────────────────────────┐
    │         CONTROL PLANE                               │
    │                                                     │
    │   ┌──────────────┐       ┌─────────┐
    │   │ Orchestrator          │ <--->  │ AI Agent     │
    │   │ (The Engine)          │        │ (Reasoning)  │
    │   └──────┬───────┘       └─────────┘
    │          (2. Manages                                │
    │       Task/Result Loop)                             │
    └──────────┼─────────────────────┘
                      │ (3. Executes Tools & Returns Output)
                      ▼
    ┌───────────────────────────────┐
    │        EXECUTION PLANE                            │
    │                                                   │
    │        ┌────────────┐                    │
    │        │   Tools           │                     │
    │        └─────┬──────┘                    │
    │                  │ (4. Acts upon...)              |
    │                  ▼                                │
    │  ┌──────────────────────────┐   │
    │  │    Target Environment                     │   │
    │  │    ┌────────────────┐         │   │
    │  │    │ Virtual Plugin           │          │   │
    │  │    └────────────────┘         │   │
    │  │              OR                           │   │
    │  │    ┌────────────────┐         │   │
    │  │    │  Real Plugin              │         │   │
    │  │    └────────────────┘         │   │
    │  └──────────────────────────┘   │
    └───────────────────────────────┘
```

#### How It Works:

The architecture is composed of two primary layers, with the Orchestrator acting as the bridge between them.

1.  **The Control Plane (The "Brains")**: This is where the strategy and reasoning happen.
    *   A **Playbook** provides the high-level mission or goal to the Orchestrator.
    *   The **Orchestrator** is the central engine that manages the entire workflow. It does not reason on its own.
    *   The **AI Agent** provides the reasoning. The Orchestrator passes the agent the current task and context; the agent decides which tool to use next and passes that request back to the Orchestrator. This tight loop continues until the goal is met.

2.  **The Execution Plane (The "World")**: This is the environment that the Orchestrator can act upon. The agent has **no direct access** to this layer.
    *   **Tools** are the discrete capabilities the Orchestrator can execute, such as `read_file` or `run_shell_command`.
    *   The **Target Environment** is what the tools affect. The Orchestrator can be configured to point to either:
        *   A **Virtual Plugin**: A safe, simulated environment for testing, debugging, and refining playbooks.
        *   A **Real Plugin**: The actual production codebase for executing a validated, trusted workflow.

This model is fundamentally safe because the agent can only *request* actions. The **Orchestrator** is the component that actually *executes* them, providing a single point of control for logging, security, and switching between test and production environments.

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
