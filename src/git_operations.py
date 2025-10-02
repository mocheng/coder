"""Git Operations - Execute git commands and parse diff output"""

import subprocess
import re
from typing import List, Dict, Any
from dataclasses import dataclass


@dataclass
class GitDiffFile:
    """Represents a file in git diff with changes"""
    file_path: str
    old_file: str
    new_file: str
    added_lines: List[tuple]  # (line_number, content)
    removed_lines: List[tuple]  # (line_number, content)
    context_lines: List[tuple]  # (line_number, content)


class GitOperations:
    """Handle git command execution and diff parsing"""
    
    def __init__(self, working_dir: str = "."):
        """
        Initialize git operations.
        
        Args:
            working_dir: Working directory for git commands
        """
        self.working_dir = working_dir
    
    def get_staged_diff(self) -> str:
        """
        Get staged changes diff.
        
        Returns:
            Git diff output for staged changes
            
        Raises:
            ValueError: If git command fails
        """
        try:
            result = subprocess.run(
                ["git", "diff", "--cached"],
                cwd=self.working_dir,
                capture_output=True,
                text=True,
                check=True
            )
            
            if not result.stdout.strip():
                raise ValueError("No staged changes found")
            
            return result.stdout
            
        except subprocess.CalledProcessError as e:
            raise ValueError(f"Git diff failed: {e.stderr}")
        except FileNotFoundError:
            raise ValueError("Git not found - ensure git is installed")
    
    def get_commit_diff(self, commit_hash: str) -> str:
        """
        Get diff for specific commit.
        
        Args:
            commit_hash: Commit hash to review
            
        Returns:
            Git diff output for the commit
            
        Raises:
            ValueError: If git command fails
        """
        try:
            result = subprocess.run(
                ["git", "show", "--format=", commit_hash],
                cwd=self.working_dir,
                capture_output=True,
                text=True,
                check=True
            )
            
            return result.stdout
            
        except subprocess.CalledProcessError as e:
            raise ValueError(f"Git show failed: {e.stderr}")
    
    def get_branch_diff(self, branch: str, base_branch: str = "main") -> str:
        """
        Get diff between branch and base branch.
        
        Args:
            branch: Branch to review
            base_branch: Base branch to compare against
            
        Returns:
            Git diff output between branches
            
        Raises:
            ValueError: If git command fails
        """
        try:
            result = subprocess.run(
                ["git", "diff", f"{base_branch}...{branch}"],
                cwd=self.working_dir,
                capture_output=True,
                text=True,
                check=True
            )
            
            if not result.stdout.strip():
                raise ValueError(f"No differences found between {base_branch} and {branch}")
            
            return result.stdout
            
        except subprocess.CalledProcessError as e:
            raise ValueError(f"Git branch diff failed: {e.stderr}")
    
    def parse_diff(self, diff_output: str) -> List[GitDiffFile]:
        """
        Parse git diff output into structured data.
        
        Args:
            diff_output: Raw git diff output
            
        Returns:
            List of GitDiffFile objects
        """
        files = []
        current_file = None
        
        lines = diff_output.split('\n')
        i = 0
        
        while i < len(lines):
            line = lines[i]
            
            # New file header
            if line.startswith('diff --git'):
                if current_file:
                    files.append(current_file)
                
                # Extract file paths
                match = re.match(r'diff --git a/(.*) b/(.*)', line)
                if match:
                    old_file, new_file = match.groups()
                    current_file = GitDiffFile(
                        file_path=new_file,
                        old_file=old_file,
                        new_file=new_file,
                        added_lines=[],
                        removed_lines=[],
                        context_lines=[]
                    )
            
            # Hunk header
            elif line.startswith('@@') and current_file:
                # Parse hunk info: @@ -old_start,old_count +new_start,new_count @@
                match = re.match(r'@@ -(\d+),?\d* \+(\d+),?\d* @@', line)
                if match:
                    old_line_num = int(match.group(1))
                    new_line_num = int(match.group(2))
                    
                    # Process hunk content
                    i += 1
                    while i < len(lines) and not lines[i].startswith('@@') and not lines[i].startswith('diff --git'):
                        hunk_line = lines[i]
                        
                        if hunk_line.startswith('+') and not hunk_line.startswith('+++'):
                            current_file.added_lines.append((new_line_num, hunk_line[1:]))
                            new_line_num += 1
                        elif hunk_line.startswith('-') and not hunk_line.startswith('---'):
                            current_file.removed_lines.append((old_line_num, hunk_line[1:]))
                            old_line_num += 1
                        elif hunk_line.startswith(' '):
                            current_file.context_lines.append((new_line_num, hunk_line[1:]))
                            old_line_num += 1
                            new_line_num += 1
                        
                        i += 1
                    continue
            
            i += 1
        
        # Add last file
        if current_file:
            files.append(current_file)
        
        return files
    
    def get_file_content_at_commit(self, file_path: str, commit_hash: str = "HEAD") -> str:
        """
        Get file content at specific commit.
        
        Args:
            file_path: Path to file
            commit_hash: Commit hash (default: HEAD)
            
        Returns:
            File content at the commit
            
        Raises:
            ValueError: If git command fails
        """
        try:
            result = subprocess.run(
                ["git", "show", f"{commit_hash}:{file_path}"],
                cwd=self.working_dir,
                capture_output=True,
                text=True,
                check=True
            )
            
            return result.stdout
            
        except subprocess.CalledProcessError as e:
            raise ValueError(f"Failed to get file content: {e.stderr}")
