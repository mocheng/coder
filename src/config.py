"""Configuration management for CLI Coding Agent"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Configuration settings for the application"""
    
    def __init__(self):
        """Initialize configuration with defaults"""
        self.llm_model = os.getenv("CODER_LLM_MODEL", "gemini/gemini-2.5-flash")
        self.api_timeout = int(os.getenv("CODER_API_TIMEOUT", "30"))
        self.max_tokens = int(os.getenv("CODER_MAX_TOKENS", "2000"))
        self.temperature = float(os.getenv("CODER_TEMPERATURE", "0.1"))
    
    def get_llm_model(self) -> str:
        """Get configured LLM model"""
        return self.llm_model
    
    def set_llm_model(self, model: str) -> None:
        """Set LLM model"""
        self.llm_model = model
    
    def get_api_timeout(self) -> int:
        """Get API timeout in seconds"""
        return self.api_timeout
    
    def get_max_tokens(self) -> int:
        """Get max tokens for LLM responses"""
        return self.max_tokens
    
    def get_temperature(self) -> float:
        """Get temperature for LLM responses"""
        return self.temperature


# Global configuration instance
config = Config()
