#!/usr/bin/env python3
"""CLI Coding Agent - Main Entry Point"""

from pathlib import Path
import typer
from rich.console import Console
from rich.panel import Panel
from .tool_ops import is_text_file
from .input_parser import InputParser
from .source_collector import SourceCollector
from .review_orchestrator import ReviewOrchestrator
from .results_formatter import ResultsFormatter
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
    
    # Initialize components
    input_parser = InputParser()
    source_collector = SourceCollector()
    formatter = ResultsFormatter(console)
    
    try:
        # Parse and validate input
        review_input = input_parser.parse(file)
        
        # Check if it's a text file
        if not is_text_file(file):
            console.print(f"[yellow]Warning: '{file}' may not be a text file[/yellow]")
        
        # Collect source file
        source_file = source_collector.collect(review_input)
        
        # Display file info
        formatter.display_file_info(source_file)
        
        # Initialize LLM client and orchestrator
        formatter.display_progress("🤖 Analyzing code with AI...")
        
        try:
            llm_client = LLMClient()
            orchestrator = ReviewOrchestrator(llm_client)
            
            # Perform review
            result = orchestrator.review(source_file)
            
            # Display results
            formatter.display_review_result(result, source_file)
            
        except Exception as llm_error:
            console.print(f"\n[red]⚠️  LLM Error: {llm_error}[/red]")
            
            # Show file preview as fallback
            lines = source_file.content.splitlines()
            preview_lines = lines[:10]
            preview_content = "\n".join(f"{i:3}: {line}" for i, line in enumerate(preview_lines, 1))
            
            if len(lines) > 10:
                preview_content += f"\n... ({len(lines) - 10} more lines)"
            
            console.print(Panel(
                preview_content,
                title="📄 File Content Preview (LLM unavailable)",
                border_style="yellow"
            ))
        
    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]Unexpected error: {e}[/red]")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
