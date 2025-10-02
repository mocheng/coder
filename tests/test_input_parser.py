#!/usr/bin/env python3
"""Unit tests for Input Parser"""

import unittest
import tempfile
import os
from src.input_parser import InputParser, ReviewInput


class TestInputParser(unittest.TestCase):
    
    def setUp(self):
        self.parser = InputParser()
        
        # Create temporary file for testing
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False)
        self.temp_file.write("def test(): pass")
        self.temp_file.close()
    
    def tearDown(self):
        os.unlink(self.temp_file.name)
    
    def test_parse_valid_file(self):
        """Test parsing valid file input"""
        result = self.parser.parse(self.temp_file.name)
        
        self.assertIsInstance(result, ReviewInput)
        self.assertEqual(result.file_path, self.temp_file.name)
    
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


if __name__ == '__main__':
    unittest.main()
