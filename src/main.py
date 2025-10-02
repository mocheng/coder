#!/usr/bin/env python3
"""CLI Coding Agent - Main Entry Point"""

import sys
from pathlib import Path
import typer
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text
from .tool_ops import read_file_content, is_text_file
from .llm_client import LLMClient


app = typer.Typer(help="CLI Coding Agent - LLM-powered code assistance")
console = Console()


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """CLI Coding Agent - LLM-powered code assistance"""
    if ctx.invoked_subcommand is None:
        console.print("CLI Coding Agent - LLM-powered code assistance", style="bold blue")
        console.print("Use --help to see available commands")


@app.command()
def cr(file: str):
    """Code review for a file"""
    file_path = Path(file)
    
    # Basic validation
    if not file_path.exists():
        console.print(f"[red]Error: File '{file}' not found[/red]")
        raise typer.Exit(1)
    
    if not file_path.is_file():
        console.print(f"[red]Error: '{file}' is not a file[/red]")
        raise typer.Exit(1)
    
    # Check if it's a text file
    if not is_text_file(file):
        console.print(f"[yellow]Warning: '{file}' may not be a text file[/yellow]")
    
    try:
        # Read file content
        content = read_file_content(file)
        
        # Display file info with rich formatting
        info_text = Text()
        info_text.append("📁 File: ", style="bold")
        info_text.append(file, style="cyan")
        info_text.append(f"\n📏 Size: {len(content)} characters")
        info_text.append(f"\n📄 Lines: {len(content.splitlines())}")
        
        console.print(Panel(info_text, title="File Information", border_style="blue"))
        
        # Initialize LLM client and perform code review
        console.print("\n🤖 Analyzing code with AI...", style="bold yellow")
        
        try:
            llm_client = LLMClient()
            review_result = llm_client.code_review(content, file)
            
            # Display review results with rich markdown formatting
            console.print("\n")
            console.print(Panel(
                Markdown(review_result),
                title="📋 CODE REVIEW RESULTS",
                border_style="green"
            ))
            
        except Exception as llm_error:
            console.print(f"\n[red]⚠️  LLM Error: {llm_error}[/red]")
            
            # Show file preview as fallback
            lines = content.splitlines()
            preview_lines = lines[:10]
            preview_content = "\n".join(f"{i:3}: {line}" for i, line in enumerate(preview_lines, 1))
            
            if len(lines) > 10:
                preview_content += f"\n... ({len(lines) - 10} more lines)"
            
            console.print(Panel(
                preview_content,
                title="📄 File Content Preview (LLM unavailable)",
                border_style="yellow"
            ))
        
    except FileNotFoundError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)
    except PermissionError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)
    except UnicodeDecodeError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]Unexpected error: {e}[/red]")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
