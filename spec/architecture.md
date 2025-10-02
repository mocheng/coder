# CLI Coding Agent - Architecture Specification

## Project Objective

Build a command-line tool that leverages LLM capabilities to assist with code review, generation, and modification tasks. The agent should be simple, extensible, and cost-effective.

## Core Principles

1. **LLM-First:** All code understanding and analysis handled by LLM
2. **Minimal Viable Product:** Start simple, add complexity only when proven necessary
3. **Cost Conscious:** Use free/cheap models (gemini-flash) as default
4. **Extensible:** Support multiple LLM providers through unified interface
5. **Safe Operations:** Never modify files without explicit user consent
6. **Test-Driven Development:** Every feature must include comprehensive unit tests

## High-Level Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   CLI Interface │────│  Input Parser   │────│ Source Collector│────│Review Orchestrator│
│   (main.py)     │    │                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘    └─────────────────┘
                                                                              │
┌─────────────────┐    ┌─────────────────┐                                   │
│Results Formatter│────│  Code Context   │                                   │
│                 │    │   Display       │                                   │
└─────────────────┘    └─────────────────┘                                   │
                                                                              │
                       ┌─────────────────┐    ┌─────────────────┐            │
                       │  Tool Operations│    │   LLM Client    │────────────┘
                       │                 │    │   (litellm)     │
                       └─────────────────┘    └─────────────────┘
```

## Component Responsibilities

### CLI Interface (main.py)
- Parse command-line arguments with typer
- Coordinate workflow between modular components
- Handle user interactions and error display
- Maintain backward compatibility with existing interface

### Input Parser (input_parser.py)
- Parse and validate single file input
- Provide structured input validation
- Extensible for future input types (directories, git)
- Clean error handling and reporting

### Source Collector (source_collector.py)
- Collect source code content from single file
- Provide file metadata (size, lines, path)
- Handle file reading errors gracefully
- Extensible for future source types

### Review Orchestrator (review_orchestrator.py)
- Manage single file code review workflow
- Coordinate with LLM client for reviews
- Handle LLM errors and provide fallback
- Extensible for multi-file orchestration

### Results Formatter (results_formatter.py)
- Format and display review results with rich
- Show file information and progress messages
- Display review results with markdown formatting
- Integrate with code context display system

### LLM Client (llm_client.py)
- Abstract LLM provider differences
- Handle API calls and retries
- Manage model configuration
- Process responses

### Code Context Display (code_context.py)
- Parse line-specific feedback from LLM responses
- Display code snippets with syntax highlighting
- Show context around problematic lines
- Integrate with rich formatting system

### Tool Operations (tool_ops.py)
- File reading/writing operations
- Text file detection and encoding handling
- Basic file system utilities

## Technology Constraints

- **Language:** Python 3.12+
- **LLM Library:** litellm (unified interface)
- **Default Model:** gemini/gemini-1.5-flash
- **CLI Framework:** typer
- **UI Library:** rich (terminal formatting)
- **Testing:** unittest/pytest
- **Dependencies:** Minimal, prefer standard library

## Project Structure

```
coder/
├── src/                     # Source code
│   ├── __init__.py          # Package initialization
│   ├── main.py              # CLI entry point (typer)
│   ├── llm_client.py        # LLM integration (litellm)
│   ├── tool_ops.py          # File operations
│   ├── config.py            # Configuration management
│   └── code_context.py      # Code context display (rich)
├── tests/                   # Unit tests
│   ├── __init__.py          # Test package initialization
│   └── test_main.py         # Main CLI functionality tests
├── spec/                    # Project specifications
│   ├── kanban.md            # Project KANBAN board
│   ├── workflow.md          # Development workflow
│   └── architecture.md      # System architecture
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
├── .gitignore              # Git ignore rules
└── README.md               # Project documentation
```

## Testing Strategy

- **Unit Tests**: Located in `tests/` directory following standard Python conventions
- **Test Discovery**: Use `python -m unittest discover tests/` or `pytest tests/`
- **Mocking**: Mock LLM API calls to avoid external dependencies during testing
- **Coverage**: Test CLI commands, core functions, and error handling
- **Mandatory Testing**: Every new feature must include corresponding unit tests
- **Test-First Development**: Write tests alongside or before implementation
- **Minimum Coverage**: Each new module must have at least 80% test coverage
- **Test Organization**: Mirror source structure in tests/ directory (test_module.py for module.py)
- **Coverage Enforcement**: All test runs must show coverage and fail if below 80%
- **Coverage Commands**: 
  - `pytest tests/ --cov=src --cov-fail-under=80 --cov-report=term-missing`

## Security & Safety

- Never execute code without explicit user approval
- Create backups before file modifications
- Validate file paths to prevent directory traversal
- Sanitize LLM responses before operations
- Respect file permissions and ownership

## Initial Commands

1. `cr <file>` - Code review for specified file
2. `help` - Show usage information
3. `config` - Manage configuration (future)

## Non-Goals (Initially)

- Built-in code execution
- Complex project management features
- GUI interface
- Real-time collaboration
