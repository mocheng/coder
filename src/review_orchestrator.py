"""Review Orchestrator - Manage single file code review"""

from dataclasses import dataclass
from .source_collector import SourceFile
from .llm_client import LLMClient


@dataclass
class ReviewResult:
    """Result of code review for a single file"""
    file_path: str
    review_content: str
    success: bool


class ReviewOrchestrator:
    """Orchestrate single file code review"""
    
    def __init__(self, llm_client: LLMClient):
        """
        Initialize review orchestrator.
        
        Args:
            llm_client: LLM client for performing reviews
        """
        self.llm_client = llm_client
    
    def review(self, source_file: SourceFile) -> ReviewResult:
        """
        Review single source file.
        
        Args:
            source_file: Source file to review
            
        Returns:
            Review result
        """
        try:
            review_content = self.llm_client.code_review(
                source_file.content, 
                source_file.path
            )
            
            return ReviewResult(
                file_path=source_file.path,
                review_content=review_content,
                success=True
            )
            
        except Exception as e:
            return ReviewResult(
                file_path=source_file.path,
                review_content=f"Review failed: {str(e)}",
                success=False
            )
