"""Results Formatter - Format and display review results"""

from typing import List
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.markdown import Markdown
from rich.table import Table
from .source_collector import SourceFile
from .review_orchestrator import ReviewResult
from .input_parser import ReviewInput, ReviewType
from .code_context import display_code_with_feedback


class ResultsFormatter:
    """Format and display review results"""
    
    def __init__(self, console: Console):
        """
        Initialize results formatter.
        
        Args:
            console: Rich console for output
        """
        self.console = console
    
    def display_file_info(self, source_file: SourceFile):
        """Display single file information"""
        info_text = Text()
        info_text.append("📁 File: ", style="bold")
        info_text.append(source_file.path, style="cyan")
        info_text.append(f"\n📏 Size: {source_file.size} characters")
        info_text.append(f"\n📄 Lines: {source_file.lines}")
        
        self.console.print(Panel(info_text, title="File Information", border_style="blue"))
    
    def display_git_summary(self, source_files: List[SourceFile], review_input: ReviewInput):
        """Display git changes summary"""
        info_text = Text()
        
        if review_input.review_type == ReviewType.GIT_DIFF:
            info_text.append("🔄 Git Staged Changes", style="bold")
        elif review_input.review_type == ReviewType.GIT_COMMIT:
            info_text.append(f"📝 Git Commit: {review_input.target}", style="bold")
        elif review_input.review_type == ReviewType.GIT_BRANCH:
            info_text.append(f"🌿 Git Branch: {review_input.target}", style="bold")
        
        info_text.append(f"\n📁 Files Changed: {len(source_files)}")
        
        total_added = sum(f.diff_info.get('added_lines', 0) for f in source_files if f.diff_info)
        total_removed = sum(f.diff_info.get('removed_lines', 0) for f in source_files if f.diff_info)
        
        info_text.append(f"\n➕ Lines Added: {total_added}")
        info_text.append(f"\n➖ Lines Removed: {total_removed}")
        
        self.console.print(Panel(info_text, title="Git Changes Summary", border_style="blue"))
    
    def display_git_results(self, results: List[ReviewResult], source_files: List[SourceFile]):
        """Display git review results"""
        # Summary table
        table = Table(title="📋 Git Review Summary")
        table.add_column("File", style="cyan")
        table.add_column("Status", style="bold")
        table.add_column("Changes", style="yellow")
        
        issues_found = 0
        for result in results:
            if result.success and result.review_content.strip():
                # Count issues (simple heuristic)
                issue_count = result.review_content.count("Line ") + result.review_content.count("issue") + result.review_content.count("problem")
                if issue_count > 0:
                    issues_found += 1
                    status = f"⚠️  {issue_count} issues"
                else:
                    status = "✅ Clean"
            else:
                status = "❌ Error" if not result.success else "✅ Clean"
            
            changes = ""
            if result.diff_info:
                added = result.diff_info.get('added_lines', 0)
                removed = result.diff_info.get('removed_lines', 0)
                changes = f"+{added} -{removed}"
            
            table.add_row(result.file_path, status, changes)
        
        self.console.print(table)
        
        # Detailed results for files with issues
        files_with_issues = [r for r in results if r.success and r.review_content.strip() and 
                           ("Line " in r.review_content or "issue" in r.review_content.lower() or "problem" in r.review_content.lower())]
        
        if files_with_issues:
            self.console.print(f"\n[bold red]Found issues in {len(files_with_issues)} files:[/bold red]")
            
            for result in files_with_issues:
                self.console.print(f"\n[bold cyan]File: {result.file_path}[/bold cyan]")
                
                if result.diff_info:
                    diff_type = result.diff_info.get('type', 'changes')
                    self.console.print(f"[yellow]Git {diff_type} review[/yellow]")
                
                self.console.print(Panel(
                    Markdown(result.review_content),
                    title=f"📋 Issues in {result.file_path}",
                    border_style="red"
                ))
        else:
            self.console.print("\n")
            self.console.print(Panel(
                "✅ No issues found in git changes",
                title="🎉 All Clean!",
                border_style="green"
            ))
    
    def display_review_result(self, result: ReviewResult, source_file: SourceFile):
        """Display single file review result"""
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
    
    def display_error(self, message: str):
        """Display error message"""
        self.console.print(f"[red]Error: {message}[/red]")
    
    def display_warning(self, message: str):
        """Display warning message"""
        self.console.print(f"[yellow]Warning: {message}[/yellow]")
