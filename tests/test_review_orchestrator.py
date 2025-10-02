#!/usr/bin/env python3
"""Unit tests for Review Orchestrator"""

import unittest
from unittest.mock import Mock
from src.review_orchestrator import ReviewOrchestrator, ReviewResult
from src.source_collector import SourceFile
from src.llm_client import LLMClient


class TestReviewOrchestrator(unittest.TestCase):
    
    def setUp(self):
        self.mock_llm_client = Mock(spec=LLMClient)
        self.orchestrator = ReviewOrchestrator(self.mock_llm_client)
    
    def test_review_single_file(self):
        """Test reviewing single source file"""
        # Mock LLM response
        self.mock_llm_client.code_review.return_value = "Line 1: Missing docstring"
        
        source_files = [
            SourceFile("test.py", "def test(): pass", 15, 1, is_diff=False)
        ]
        
        results = self.orchestrator.review(source_files)
        
        self.assertEqual(len(results), 1)
        result = results[0]
        self.assertEqual(result.file_path, "test.py")
        self.assertIn("Missing docstring", result.review_content)
        self.assertTrue(result.success)
        self.assertFalse(result.is_diff)
    
    def test_review_multiple_files(self):
        """Test reviewing multiple source files"""
        # Mock LLM responses
        self.mock_llm_client.code_review.side_effect = [
            "Line 1: Missing docstring",
            "No issues found"
        ]
        
        source_files = [
            SourceFile("test1.py", "def test(): pass", 15, 1, is_diff=False),
            SourceFile("test2.py", "def good_function():\n    '''Good docstring'''\n    pass", 50, 3, is_diff=False)
        ]
        
        results = self.orchestrator.review(source_files)
        
        self.assertEqual(len(results), 2)
        self.assertIn("Missing docstring", results[0].review_content)
        self.assertIn("No issues", results[1].review_content)
        self.assertTrue(results[0].success)
        self.assertTrue(results[1].success)
    
    def test_review_diff_file(self):
        """Test reviewing git diff file"""
        # Mock LLM response for diff
        self.mock_llm_client.send_message.return_value = "Line 1: Issue in added code"
        
        source_files = [
            SourceFile(
                "test.py", 
                "=== ADDED LINES ===\n+ 1: def new_function(): pass", 
                30, 2, 
                is_diff=True,
                diff_info={"type": "staged_changes", "added_lines": 1, "removed_lines": 0}
            )
        ]
        
        results = self.orchestrator.review(source_files)
        
        self.assertEqual(len(results), 1)
        result = results[0]
        self.assertEqual(result.file_path, "test.py")
        self.assertIn("Issue in added code", result.review_content)
        self.assertTrue(result.success)
        self.assertTrue(result.is_diff)
        self.assertEqual(result.diff_info["type"], "staged_changes")
    
    def test_review_with_llm_error(self):
        """Test handling LLM errors during review"""
        # Mock LLM to raise exception
        self.mock_llm_client.code_review.side_effect = Exception("API Error")
        
        source_files = [
            SourceFile("test.py", "def test(): pass", 15, 1, is_diff=False)
        ]
        
        results = self.orchestrator.review(source_files)
        
        self.assertEqual(len(results), 1)
        result = results[0]
        self.assertIn("Review failed", result.review_content)
        self.assertFalse(result.success)
    
    def test_review_diff_file_with_specialized_prompt(self):
        """Test that diff files use specialized prompt"""
        self.mock_llm_client.send_message.return_value = "Diff review result"
        
        source_files = [
            SourceFile(
                "test.py",
                "diff content", 
                10, 1,
                is_diff=True,
                diff_info={"type": "commit", "commit_hash": "abc123"}
            )
        ]
        
        results = self.orchestrator.review(source_files)
        
        # Verify send_message was called (for diff) instead of code_review
        self.mock_llm_client.send_message.assert_called_once()
        self.mock_llm_client.code_review.assert_not_called()
        
        # Check the system prompt contains git-specific instructions
        call_args = self.mock_llm_client.send_message.call_args
        system_prompt = call_args[0][1]  # Second argument is system_prompt
        self.assertIn("git changes", system_prompt.lower())
        self.assertIn("added lines", system_prompt.lower())
    
    def test_review_mixed_files(self):
        """Test reviewing mix of regular and diff files"""
        self.mock_llm_client.code_review.return_value = "Regular file review"
        self.mock_llm_client.send_message.return_value = "Diff file review"
        
        source_files = [
            SourceFile("regular.py", "def test(): pass", 15, 1, is_diff=False),
            SourceFile("diff.py", "diff content", 10, 1, is_diff=True, diff_info={"type": "diff"})
        ]
        
        results = self.orchestrator.review(source_files)
        
        self.assertEqual(len(results), 2)
        self.assertFalse(results[0].is_diff)
        self.assertTrue(results[1].is_diff)
        
        # Verify both methods were called
        self.mock_llm_client.code_review.assert_called_once()
        self.mock_llm_client.send_message.assert_called_once()


if __name__ == '__main__':
    unittest.main()
