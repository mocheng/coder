#!/usr/bin/env python3
"""Unit tests for LLM client functionality"""

import unittest
import os
from unittest.mock import patch, MagicMock
from src.llm_client import LLMClient


class TestLLMClient(unittest.TestCase):
    
    @patch.dict(os.environ, {'GOOGLE_API_KEY': 'test_key'})
    def setUp(self):
        """Set up test client"""
        self.client = LLMClient()
    
    def test_client_initialization(self):
        """Test LLM client initialization"""
        self.assertIsNotNone(self.client.model)
        self.assertEqual(self.client.get_model(), "gemini/gemini-2.5-flash")
    
    @patch('src.llm_client.completion')
    def test_send_message_success(self, mock_completion):
        """Test successful message sending"""
        # Mock LLM response
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "Test response"
        mock_completion.return_value = mock_response
        
        result = self.client.send_message("Test message")
        
        self.assertEqual(result, "Test response")
        mock_completion.assert_called_once()
    
    @patch('src.llm_client.completion')
    def test_send_message_with_system_prompt(self, mock_completion):
        """Test message sending with system prompt"""
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "System response"
        mock_completion.return_value = mock_response
        
        result = self.client.send_message("User message", "System prompt")
        
        self.assertEqual(result, "System response")
        # Verify system prompt was included in messages
        call_args = mock_completion.call_args[1]
        messages = call_args['messages']
        self.assertEqual(len(messages), 2)
        self.assertEqual(messages[0]['role'], 'system')
        self.assertEqual(messages[1]['role'], 'user')
    
    @patch('src.llm_client.completion')
    def test_code_review(self, mock_completion):
        """Test code review functionality"""
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "Line 1: Missing docstring"
        mock_completion.return_value = mock_response
        
        result = self.client.code_review("def test(): pass", "test.py")
        
        self.assertIn("Line 1:", result)
        mock_completion.assert_called_once()
    
    @patch('src.llm_client.completion')
    def test_send_message_api_error(self, mock_completion):
        """Test API error handling"""
        mock_completion.side_effect = Exception("API Error")
        
        with self.assertRaises(Exception) as context:
            self.client.send_message("Test message")
        
        self.assertIn("LLM API error", str(context.exception))
    
    def test_set_model(self):
        """Test model setting"""
        new_model = "gemini/gemini-1.5-pro"
        self.client.set_model(new_model)
        self.assertEqual(self.client.get_model(), new_model)


if __name__ == '__main__':
    unittest.main()
