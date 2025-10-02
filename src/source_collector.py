"""Source Collector - Collect single file content"""

from dataclasses import dataclass
from .input_parser import ReviewInput
from .tool_ops import read_file_content


@dataclass
class SourceFile:
    """Represents a source file with content and metadata"""
    path: str
    content: str
    size: int
    lines: int


class SourceCollector:
    """Collect source code from single file"""
    
    def collect(self, review_input: ReviewInput) -> SourceFile:
        """
        Collect single file content.
        
        Args:
            review_input: Parsed review input
            
        Returns:
            SourceFile with content and metadata
            
        Raises:
            ValueError: If collection fails
        """
        try:
            content = read_file_content(review_input.file_path)
            
            return SourceFile(
                path=review_input.file_path,
                content=content,
                size=len(content),
                lines=len(content.splitlines())
            )
            
        except Exception as e:
            raise ValueError(f"Failed to read file '{review_input.file_path}': {e}")
