# KANBAN Board

## Backlog

### K009: Multi-File Code Review
**Description:** Extend `cr` command to handle directories and multiple files
**Acceptance Criteria:**
- Accept directory paths in `cr` command
- Recursively find code files in directories
- Review multiple files in batch with consolidated output
- Filter by file extensions (configurable)
- Handle large codebases efficiently
- Show per-file and summary results

### K010: Git Integration for Code Review
**Description:** Add git-aware code review for changes and diffs
**Acceptance Criteria:**
- Add `cr --diff` option to review staged changes
- Add `cr --commit <hash>` to review specific commit
- Add `cr --branch <branch>` to review branch changes
- Parse git diff output and focus review on changed lines
- Show context around changed code
- Integrate with existing line-specific feedback system

## Ready

## In Progress

### K008: Architecture Refinement for Multi-Scenario Code Review
**Description:** Refactor current single-file architecture to support multiple review scenarios
**Acceptance Criteria:**
- Design modular components (Input Parser, Source Collector, Review Orchestrator, Results Formatter)
- Define clear interfaces and data flow between components
- Refactor existing code to use new architecture
- Maintain backward compatibility with current `cr` command
- Create extensible foundation for future review scenarios
- Update architecture documentation

### K008: Multi-File Code Review
**Description:** Extend `cr` command to handle directories and multiple files
**Acceptance Criteria:**
- Accept directory paths in `cr` command
- Recursively find code files in directories
- Review multiple files in batch with consolidated output
- Filter by file extensions (configurable)
- Handle large codebases efficiently
- Show per-file and summary results

## Review

## Done

### K007: Source Code Context Display
**Description:** Show source code context with line numbers alongside review feedback
**Acceptance Criteria:**
- Modify LLM prompt to request line number references in feedback ✓
- Parse LLM responses to extract line-specific comments ✓
- Use rich to display source code snippets with line numbers ✓
- Highlight referenced lines in context (show ±3 lines around issues) ✓
- Format as side-by-side or sequential display: code snippet → feedback ✓
- Integrate with existing tool_ops.py file reading functionality ✓

### K006: Rich Terminal Output Integration
**Description:** Replace plain markdown output with rich library for colorful, formatted terminal display
**Acceptance Criteria:**
- Add rich dependency to requirements.txt ✓
- Integrate rich.console for output formatting in main.py ✓
- Convert LLM markdown responses to rich-formatted output ✓
- Use rich syntax highlighting for code blocks ✓
- Apply consistent color scheme (errors=red, suggestions=yellow, good=green) ✓
- Maintain compatibility with existing typer CLI structure ✓

## Done

### K001: Initialize Source Structure
**Description:** Create src folder and basic project structure
**Acceptance Criteria:**
- Create src/ directory ✓
- Add __init__.py files as needed ✓
- Set up basic module structure ✓

### K002: Basic CLI Structure
**Description:** Create main CLI entry point with `cr` command
**Acceptance Criteria:**
- CLI accepts `cr <file>` command for code review ✓
- Shows help when no arguments provided ✓
- Basic argument validation ✓

### K004: Tool Operations
**Description:** File reading and basic tool operations
**Acceptance Criteria:**
- Read file content safely ✓
- Handle file not found errors ✓
- Support common text file formats ✓

### K003: LLM Integration
**Description:** Integrate litellm for LLM communication
**Acceptance Criteria:**
- Can send text to gemini-flash model ✓
- Handle API responses and errors ✓
- Basic configuration for model selection ✓

### K005: Integrate LLM with CR Command
**Description:** Connect file reading with LLM to provide actual code review
**Acceptance Criteria:**
- Send file content to LLM for code review ✓
- Display LLM response instead of placeholder message ✓
- Handle LLM API errors gracefully ✓
- Provide meaningful code review output ✓
