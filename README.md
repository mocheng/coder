# CLI Coding Agent

A command-line tool that provides AI-powered code review and analysis using LLM integration.

## Features

- **Code Review**: Analyze code files with AI-powered feedback
- **Multiple LLM Support**: Uses litellm for flexible model selection
- **File Operations**: Safe file reading with encoding detection
- **Modern CLI**: Built with typer for excellent user experience

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd coder
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY
```

## Usage

### Code Review
Review a single file:
```bash
python src/main.py cr path/to/your/file.py
```

### Help
Show available commands:
```bash
python src/main.py --help
```

## Configuration

Configure the tool using environment variables in `.env`:

- `GOOGLE_API_KEY`: Your Google AI API key (required)
- `CODER_LLM_MODEL`: LLM model to use (default: gemini/gemini-2.5-flash)
- `CODER_API_TIMEOUT`: API timeout in seconds (default: 30)
- `CODER_MAX_TOKENS`: Maximum tokens for responses (default: 2000)
- `CODER_TEMPERATURE`: LLM temperature setting (default: 0.1)

## Testing

Test the LLM integration:
```bash
python test_llm.py
```

## Project Structure

```
coder/
├── src/
│   ├── __init__.py          # Package initialization
│   ├── main.py              # CLI entry point
│   ├── llm_client.py        # LLM integration
│   ├── tool_ops.py          # File operations
│   └── config.py            # Configuration management
├── spec/
│   ├── kanban.md            # Project KANBAN board
│   ├── workflow.md          # Development workflow
│   └── architecture.md      # System architecture
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## Development

This project follows a KANBAN-style development workflow with AI assistance. See `spec/workflow.md` for details.

## License

[Add your license here]
