#!/usr/bin/env python3
"""Unit tests for Git Operations"""

import unittest
from unittest.mock import patch, MagicMock
import subprocess
from src.git_operations import GitOperations, GitDiffFile


class TestGitOperations(unittest.TestCase):
    
    def setUp(self):
        self.git_ops = GitOperations()
    
    @patch('subprocess.run')
    def test_get_staged_diff_success(self, mock_run):
        """Test successful staged diff retrieval"""
        mock_run.return_value = MagicMock(
            stdout="diff --git a/test.py b/test.py\n+added line",
            stderr="",
            returncode=0
        )
        
        result = self.git_ops.get_staged_diff()
        
        self.assertIn("diff --git", result)
        mock_run.assert_called_once_with(
            ["git", "diff", "--cached"],
            cwd=".",
            capture_output=True,
            text=True,
            check=True
        )
    
    @patch('subprocess.run')
    def test_get_staged_diff_no_changes(self, mock_run):
        """Test staged diff with no changes"""
        mock_run.return_value = MagicMock(
            stdout="",
            stderr="",
            returncode=0
        )
        
        with self.assertRaises(ValueError) as context:
            self.git_ops.get_staged_diff()
        
        self.assertIn("No staged changes", str(context.exception))
    
    @patch('subprocess.run')
    def test_get_staged_diff_git_error(self, mock_run):
        """Test staged diff with git error"""
        mock_run.side_effect = subprocess.CalledProcessError(1, "git", stderr="not a git repository")
        
        with self.assertRaises(ValueError) as context:
            self.git_ops.get_staged_diff()
        
        self.assertIn("Git diff failed", str(context.exception))
    
    @patch('subprocess.run')
    def test_get_commit_diff_success(self, mock_run):
        """Test successful commit diff retrieval"""
        mock_run.return_value = MagicMock(
            stdout="diff --git a/test.py b/test.py\n+added line",
            stderr="",
            returncode=0
        )
        
        result = self.git_ops.get_commit_diff("abc123")
        
        self.assertIn("diff --git", result)
        mock_run.assert_called_once_with(
            ["git", "show", "--format=", "abc123"],
            cwd=".",
            capture_output=True,
            text=True,
            check=True
        )
    
    @patch('subprocess.run')
    def test_get_branch_diff_success(self, mock_run):
        """Test successful branch diff retrieval"""
        mock_run.return_value = MagicMock(
            stdout="diff --git a/test.py b/test.py\n+added line",
            stderr="",
            returncode=0
        )
        
        result = self.git_ops.get_branch_diff("feature/test")
        
        self.assertIn("diff --git", result)
        mock_run.assert_called_once_with(
            ["git", "diff", "main...feature/test"],
            cwd=".",
            capture_output=True,
            text=True,
            check=True
        )
    
    def test_parse_diff_simple(self):
        """Test parsing simple git diff"""
        diff_output = """diff --git a/test.py b/test.py
index 1234567..abcdefg 100644
--- a/test.py
+++ b/test.py
@@ -1,3 +1,4 @@
 def hello():
+    print("new line")
     print("world")
-    old_line()"""
        
        result = self.git_ops.parse_diff(diff_output)
        
        self.assertEqual(len(result), 1)
        diff_file = result[0]
        self.assertEqual(diff_file.file_path, "test.py")
        self.assertEqual(len(diff_file.added_lines), 1)
        self.assertEqual(len(diff_file.removed_lines), 1)
        self.assertEqual(diff_file.added_lines[0][1], '    print("new line")')
        self.assertEqual(diff_file.removed_lines[0][1], '    old_line()')
    
    def test_parse_diff_multiple_files(self):
        """Test parsing diff with multiple files"""
        diff_output = """diff --git a/file1.py b/file1.py
index 1234567..abcdefg 100644
--- a/file1.py
+++ b/file1.py
@@ -1,2 +1,3 @@
 line1
+added1
 line2
diff --git a/file2.py b/file2.py
index 2345678..bcdefgh 100644
--- a/file2.py
+++ b/file2.py
@@ -1,2 +1,3 @@
 line1
+added2
 line2"""
        
        result = self.git_ops.parse_diff(diff_output)
        
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].file_path, "file1.py")
        self.assertEqual(result[1].file_path, "file2.py")
        self.assertEqual(result[0].added_lines[0][1], "added1")
        self.assertEqual(result[1].added_lines[0][1], "added2")
    
    def test_parse_diff_empty(self):
        """Test parsing empty diff"""
        result = self.git_ops.parse_diff("")
        self.assertEqual(len(result), 0)
    
    @patch('subprocess.run')
    def test_get_file_content_at_commit(self, mock_run):
        """Test getting file content at specific commit"""
        mock_run.return_value = MagicMock(
            stdout="file content",
            stderr="",
            returncode=0
        )
        
        result = self.git_ops.get_file_content_at_commit("test.py", "abc123")
        
        self.assertEqual(result, "file content")
        mock_run.assert_called_once_with(
            ["git", "show", "abc123:test.py"],
            cwd=".",
            capture_output=True,
            text=True,
            check=True
        )


if __name__ == '__main__':
    unittest.main()
