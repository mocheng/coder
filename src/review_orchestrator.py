"""Review Orchestrator - Manage code review workflow"""

from dataclasses import dataclass
from typing import List
from .source_collector import SourceFile
from .llm_client import LLMClient


@dataclass
class ReviewResult:
    """Result of code review for a single file"""
    file_path: str
    review_content: str
    success: bool
    is_diff: bool = False
    diff_info: dict = None


class ReviewOrchestrator:
    """Orchestrate code review workflow"""
    
    def __init__(self, llm_client: LLMClient):
        """
        Initialize review orchestrator.
        
        Args:
            llm_client: LLM client for performing reviews
        """
        self.llm_client = llm_client
    
    def review(self, source_files: List[SourceFile]) -> List[ReviewResult]:
        """
        Review source files.
        
        Args:
            source_files: List of source files to review
            
        Returns:
            List of review results
        """
        results = []
        
        for source_file in source_files:
            try:
                # Use different prompts for diff vs regular files
                if source_file.is_diff:
                    review_content = self._review_diff_file(source_file)
                else:
                    review_content = self.llm_client.code_review(
                        source_file.content, 
                        source_file.path
                    )
                
                result = ReviewResult(
                    file_path=source_file.path,
                    review_content=review_content,
                    success=True,
                    is_diff=source_file.is_diff,
                    diff_info=source_file.diff_info
                )
                
                results.append(result)
                
            except Exception as e:
                error_result = ReviewResult(
                    file_path=source_file.path,
                    review_content=f"Review failed: {str(e)}",
                    success=False,
                    is_diff=source_file.is_diff,
                    diff_info=source_file.diff_info
                )
                results.append(error_result)
        
        return results
    
    def _review_diff_file(self, source_file: SourceFile) -> str:
        """
        Review git diff file with specialized prompt.
        
        Args:
            source_file: Source file with diff content
            
        Returns:
            Review content from LLM
        """
        system_prompt = """You are an expert code reviewer analyzing git changes. Focus ONLY on the changes being made (added/removed lines).

Analyze the changes for:
1. Bugs introduced by the changes
2. Security issues in new code
3. Performance problems in additions
4. Code quality issues in changes
5. Best practice violations in new code

IMPORTANT:
- Focus only on the ADDED LINES (marked with +)
- Consider REMOVED LINES (marked with -) for context
- Only report problems in the changes, not existing code
- Include line numbers for specific issues
- Be concise and actionable"""

        diff_type = source_file.diff_info.get("type", "changes") if source_file.diff_info else "changes"
        
        user_message = f"""Review these git {diff_type} and report ONLY issues in the changes:

File: {source_file.path}

{source_file.content}

Focus on problems in the added lines. Include line numbers for specific issues."""

        return self.llm_client.send_message(user_message, system_prompt)
