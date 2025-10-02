# CLI Coding Agent - Architecture Specification

## Project Objective

Build a command-line tool that leverages LLM capabilities to assist with code review, generation, and modification tasks. The agent should be simple, extensible, and cost-effective.

## Core Principles

1. **LLM-First:** All code understanding and analysis handled by LLM
2. **Minimal Viable Product:** Start simple, add complexity only when proven necessary
3. **Cost Conscious:** Use free/cheap models (gemini-flash) as default
4. **Extensible:** Support multiple LLM providers through unified interface
5. **Safe Operations:** Never modify files without explicit user consent

## High-Level Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   CLI Interface │────│  Core Agent     │────│  LLM Client     │
│   (click/argparse)   │  (orchestration)│    │  (litellm)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                       ┌─────────────────┐
                       │  Tool Operations│
                       │  (file/git/etc) │
                       └─────────────────┘
```

## Component Responsibilities

### CLI Interface
- Parse command-line arguments
- Validate user input
- Display results and errors
- Handle user interactions

### Core Agent
- Orchestrate workflow between components
- Manage conversation context
- Apply business logic and safety checks
- Format prompts for LLM

### LLM Client
- Abstract LLM provider differences
- Handle API calls and retries
- Manage model configuration
- Process responses

### Tool Operations
- File reading/writing operations
- Git command execution
- Directory traversal
- System command execution

## Technology Constraints

- **Language:** Python 3.12+
- **LLM Library:** litellm (unified interface)
- **Default Model:** gemini/gemini-1.5-flash
- **CLI Framework:** click or argparse
- **Dependencies:** Minimal, prefer standard library

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
