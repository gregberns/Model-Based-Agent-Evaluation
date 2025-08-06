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

This approach builds confidence. When we finally deploy the agent to operate on a real plugin, we have already validated that it can follow the playbook and achieve the desired outcome.

## 🔍 The Virtual Plugin

### What is a Virtual Plugin?

A Virtual Plugin is a **behavioral model** that simulates a real plugin's characteristics:

 - **Defines Expected Behaviors**: Specifies how a plugin should respond to various inputs
 - **Simulates System Behavior**: Mocks tool execution outcomes without real implementation
 - **Provides Safe Testing Environment**: Enables AI agent development without risking real systems

### Why This Approach Matters

Traditional AI tool testing faces challenges because real systems can be risky, complex, or expensive to test against. Virtual Plugins provide an alternative approach:

**Safe Development Environment**
- Test agent behavior without risking production systems
- Enable rapid iteration on agent capabilities
- Provide reproducible scenarios for debugging and validation

**Realistic Testing Framework**
- Agents encounter realistic challenges and constraints
- Test both success and failure scenarios
- Validate process-following rather than just output generation

**Example Workflow: Bug Fixing Validation**
1. **Initial State**: Virtual plugin defines a failure scenario
2. **Agent Task**: "Fix the InvalidFile error for zero-byte files"
3. **Agent Action**: Modifies the behavioral profile (not real code)
4. **Verification**: Test harness confirms the fix works as expected

This validates the agent's **problem-solving process** - the exact capability needed for real maintenance tasks.

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
