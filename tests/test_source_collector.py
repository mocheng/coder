#!/usr/bin/env python3
"""Unit tests for Source Collector"""

import unittest
import tempfile
import os
from unittest.mock import patch, MagicMock
from src.source_collector import SourceCollector, SourceFile
from src.input_parser import ReviewInput, ReviewType
from src.git_operations import GitDiffFile


class TestSourceCollector(unittest.TestCase):
    
    def setUp(self):
        self.collector = SourceCollector()
        
        # Create temporary test file
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False)
        self.temp_file.write("def hello():\n    print('Hello')")
        self.temp_file.close()
    
    def tearDown(self):
        os.unlink(self.temp_file.name)
    
    def test_collect_single_file(self):
        """Test collecting single file"""
        review_input = ReviewInput(
            review_type=ReviewType.SINGLE_FILE,
            target=self.temp_file.name,
            git_options={}
        )
        
        result = self.collector.collect(review_input)
        
        self.assertEqual(len(result), 1)
        source_file = result[0]
        self.assertEqual(source_file.path, self.temp_file.name)
        self.assertIn("def hello", source_file.content)
        self.assertEqual(source_file.lines, 2)
        self.assertFalse(source_file.is_diff)
    
    @patch('src.source_collector.GitOperations')
    def test_collect_git_diff(self, mock_git_ops_class):
        """Test collecting git staged changes"""
        # Create a fresh collector with mocked GitOperations
        collector = SourceCollector()
        
        # Mock the instance methods
        mock_git_ops = mock_git_ops_class.return_value
        collector.git_ops = mock_git_ops
        
        mock_git_ops.get_staged_diff.return_value = "diff output"
        mock_git_ops.parse_diff.return_value = [
            GitDiffFile(
                file_path="test.py",
                old_file="test.py",
                new_file="test.py",
                added_lines=[(1, "new line")],
                removed_lines=[(2, "old line")],
                context_lines=[(3, "context")]
            )
        ]
        
        review_input = ReviewInput(
            review_type=ReviewType.GIT_DIFF,
            target=".",
            git_options={"diff": True}
        )
        
        result = collector.collect(review_input)
        
        self.assertEqual(len(result), 1)
        source_file = result[0]
        self.assertEqual(source_file.path, "test.py")
        self.assertTrue(source_file.is_diff)
        self.assertEqual(source_file.diff_info["type"], "staged_changes")
        self.assertEqual(source_file.diff_info["added_lines"], 1)
        self.assertEqual(source_file.diff_info["removed_lines"], 1)
    
    @patch('src.source_collector.GitOperations')
    def test_collect_git_commit(self, mock_git_ops_class):
        """Test collecting git commit changes"""
        collector = SourceCollector()
        
        mock_git_ops = mock_git_ops_class.return_value
        collector.git_ops = mock_git_ops
        
        mock_git_ops.get_commit_diff.return_value = "commit diff output"
        mock_git_ops.parse_diff.return_value = [
            GitDiffFile(
                file_path="test.py",
                old_file="test.py", 
                new_file="test.py",
                added_lines=[(1, "new line")],
                removed_lines=[],
                context_lines=[]
            )
        ]
        
        review_input = ReviewInput(
            review_type=ReviewType.GIT_COMMIT,
            target="abc123",
            git_options={"commit": "abc123"}
        )
        
        result = collector.collect(review_input)
        
        self.assertEqual(len(result), 1)
        source_file = result[0]
        self.assertEqual(source_file.path, "test.py")
        self.assertTrue(source_file.is_diff)
        self.assertEqual(source_file.diff_info["type"], "commit")
        self.assertEqual(source_file.diff_info["commit_hash"], "abc123")
    
    @patch('src.source_collector.GitOperations')
    def test_collect_git_branch(self, mock_git_ops_class):
        """Test collecting git branch changes"""
        collector = SourceCollector()
        
        mock_git_ops = mock_git_ops_class.return_value
        collector.git_ops = mock_git_ops
        
        mock_git_ops.get_branch_diff.return_value = "branch diff output"
        mock_git_ops.parse_diff.return_value = [
            GitDiffFile(
                file_path="test.py",
                old_file="test.py",
                new_file="test.py", 
                added_lines=[(1, "new line")],
                removed_lines=[],
                context_lines=[]
            )
        ]
        
        review_input = ReviewInput(
            review_type=ReviewType.GIT_BRANCH,
            target="feature/test",
            git_options={"branch": "feature/test"}
        )
        
        result = collector.collect(review_input)
        
        self.assertEqual(len(result), 1)
        source_file = result[0]
        self.assertEqual(source_file.path, "test.py")
        self.assertTrue(source_file.is_diff)
        self.assertEqual(source_file.diff_info["type"], "branch")
        self.assertEqual(source_file.diff_info["branch"], "feature/test")
    
    def test_collect_nonexistent_file(self):
        """Test collecting nonexistent file"""
        review_input = ReviewInput(
            review_type=ReviewType.SINGLE_FILE,
            target="nonexistent.py",
            git_options={}
        )
        
        with self.assertRaises(ValueError) as context:
            self.collector.collect(review_input)
        
        self.assertIn("Failed to read file", str(context.exception))
    
    @patch('src.source_collector.GitOperations')
    def test_collect_git_error(self, mock_git_ops_class):
        """Test git collection with error"""
        mock_git_ops = MagicMock()
        mock_git_ops_class.return_value = mock_git_ops
        mock_git_ops.get_staged_diff.side_effect = ValueError("Git error")
        
        review_input = ReviewInput(
            review_type=ReviewType.GIT_DIFF,
            target=".",
            git_options={"diff": True}
        )
        
        with self.assertRaises(ValueError) as context:
            self.collector.collect(review_input)
        
        self.assertIn("Failed to collect git diff", str(context.exception))
    
    def test_create_diff_content(self):
        """Test creating diff content from GitDiffFile"""
        diff_file = GitDiffFile(
            file_path="test.py",
            old_file="test.py",
            new_file="test.py",
            added_lines=[(1, "new line"), (2, "another line")],
            removed_lines=[(3, "old line")],
            context_lines=[(4, "context line")]
        )
        
        content = self.collector._create_diff_content(diff_file)
        
        self.assertIn("File: test.py", content)
        self.assertIn("=== ADDED LINES ===", content)
        self.assertIn("+ 1: new line", content)
        self.assertIn("=== REMOVED LINES ===", content)
        self.assertIn("- 3: old line", content)
        self.assertIn("=== CONTEXT ===", content)
        self.assertIn("  4: context line", content)


if __name__ == '__main__':
    unittest.main()
