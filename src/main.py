#!/usr/bin/env python3
"""CLI Coding Agent - Main Entry Point"""

import sys
from pathlib import Path
import typer


app = typer.Typer(help="CLI Coding Agent - LLM-powered code assistance")


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """CLI Coding Agent - LLM-powered code assistance"""
    if ctx.invoked_subcommand is None:
        typer.echo("CLI Coding Agent - LLM-powered code assistance")
        typer.echo("Use --help to see available commands")


@app.command()
def cr(file: str):
    """Code review for a file"""
    file_path = Path(file)
    
    # Basic validation
    if not file_path.exists():
        typer.echo(f"Error: File '{file}' not found", err=True)
        raise typer.Exit(1)
    
    if not file_path.is_file():
        typer.echo(f"Error: '{file}' is not a file", err=True)
        raise typer.Exit(1)
    
    # Placeholder for actual code review functionality
    typer.echo(f"Code review for: {file}")
    typer.echo("(LLM integration coming soon)")


if __name__ == "__main__":
    app()
