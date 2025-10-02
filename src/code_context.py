"""Code Context Display - Parse feedback and show code snippets with line numbers"""

import re
from typing import List, Tuple, Dict
from rich.console import Console
from rich.syntax import Syntax
from rich.panel import Panel
from rich.columns import Columns
from rich.text import Text


def parse_line_references(review_text: str) -> List[int]:
    """
    Extract line numbers from review text.
    
    Args:
        review_text: LLM review response
        
    Returns:
        List of line numbers referenced in the review
    """
    # Find all "Line X:" patterns
    pattern = r'Line (\d+):'
    matches = re.findall(pattern, review_text, re.IGNORECASE)
    return [int(match) for match in matches]


def get_code_context(file_content: str, line_number: int, context_lines: int = 3) -> Tuple[str, int, int]:
    """
    Get code context around a specific line.
    
    Args:
        file_content: Full file content
        line_number: Target line number (1-based)
        context_lines: Number of lines to show before/after
        
    Returns:
        Tuple of (context_code, start_line, end_line)
    """
    lines = file_content.splitlines()
    total_lines = len(lines)
    
    # Convert to 0-based indexing
    target_idx = line_number - 1
    
    # Calculate context range
    start_idx = max(0, target_idx - context_lines)
    end_idx = min(total_lines, target_idx + context_lines + 1)
    
    # Extract context lines
    context_lines_list = lines[start_idx:end_idx]
    context_code = '\n'.join(context_lines_list)
    
    return context_code, start_idx + 1, end_idx


def display_code_with_feedback(console: Console, file_content: str, review_text: str, file_path: str):
    """
    Display code snippets with associated feedback.
    
    Args:
        console: Rich console instance
        file_content: Full file content
        review_text: LLM review response
        file_path: Path to the file
    """
    line_refs = parse_line_references(review_text)
    
    if not line_refs:
        # No line references found, check if there are any issues at all
        if len(review_text.strip()) < 50 or "no issues" in review_text.lower():
            console.print("\n")
            console.print(Panel(
                "✅ No specific issues found that require code changes",
                title="📍 Code Analysis",
                border_style="green"
            ))
        return
    
    # Get file extension for syntax highlighting
    file_ext = file_path.split('.')[-1] if '.' in file_path else 'text'
    
    console.print("\n")
    console.print(Panel(
        f"Found {len(line_refs)} issues requiring attention",
        title="⚠️  Issues Found",
        border_style="red"
    ))
    
    # Display each referenced line with context
    for line_num in sorted(set(line_refs)):  # Remove duplicates and sort
        context_code, start_line, end_line = get_code_context(file_content, line_num)
        
        # Create syntax highlighted code
        syntax = Syntax(
            context_code,
            file_ext,
            line_numbers=True,
            start_line=start_line,
            highlight_lines={line_num}
        )
        
        # Extract feedback for this line
        feedback = extract_line_feedback(review_text, line_num)
        
        # Create feedback text
        feedback_text = Text()
        feedback_text.append(f"Line {line_num}: ", style="bold red")
        feedback_text.append(feedback, style="white")
        
        # Display code and feedback
        console.print(f"\n[bold red]Issue at Line {line_num}:[/bold red]")
        console.print(syntax)
        console.print(Panel(feedback_text, border_style="red", padding=(0, 1)))


def extract_line_feedback(review_text: str, line_number: int) -> str:
    """
    Extract feedback text for a specific line number.
    
    Args:
        review_text: Full review text
        line_number: Target line number
        
    Returns:
        Feedback text for the line
    """
    # Find the line reference and extract following text
    pattern = rf'Line {line_number}:\s*([^\n]*(?:\n(?!Line \d+:)[^\n]*)*)'
    match = re.search(pattern, review_text, re.IGNORECASE | re.MULTILINE)
    
    if match:
        feedback = match.group(1).strip()
        # Clean up the feedback (remove excessive whitespace)
        feedback = re.sub(r'\n\s*\n', '\n', feedback)
        return feedback
    
    return f"Referenced in review (line {line_number})"
