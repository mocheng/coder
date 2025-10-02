#!/usr/bin/env python3
"""Unit tests for Source Collector"""

import unittest
import tempfile
import os
from src.source_collector import SourceCollector, SourceFile
from src.input_parser import ReviewInput


class TestSourceCollector(unittest.TestCase):
    
    def setUp(self):
        self.collector = SourceCollector()
        
        # Create temporary test file
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False)
        self.temp_file.write("def hello():\n    print('Hello')")
        self.temp_file.close()
    
    def tearDown(self):
        os.unlink(self.temp_file.name)
    
    def test_collect_valid_file(self):
        """Test collecting valid file"""
        review_input = ReviewInput(file_path=self.temp_file.name)
        
        result = self.collector.collect(review_input)
        
        self.assertIsInstance(result, SourceFile)
        self.assertEqual(result.path, self.temp_file.name)
        self.assertIn("def hello", result.content)
        self.assertEqual(result.lines, 2)
        self.assertEqual(result.size, len("def hello():\n    print('Hello')"))
    
    def test_collect_nonexistent_file(self):
        """Test collecting nonexistent file"""
        review_input = ReviewInput(file_path="nonexistent.py")
        
        with self.assertRaises(ValueError) as context:
            self.collector.collect(review_input)
        
        self.assertIn("Failed to read file", str(context.exception))


if __name__ == '__main__':
    unittest.main()
