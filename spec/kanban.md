# KANBAN Board

## Backlog

## Ready

## In Progress

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
