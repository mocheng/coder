#!/usr/bin/env python3
"""CLI Coding Agent - Main Entry Point"""

import sys
from pathlib import Path
import typer
from .tool_ops import read_file_content, is_text_file
from .llm_client import LLMClient


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
    
    # Basic validation (already exists in tool_ops, but keep for early feedback)
    if not file_path.exists():
        typer.echo(f"Error: File '{file}' not found", err=True)
        raise typer.Exit(1)
    
    if not file_path.is_file():
        typer.echo(f"Error: '{file}' is not a file", err=True)
        raise typer.Exit(1)
    
    # Check if it's a text file
    if not is_text_file(file):
        typer.echo(f"Warning: '{file}' may not be a text file", err=True)
    
    try:
        # Read file content
        content = read_file_content(file)
        
        # Display basic file info
        typer.echo(f"Code review for: {file}")
        typer.echo(f"File size: {len(content)} characters")
        typer.echo(f"Lines: {len(content.splitlines())}")
        
        # Initialize LLM client and perform code review
        typer.echo("\n🤖 Analyzing code with AI...")
        
        try:
            llm_client = LLMClient()
            review_result = llm_client.code_review(content, file)
            
            typer.echo("\n" + "="*60)
            typer.echo("📋 CODE REVIEW RESULTS")
            typer.echo("="*60)
            typer.echo(review_result)
            typer.echo("="*60)
            
        except Exception as llm_error:
            typer.echo(f"\n⚠️  LLM Error: {llm_error}", err=True)
            typer.echo("\n📄 File Content Preview (LLM unavailable):")
            typer.echo("-" * 40)
            
            # Show first 10 lines as fallback
            lines = content.splitlines()
            preview_lines = lines[:10]
            for i, line in enumerate(preview_lines, 1):
                typer.echo(f"{i:3}: {line}")
            
            if len(lines) > 10:
                typer.echo(f"... ({len(lines) - 10} more lines)")
        
    except FileNotFoundError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)
    except PermissionError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)
    except UnicodeDecodeError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)
    except Exception as e:
        typer.echo(f"Unexpected error: {e}", err=True)
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
