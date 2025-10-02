"""Source Collector - Collect source code from various inputs"""

from dataclasses import dataclass
from typing import List
from .input_parser import ReviewInput, ReviewType
from .tool_ops import read_file_content
from .git_operations import GitOperations, GitDiffFile


@dataclass
class SourceFile:
    """Represents a source file with content and metadata"""
    path: str
    content: str
    size: int
    lines: int
    is_diff: bool = False
    diff_info: dict = None


class SourceCollector:
    """Collect source code from various input types"""
    
    def __init__(self):
        """Initialize source collector"""
        self.git_ops = GitOperations()
    
    def collect(self, review_input: ReviewInput) -> List[SourceFile]:
        """
        Collect source files based on review input.
        
        Args:
            review_input: Parsed review input
            
        Returns:
            List of SourceFile objects
            
        Raises:
            ValueError: If collection fails
        """
        if review_input.review_type == ReviewType.SINGLE_FILE:
            return self._collect_single_file(review_input.target)
        
        elif review_input.review_type == ReviewType.GIT_DIFF:
            return self._collect_git_diff()
        
        elif review_input.review_type == ReviewType.GIT_COMMIT:
            return self._collect_git_commit(review_input.target)
        
        elif review_input.review_type == ReviewType.GIT_BRANCH:
            return self._collect_git_branch(review_input.target)
        
        else:
            raise ValueError(f"Unsupported review type: {review_input.review_type}")
    
    def _collect_single_file(self, file_path: str) -> List[SourceFile]:
        """Collect single file content"""
        try:
            content = read_file_content(file_path)
            
            source_file = SourceFile(
                path=file_path,
                content=content,
                size=len(content),
                lines=len(content.splitlines()),
                is_diff=False
            )
            
            return [source_file]
            
        except Exception as e:
            raise ValueError(f"Failed to read file '{file_path}': {e}")
    
    def _collect_git_diff(self) -> List[SourceFile]:
        """Collect git staged changes"""
        try:
            diff_output = self.git_ops.get_staged_diff()
            diff_files = self.git_ops.parse_diff(diff_output)
            
            source_files = []
            for diff_file in diff_files:
                # Create content focusing on changed lines
                content = self._create_diff_content(diff_file)
                
                source_file = SourceFile(
                    path=diff_file.file_path,
                    content=content,
                    size=len(content),
                    lines=len(content.splitlines()),
                    is_diff=True,
                    diff_info={
                        "added_lines": len(diff_file.added_lines),
                        "removed_lines": len(diff_file.removed_lines),
                        "type": "staged_changes"
                    }
                )
                source_files.append(source_file)
            
            return source_files
            
        except Exception as e:
            raise ValueError(f"Failed to collect git diff: {e}")
    
    def _collect_git_commit(self, commit_hash: str) -> List[SourceFile]:
        """Collect git commit changes"""
        try:
            diff_output = self.git_ops.get_commit_diff(commit_hash)
            diff_files = self.git_ops.parse_diff(diff_output)
            
            source_files = []
            for diff_file in diff_files:
                content = self._create_diff_content(diff_file)
                
                source_file = SourceFile(
                    path=diff_file.file_path,
                    content=content,
                    size=len(content),
                    lines=len(content.splitlines()),
                    is_diff=True,
                    diff_info={
                        "added_lines": len(diff_file.added_lines),
                        "removed_lines": len(diff_file.removed_lines),
                        "type": "commit",
                        "commit_hash": commit_hash
                    }
                )
                source_files.append(source_file)
            
            return source_files
            
        except Exception as e:
            raise ValueError(f"Failed to collect git commit: {e}")
    
    def _collect_git_branch(self, branch: str) -> List[SourceFile]:
        """Collect git branch changes"""
        try:
            diff_output = self.git_ops.get_branch_diff(branch)
            diff_files = self.git_ops.parse_diff(diff_output)
            
            source_files = []
            for diff_file in diff_files:
                content = self._create_diff_content(diff_file)
                
                source_file = SourceFile(
                    path=diff_file.file_path,
                    content=content,
                    size=len(content),
                    lines=len(content.splitlines()),
                    is_diff=True,
                    diff_info={
                        "added_lines": len(diff_file.added_lines),
                        "removed_lines": len(diff_file.removed_lines),
                        "type": "branch",
                        "branch": branch
                    }
                )
                source_files.append(source_file)
            
            return source_files
            
        except Exception as e:
            raise ValueError(f"Failed to collect git branch: {e}")
    
    def _create_diff_content(self, diff_file: GitDiffFile) -> str:
        """
        Create focused content from git diff file.
        
        Args:
            diff_file: Parsed git diff file
            
        Returns:
            Content string focusing on changes
        """
        lines = []
        
        # Add file header
        lines.append(f"File: {diff_file.file_path}")
        lines.append("")
        
        # Add removed lines (for context)
        if diff_file.removed_lines:
            lines.append("=== REMOVED LINES ===")
            for line_num, content in diff_file.removed_lines:
                lines.append(f"- {line_num}: {content}")
            lines.append("")
        
        # Add added lines (main focus)
        if diff_file.added_lines:
            lines.append("=== ADDED LINES ===")
            for line_num, content in diff_file.added_lines:
                lines.append(f"+ {line_num}: {content}")
            lines.append("")
        
        # Add some context lines
        if diff_file.context_lines:
            lines.append("=== CONTEXT ===")
            for line_num, content in diff_file.context_lines[:10]:  # Limit context
                lines.append(f"  {line_num}: {content}")
        
        return "\n".join(lines)
