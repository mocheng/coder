"""Input Parser - Parse and validate input for code review"""

from pathlib import Path
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class ReviewType(Enum):
    """Types of code review inputs"""
    SINGLE_FILE = "single_file"
    GIT_DIFF = "git_diff"
    GIT_COMMIT = "git_commit"
    GIT_BRANCH = "git_branch"


@dataclass
class ReviewInput:
    """Parsed review input with metadata"""
    review_type: ReviewType
    target: str
    git_options: dict


class InputParser:
    """Parse and validate input for code review"""
    
    def parse(self, file_path: str, diff: bool = False, commit: Optional[str] = None, 
              branch: Optional[str] = None) -> ReviewInput:
        """
        Parse input for code review.
        
        Args:
            file_path: Path to file for review (or working directory for git operations)
            diff: Review staged git changes
            commit: Review specific commit hash
            branch: Review branch changes
            
        Returns:
            ReviewInput with parsed information
            
        Raises:
            ValueError: If input is invalid
        """
        git_options = {}
        
        # Check for git options first
        if diff:
            return ReviewInput(
                review_type=ReviewType.GIT_DIFF,
                target=file_path,
                git_options={"diff": True}
            )
        
        if commit:
            return ReviewInput(
                review_type=ReviewType.GIT_COMMIT,
                target=commit,
                git_options={"commit": commit}
            )
            
        if branch:
            return ReviewInput(
                review_type=ReviewType.GIT_BRANCH,
                target=branch,
                git_options={"branch": branch}
            )
        
        # Default to single file
        path = Path(file_path)
        
        if not path.exists():
            raise ValueError(f"File '{file_path}' not found")
        
        if not path.is_file():
            raise ValueError(f"'{file_path}' is not a file")
        
        return ReviewInput(
            review_type=ReviewType.SINGLE_FILE,
            target=file_path,
            git_options={}
        )
