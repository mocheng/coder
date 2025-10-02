#!/usr/bin/env python3
"""Unit tests for main CLI functionality"""

import unittest
import tempfile
import os
from unittest.mock import patch
from typer.testing import CliRunner
from src.main import app
from src.llm_client import LLMClient
from src.code_context import parse_line_references, extract_line_feedback


class TestCodeReview(unittest.TestCase):
    
    def setUp(self):
        self.runner = CliRunner()
        
    def test_cr_file_not_found(self):
        """Test cr command with non-existent file"""
        result = self.runner.invoke(app, ["cr", "nonexistent.py"])
        self.assertEqual(result.exit_code, 1)
        self.assertIn("not found", result.stdout)
    
    def test_cr_with_valid_file(self):
        """Test cr command with valid Python file"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write("def test(): pass")
            temp_file = f.name
        
        try:
            with patch('src.llm_client.LLMClient.code_review') as mock_review:
                mock_review.return_value = "Line 1: Missing docstring"
                result = self.runner.invoke(app, ["cr", temp_file])
                self.assertEqual(result.exit_code, 0)
                self.assertIn("File Information", result.stdout)
                self.assertIn("CODE REVIEW RESULTS", result.stdout)
        finally:
            os.unlink(temp_file)
    
    def test_cr_with_directory_fails(self):
        """Test cr command with directory (should fail)"""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = self.runner.invoke(app, ["cr", temp_dir])
            self.assertEqual(result.exit_code, 1)
            self.assertIn("is not a file", result.stdout)
    
    def test_parse_line_references(self):
        """Test parsing line references from review text"""
        review_text = "Line 5: Issue here. Line 10: Another issue. No line reference here."
        line_refs = parse_line_references(review_text)
        self.assertEqual(line_refs, [5, 10])
    
    def test_extract_line_feedback(self):
        """Test extracting feedback for specific line"""
        review_text = "Line 5: Missing docstring. Line 10: Use is None instead of == None."
        feedback = extract_line_feedback(review_text, 5)
        self.assertIn("Missing docstring", feedback)
    
    @patch.dict(os.environ, {'GOOGLE_API_KEY': 'test_key'})
    def test_llm_client_initialization(self):
        """Test LLM client can be initialized"""
        client = LLMClient()
        self.assertIsNotNone(client.model)


if __name__ == '__main__':
    unittest.main()
