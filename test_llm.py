#!/usr/bin/env python3
"""Simple test script to verify LLM integration"""

from src.llm_client import LLMClient

def test_llm():
    """Test LLM with simple math question"""
    try:
        client = LLMClient()
        print(f"Testing LLM model: {client.get_model()}")
        
        response = client.send_message("What is 1+1? Please explain briefly.")
        
        print("✓ LLM integration successful!")
        print(f"Question: What is 1+1?")
        print(f"Response: {response}")
        
    except Exception as e:
        print(f"✗ LLM test failed: {e}")
        print("Make sure GOOGLE_API_KEY is set in .env file")

if __name__ == "__main__":
    test_llm()
