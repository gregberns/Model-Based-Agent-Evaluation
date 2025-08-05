# Next Steps Plan

## Executive Summary

We're following the master plan outlined in [`docs/project-plan/00_master_plan.md`](./docs/project-plan/00_master_plan.md). We're currently in Phase 2 (The Orchestrator and Agent Integration) and focusing on building robust tool combinations and agent reasoning capabilities. We've completed the foundation work and are now building up to complex multi-step operations through an incremental TDD approach.

## Current State Assessment

### What's Working ✅
- Core framework infrastructure (Orchestrator, Event System, Tool Wrappers)
- All individual tools tested and working: `read_file`, `write_file`, `list_files`, `execute_shell_command`, `edit_file`
- Simple tool combinations working (e.g., `read_file` + `write_file` for file copying)
- Virtual plugin factory and evaluation harness are functional
- Event-driven architecture with tool wrapping is implemented

### What's Not Working Yet
- Complex multi-step playbooks (like `fix_bug`) are still being developed
- Agent reasoning for context-based operations needs more validation
- Need to build up to complex operations through validated intermediate steps

## Architecture Principles

### Tool Wrapper Design
- **Core Framework**: Expects simple callable tools
- **Testing**: Uses pure `event_emitting_wrapper` for deterministic testing
- **Flexibility**: Tool wrappers can be configured for different environments

### Incremental Development (Following Master Plan)
- **Foundation Complete**: Individual tools validated and working
- **Combinations in Progress**: Building up to multi-step operations gradually
- **Reasoning Next**: Context-based operations after combinations are solid
- **Complex Operations Final**: Multi-step operations after foundation is complete

## Development Phases (Aligned with Master Plan)

### Phase 1: The Virtual Plugin and Evaluation Foundation ✅ COMPLETED
- Plugin model schema with Pydantic validation ✅
- Virtual plugin factory with Jinja2 templating ✅
- Evaluation harness for end-to-end testing ✅
- Initial playbook development ✅

### Phase 2: The Orchestrator and Agent Integration 🔄 IN PROGRESS
- Composable Orchestrator components ✅
- Event system and tool wrappers ✅
- Gemini Agent integration ✅
- End-to-end evaluation (in progress) 🔄

**Current Focus Areas:**
1. **Tool Combinations**: Validate simple two-tool combinations
2. **Agent Reasoning**: Test context-based operations
3. **Playbook Development**: Build up to complex operations

### Phase 3: Real Plugin Environment and CLI (Future)
- Implement real environment logic
- Build core CLI interface
- Create first real plugin

## Immediate Action Plan

### Phase 2A: Tool Combination Validation

1. **Complete Two-Tool Combinations**
   - ✅ `read_file` + `write_file` - Copy file content (playbook_copy_file)
   - 🔄 `list_files` + `read_file` - Process specific file from list
   - 🔄 `execute_shell_command` + `read_file` - Execute command and capture output

2. **Combination Validation Criteria**
   - Each combination must work reliably end-to-end
   - State must be maintained between tool calls
   - Context must be properly passed between steps
   - Error handling must work across tool boundaries

### Phase 2B: Reasoning and Context-Based Operations

1. **Simple File Modification Playbooks**
   - 🔄 `playbook_update_description.md` - Read profile, modify description
   - 🔄 `playbook_update_version.md` - Read profile, update version
   - 🔄 `playbook_add_behavior.md` - Read profile, add behavioral scenario

2. **Reasoning Validation**
   - Agent must correctly understand context from previous steps
   - Reasoning must lead to correct modifications
   - Agent must identify and modify specific fields accurately
   - Edge cases must be handled properly

### Phase 2C: Build Up to Complex Operations

1. **Progressive Complexity**
   - Start with simple reasoning operations
   - Gradually increase complexity
   - Each step builds on validated previous capabilities
   - Focus on operations that mirror the `fix_bug` workflow

2. **Complex Operation Validation**
   - Multi-step operations must complete reliably
   - Complex reasoning must work correctly
   - Error recovery must work at each step
   - Performance must be reasonable

## Testing Strategy

### Deterministic Tests (Unit/Integration)
- **Location**: `evaluations/` with `_isolated.py` suffix
- **Focus**: Tool functionality, event emission, error handling
- **Examples**: `test_read_file_isolated.py`, `test_write_file_isolated.py`
- **Execution**: Fast, reliable, no external dependencies

### Agent/Playbook Tests (End-to-End)
- **Location**: `evaluations/` with `test_playbook_` prefix
- **Focus**: Agent reasoning, playbook execution, context handling
- **Examples**: `test_playbook_copy_file.py`, `test_playbook_fix_bug.py`
- **Execution**: Slower, require API key, non-deterministic

## Success Criteria

### Phase 2 Complete
- ✅ All individual tools work reliably in isolation
- ✅ Tool-specific tests pass consistently
- ✅ Event emission works correctly for all tools
- 🔄 All two-tool combinations work reliably
- 🔄 State is maintained between tool calls
- 🔄 Context is properly passed and used
- 🔄 Simple reasoning operations work reliably
- 🔄 Agent reasoning is correct for context-based operations
- 🔄 Complex operations work end-to-end

## Next Immediate Actions

1. **Complete Tool Combinations**
   - Validate `list_files` + `read_file` combination
   - Validate `execute_shell_command` + `read_file` combination
   - Create additional combination playbooks as needed

2. **Develop Reasoning Playbooks**
   - Create `playbook_update_description.md`
   - Create `playbook_update_version.md`
   - Create `playbook_add_behavior.md`
   - Write tests for each reasoning playbook

3. **Build Up to Complexity**
   - Start with simple reasoning operations
   - Progress to more complex multi-step operations
   - Eventually tackle the `fix_bug` playbook
   - Validate each step before moving to the next

4. **Maintain TDD Workflow**
   - Write tests before implementing new capabilities
   - Validate frequently at each complexity level
   - Refactor as needed to maintain clean architecture

## Questions for Consideration

1. What specific edge cases should we test for each tool combination?
2. How should we handle tool timeouts and error recovery in multi-step operations?
3. What's the best way to validate agent reasoning correctness for context-based operations?
4. Should we create a standard test structure for all playbook evaluations?
5. How do we measure when we're ready to move to the next complexity level?

This plan provides a clear path forward that aligns with the master plan. By focusing on validated tool combinations and building up gradually, we'll ensure our fundamentals are sound and develop reliable agent capabilities.