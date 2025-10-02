"""Results Formatter - Format and display single file review results"""

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.markdown import Markdown
from .source_collector import SourceFile
from .review_orchestrator import ReviewResult
from .code_context import display_code_with_feedback


class ResultsFormatter:
    """Format and display single file review results"""
    
    def __init__(self, console: Console):
        """
        Initialize results formatter.
        
        Args:
            console: Rich console for output
        """
        self.console = console
    
    def display_file_info(self, source_file: SourceFile):
        """Display file information"""
        info_text = Text()
        info_text.append("📁 File: ", style="bold")
        info_text.append(source_file.path, style="cyan")
        info_text.append(f"\n📏 Size: {source_file.size} characters")
        info_text.append(f"\n📄 Lines: {source_file.lines}")
        
        self.console.print(Panel(info_text, title="File Information", border_style="blue"))
    
    def display_review_result(self, result: ReviewResult, source_file: SourceFile):
        """Display review result"""
        if result.success:
            self.console.print("\n")
            self.console.print(Panel(
                Markdown(result.review_content),
                title="📋 CODE REVIEW RESULTS",
                border_style="green"
            ))
            
            # Display code context with line-specific feedback
            display_code_with_feedback(
                self.console, 
                source_file.content, 
                result.review_content, 
                source_file.path
            )
        else:
            self.console.print(f"\n[red]⚠️  {result.review_content}[/red]")
    
    def display_progress(self, message: str):
        """Display progress message"""
        self.console.print(f"\n{message}", style="bold yellow")
