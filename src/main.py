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
def cr(
    target: str = typer.Argument(..., help="File path, or working directory for git operations"),
    diff: bool = typer.Option(False, "--diff", help="Review staged git changes"),
    commit: str = typer.Option(None, "--commit", help="Review specific commit"),
    branch: str = typer.Option(None, "--branch", help="Review branch changes")
):
    """Code review for files or git changes"""
    
    # Initialize components
    input_parser = InputParser()
    source_collector = SourceCollector()
    formatter = ResultsFormatter(console)
    
    try:
        # Parse and validate input
        review_input = input_parser.parse(target, diff=diff, commit=commit, branch=branch)
        
        # For single files, check if it's a text file
        if review_input.review_type.value == "single_file":
            if not is_text_file(target):
                console.print(f"[yellow]Warning: '{target}' may not be a text file[/yellow]")
        
        # Collect source files
        if review_input.review_type.value == "single_file":
            console.print("📁 Reading file...", style="bold yellow")
        else:
            console.print("🔍 Collecting git changes...", style="bold yellow")
        
        source_files = source_collector.collect(review_input)
        
        if not source_files:
            formatter.display_error("No files found to review")
            raise typer.Exit(1)
        
        # Display collection info
        if len(source_files) == 1 and not source_files[0].is_diff:
            # Single file - show file info
            formatter.display_file_info(source_files[0])
        else:
            # Multiple files or git diff - show summary
            formatter.display_git_summary(source_files, review_input)
        
        # Initialize LLM client and orchestrator
        formatter.display_progress("🤖 Analyzing code with AI...")
        
        try:
            llm_client = LLMClient()
            orchestrator = ReviewOrchestrator(llm_client)
            
            # Perform reviews
            results = orchestrator.review(source_files)
            
            # Display results
            if len(results) == 1 and not results[0].is_diff:
                # Single file result
                formatter.display_review_result(results[0], source_files[0])
            else:
                # Multiple files or git results
                formatter.display_git_results(results, source_files)
            
        except Exception as llm_error:
            console.print(f"\n[red]⚠️  LLM Error: {llm_error}[/red]")
            
            # Show fallback info
            if len(source_files) == 1 and not source_files[0].is_diff:
                # Single file fallback
                lines = source_files[0].content.splitlines()
                preview_lines = lines[:10]
                preview_content = "\n".join(f"{i:3}: {line}" for i, line in enumerate(preview_lines, 1))
                
                if len(lines) > 10:
                    preview_content += f"\n... ({len(lines) - 10} more lines)"
                
                console.print(Panel(
                    preview_content,
                    title="📄 File Content Preview (LLM unavailable)",
                    border_style="yellow"
                ))
            else:
                # Git fallback
                console.print(f"\n📄 Collected {len(source_files)} files with changes (LLM unavailable)")
                for source_file in source_files:
                    info = f"• {source_file.path}"
                    if source_file.is_diff and source_file.diff_info:
                        info += f" (+{source_file.diff_info.get('added_lines', 0)} -{source_file.diff_info.get('removed_lines', 0)})"
                    console.print(info)
        
    except ValueError as e:
        formatter.display_error(str(e))
        raise typer.Exit(1)
    except Exception as e:
        formatter.display_error(f"Unexpected error: {e}")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
