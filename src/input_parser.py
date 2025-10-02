"""Input Parser - Parse and validate single file input for code review"""

from pathlib import Path
from dataclasses import dataclass


@dataclass
class ReviewInput:
    """Parsed review input with metadata"""
    file_path: str


class InputParser:
    """Parse and validate single file input"""
    
    def parse(self, file_path: str) -> ReviewInput:
        """
        Parse single file input.
        
        Args:
            file_path: Path to file for review
            
        Returns:
            ReviewInput with parsed information
            
        Raises:
            ValueError: If input is invalid
        """
        path = Path(file_path)
        
        if not path.exists():
            raise ValueError(f"File '{file_path}' not found")
        
        if not path.is_file():
            raise ValueError(f"'{file_path}' is not a file")
        
        return ReviewInput(file_path=file_path)
