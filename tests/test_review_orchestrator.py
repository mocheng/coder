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
    
    def test_review_success(self):
        """Test successful review"""
        # Mock LLM response
        self.mock_llm_client.code_review.return_value = "Line 1: Missing docstring"
        
        source_file = SourceFile("test.py", "def test(): pass", 15, 1)
        
        result = self.orchestrator.review(source_file)
        
        self.assertIsInstance(result, ReviewResult)
        self.assertEqual(result.file_path, "test.py")
        self.assertIn("Missing docstring", result.review_content)
        self.assertTrue(result.success)
    
    def test_review_llm_error(self):
        """Test review with LLM error"""
        # Mock LLM to raise exception
        self.mock_llm_client.code_review.side_effect = Exception("API Error")
        
        source_file = SourceFile("test.py", "def test(): pass", 15, 1)
        
        result = self.orchestrator.review(source_file)
        
        self.assertEqual(result.file_path, "test.py")
        self.assertIn("Review failed", result.review_content)
        self.assertFalse(result.success)


if __name__ == '__main__':
    unittest.main()
