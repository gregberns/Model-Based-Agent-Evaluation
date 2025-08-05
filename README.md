# Plugin Manager

## Problem

What if you needed to maintain a lot of plugins, or today a lot of MCP servers. How could you do that 'at scale' - meaning there are several hundred (or more)?

What challenges would you run into?

* Resources - only so many hours in a day
* Brain power - hard for a human to understand every plugin
* Error tracking and resolution - Prod errors tracked, debugged, fixed, deployed

## Solution

The Plugin Manager is an AI-driven orchestrator system that automates complex software maintenance tasks through standardized, version-controlled **Playbooks**. The system uses an AI agent to execute playbooks on virtual or real plugins, enabling scalable plugin maintenance with minimal human intervention.

## Architecture

The system follows a phased approach as outlined in our [master plan](docs/project-plan/00_master_plan.md):

### Phase 1: Virtual Plugin and Evaluation Foundation ✅
- Plugin model schema with Pydantic validation
- Virtual plugin factory with Jinja2 templating
- Evaluation harness for end-to-end testing

### Phase 2: Orchestrator and Agent Integration 🔄
- Event-driven architecture with tool wrapping
- Gemini Agent integration via function calling
- End-to-end playbook execution testing

### Phase 3: Real Plugin Environment and CLI (Future)
- Real plugin environment logic
- Core CLI interface
- Human-in-the-loop capabilities

## Key Components

### Core Framework
- **Orchestrator**: Manages playbook execution and tool coordination
- **Event System**: Provides observability through action logging
- **Tool Wrappers**: Wrap tools with event emission for debugging
- **Evaluation Harness**: Tests agent capabilities on virtual plugins

### Tooling System
- **read_file**: Read file contents
- **write_file**: Write content to files
- **list_files**: List directory contents
- **execute_shell_command**: Execute shell commands
- **edit_file**: Edit file contents with AI assistance

### Playbook System
- **Playbook Loader**: Parse and load playbook instructions
- **Prompt Constructor**: Build agent prompts from templates
- **Standardized Playbooks**: Version-controlled instruction sets

## Development and Testing

### Testing Strategy
The project uses a comprehensive testing strategy organized into two categories:

#### Deterministic Tests (`evaluations/deterministic/`)
- **Purpose**: Unit and integration testing for individual tools
- **Characteristics**: Fast, reliable, no external dependencies
- **Coverage**: Tool functionality, event emission, error handling
- **Command**: `pytest evaluations/deterministic/ -v`

#### Agent/Playbook Tests (`evaluations/agent/`)
- **Purpose**: End-to-end testing of agent reasoning and workflows
- **Characteristics**: Slower, require API key, non-deterministic
- **Coverage**: Agent reasoning, multi-step workflows, context handling
- **Command**: `pytest evaluations/agent/ -v`

### Development Workflow
1. **Isolated Tool Testing**: Validate individual tools in deterministic tests
2. **Combination Testing**: Test simple tool combinations
3. **Reasoning Testing**: Validate context-based operations
4. **Complex Testing**: Build up to multi-step complex operations

## Getting Started

### Prerequisites
- Python 3.8+
- Gemini API key (`GEMINI_API_KEY` environment variable)
- Virtual environment setup

### Installation
```bash
make install-deps
```

### Running Tests
```bash
# All tests
make test

# Deterministic tests only
pytest evaluations/deterministic/ -v

# Agent/playbook tests only
pytest evaluations/agent/ -v
```

### Running Playbooks
```bash
# Run a playbook on a real plugin
make run-plugin p=<plugin_name> pb=<playbook_name> [bug='<description>']

# Examples:
make run-plugin p=my-first-plugin pb=playbook_fix_bug
make run-plugin p=my-first-plugin pb=playbook_fix_bug bug='Fix whitespace issue'
```

## Project Structure

```
poc-plugin-manager/
├── docs/project-plan/           # Master plan and technical specifications
├── packages/                    # Core framework packages
│   ├── framework/              # Orchestrator and core components
│   └── plugin_manager_agent/   # Agent implementation and tools
├── playbooks/                  # Standardized playbook definitions
├── templates/                  # Virtual plugin templates
├── evaluations/                # Test suites
│   ├── deterministic/          # Unit and integration tests
│   └── agent/                  # End-to-end agent tests
├── scripts/                    # Utility scripts
└── Makefile                    # Build and development targets
```

## Current Status

### ✅ Completed
- Core framework infrastructure
- Virtual plugin factory
- Individual tool implementations
- Simple tool combinations
- Deterministic testing infrastructure

### 🔄 In Progress
- Agent reasoning validation
- Complex playbook development
- Multi-step operation testing

### 🚧 Next Steps
- Complete tool combination validation
- Develop reasoning-based playbooks
- Build up to complex operations
- Validate end-to-end workflows

## Contributing

1. Follow the TDD approach: write tests before implementing features
2. Separate deterministic and agent tests appropriately
3. Use the evaluation harness for consistent agent testing
4. Document new playbooks and tools thoroughly
5. Update documentation when adding new capabilities

## Technical Choices

I've been using Gemini CLI a lot. It's a good coding agent, so let's experiment with how we could orchestrate its use over lots of standardized things.

This ABSOLUTELY could be done differently. This may only scale so far. At some point we may need something like LangChain workflows to enforce a more formal process.

But... with something like LangChain's workflows, (I have found) you don't have the robust, well integrated tools a code agent has like Gemini.

## Documentation

- [Master Plan](docs/project-plan/00_master_plan.md)
- [Next Steps](NEXT_STEPS.md)
- [Tasks](TASKS.md)
- [Evaluations Guide](evaluations/README.md)