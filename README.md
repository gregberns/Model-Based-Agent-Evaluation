# Plugin Manager: AI-Driven Plugin Orchestration


## The Challenge: Automating Maintenance with Confidence

Let's say you maintain a large library of similar components—plugins, microservices, or internal tools. The overhead of keeping them all consistent is immense. Tasks like updating dependencies, enforcing coding patterns, or applying a simple security patch across every repository create a significant maintenance burden.

AI agents should be able to help with these common problems:

*   **Repetitive Toil**: Automating simple but time-consuming updates across many repositories.
*   **Cognitive Overload**: Freeing developers from the high mental load of context-switching between numerous components just to track, fix, and deploy simple changes.
*   **Slow Deployments**: Speeding up the lifecycle of simple fixes and updates.

The idea of unleashing an AI agent to handle these tasks is compelling, but we've all seen them fail unpredictably. Even for well-defined, repetitive tasks, a critical question remains: how do you validate that the agent will actually accomplish the task correctly?

Standard unit testing falls short. It can test a specific, deterministic function, but it can't validate the complex, multi-step reasoning of an AI agent. This leads to the central problem:

How do you guarantee a high-quality result from an agent when you can't reliably test its problem-solving process?




## The Solution: A "Wind Tunnel" for AI Agents

This project explores a methodology for building and testing AI agents in a safe, controlled environment. Instead of aiming them at live code, we test them in a simulation first.

To make this tangible, we use a "wind tunnel" analogy. A successful test requires three things: the object being tested, a set of instructions, and the testing environment itself.

1.  **The Virtual Plugin (The Model)**: This is the object we place *inside* the wind tunnel. It is a **behavioral model** that simulates a real piece of code—a "process mock." It is not the code itself, but a simplified, predictable representation for the agent to modify. In our analogy, this is the scale model of an airplane wing.

2.  **The Playbook (The Instructions)**: This is our test plan. It's a clear, version-controlled **prompt** that gives the agent a high-level goal, like "Fix the bug related to zero-byte files." The playbook tells the wind tunnel what test to run, but it doesn't specify the outcome, allowing us to see how the agent reasons its way to a solution.

3.  **The Orchestrator (The Wind Tunnel)**: This is the framework that runs the entire simulation. It provides the agent with a sandboxed set of tools, executes the instructions from the Playbook, and records every action the agent takes. It's the controlled environment that ensures tests are safe and results are measurable.

## 🎯 The Testing Challenge

How do you validate and debug AI/LLM-based orchestration tools (ie an Agent)? Traditional testing approaches fall short when dealing with intelligent agents because:

- **Black Box Problem**: AI agents make unpredictable decisions, making it hard to validate their behavior
- **Reproducibility Crisis**: When something goes wrong, can you reproduce the exact conditions to debug it?
- **Production Risk**: Testing against real systems can be dangerous, expensive, or impractical
- **Skill Development Gap**: How do you develop expertise in AI agent orchestration without real-world consequences?

This project addresses these challenges by exploring a testing approach using **Virtual Plugins** as controllable test models. We create behavioral models of plugins, then execute AI agents against them as if they were real systems. This exercises the execution framework, agent reasoning, and playbook instructions in a safe, controlled environment.

The typical workflow involves:
1. **Creating model virtual plugins** that resemble the structure and capabilities of real systems
2. **Developing and testing playbooks** against these virtual models to validate agent behavior
3. **Testing the same playbooks** against real plugins to ensure they work in production
4. **Reproducing and debugging issues** by modifying virtual plugins when problems occur
5. **Iterating safely** to develop solutions in the virtual environment before real deployment

Think of this as a simulation framework where virtual plugins serve as the "wind tunnel" for testing AI orchestration systems before they encounter real-world complexity.

## 🤔 Why This Matters for Application Developers

If you're not familiar with ML modeling, you might wonder why we need "virtual" or "dummy" plugins. Here's why this approach is valuable:

### Traditional Testing vs. AI Agent Testing

**Traditional Software Testing:**
- You write unit tests that call specific functions
- Tests are deterministic and predictable
- You test exact inputs → exact outputs

**AI Agent Testing:**
- AI agents make decisions and process steps you don't fully control
- Tests need to validate reasoning processes, not just outputs
- You need to test scenarios and edge cases, not just happy paths

### The Value of Virtual Plugins

**Safe Experimentation**: Virtual plugins let you test AI agents without risking production systems. You can create scenarios that would be dangerous or expensive to reproduce in real environments.

**Realistic Complexity**: Unlike simple unit tests, virtual plugins provide realistic complexity that exercises the agent's full capabilities - file operations, error handling, decision making, etc.

**Reproducible Debugging**: When an AI agent makes a mistake, you can reproduce the exact conditions in the virtual environment to understand what went wrong and fix it.

**Skill Development**: Just as pilots use flight simulators to practice, developers can use virtual plugins to practice AI agent orchestration skills safely.

This approach bridges the gap between simple unit tests and complex real-world systems, providing the "just right" level of complexity for developing and validating AI orchestration capabilities.

## 🔍 The Virtual Plugin Innovation

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
