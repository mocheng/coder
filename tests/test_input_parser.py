#!/usr/bin/env python3
"""Unit tests for Input Parser"""

import unittest
import tempfile
import os
from src.input_parser import InputParser, ReviewInput, ReviewType


class TestInputParser(unittest.TestCase):
    
    def setUp(self):
        self.parser = InputParser()
        
        # Create temporary file for testing
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False)
        self.temp_file.write("def test(): pass")
        self.temp_file.close()
    
    def tearDown(self):
        os.unlink(self.temp_file.name)
    
    def test_parse_single_file(self):
        """Test parsing single file input"""
        result = self.parser.parse(self.temp_file.name)
        
        self.assertEqual(result.review_type, ReviewType.SINGLE_FILE)
        self.assertEqual(result.target, self.temp_file.name)
        self.assertEqual(result.git_options, {})
    
    def test_parse_git_diff(self):
        """Test parsing git diff option"""
        result = self.parser.parse(".", diff=True)
        
        self.assertEqual(result.review_type, ReviewType.GIT_DIFF)
        self.assertEqual(result.target, ".")
        self.assertTrue(result.git_options['diff'])
    
    def test_parse_git_commit(self):
        """Test parsing git commit option"""
        result = self.parser.parse(".", commit="abc123")
        
        self.assertEqual(result.review_type, ReviewType.GIT_COMMIT)
        self.assertEqual(result.target, "abc123")
        self.assertEqual(result.git_options['commit'], "abc123")
    
    def test_parse_git_branch(self):
        """Test parsing git branch option"""
        result = self.parser.parse(".", branch="feature/test")
        
        self.assertEqual(result.review_type, ReviewType.GIT_BRANCH)
        self.assertEqual(result.target, "feature/test")
        self.assertEqual(result.git_options['branch'], "feature/test")
    
    def test_parse_nonexistent_file(self):
        """Test parsing nonexistent file"""
        with self.assertRaises(ValueError) as context:
            self.parser.parse("nonexistent.py")
        
        self.assertIn("not found", str(context.exception))
    
    def test_parse_directory_as_file(self):
        """Test parsing directory instead of file"""
        with tempfile.TemporaryDirectory() as temp_dir:
            with self.assertRaises(ValueError) as context:
                self.parser.parse(temp_dir)
            
            self.assertIn("is not a file", str(context.exception))
    
    def test_git_options_priority(self):
        """Test that git options take priority over file validation"""
        # Should not validate file when git options are provided
        result = self.parser.parse("nonexistent", diff=True)
        self.assertEqual(result.review_type, ReviewType.GIT_DIFF)


if __name__ == '__main__':
    unittest.main()
