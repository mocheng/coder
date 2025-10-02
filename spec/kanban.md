# KANBAN Board

## Backlog

### K005: Integrate LLM with CR Command
**Description:** Connect file reading with LLM to provide actual code review
**Acceptance Criteria:**
- Send file content to LLM for code review
- Display LLM response instead of placeholder message
- Handle LLM API errors gracefully
- Provide meaningful code review output

## Ready

## In Progress

## Review

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
