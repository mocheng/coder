"""LLM Client - Integration with litellm for multiple LLM providers"""

import os
from typing import Optional, Dict, Any
from dotenv import load_dotenv

# Load environment variables from .env file BEFORE importing litellm
load_dotenv()

import litellm
from litellm import completion
from .config import config


class LLMClient:
    """Client for LLM communication using litellm"""
    
    def __init__(self, model: Optional[str] = None):
        """
        Initialize LLM client with specified model.
        
        Args:
            model: Model name in litellm format (default: from config)
        """
        self.model = model or config.get_llm_model()
        self.default_params = {
            "temperature": config.get_temperature(),
            "max_tokens": config.get_max_tokens(),
        }
        
        # Verify API key is available
        if not os.getenv("GOOGLE_API_KEY"):
            print("Warning: GOOGLE_API_KEY not found in environment variables")
    
    def send_message(self, message: str, system_prompt: Optional[str] = None) -> str:
        """
        Send message to LLM and get response.
        
        Args:
            message: User message to send
            system_prompt: Optional system prompt for context
            
        Returns:
            LLM response text
            
        Raises:
            Exception: If API call fails
        """
        try:
            messages = []
            
            # Add system prompt if provided
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            
            # Add user message
            messages.append({"role": "user", "content": message})
            
            # Make API call
            response = completion(
                model=self.model,
                messages=messages,
                **self.default_params
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            raise Exception(f"LLM API error: {str(e)}")
    
    def code_review(self, file_content: str, file_path: str) -> str:
        """
        Perform code review using LLM.
        
        Args:
            file_content: Content of the file to review
            file_path: Path to the file being reviewed
            
        Returns:
            Code review response from LLM
        """
        system_prompt = """You are an expert code reviewer. Analyze the provided code and give constructive feedback focusing on:

1. Code quality and best practices
2. Potential bugs or issues
3. Performance considerations
4. Security concerns
5. Readability and maintainability

Provide specific, actionable suggestions for improvement."""

        user_message = f"""Please review this code file:

File: {file_path}

```
{file_content}
```

Provide a detailed code review with specific suggestions for improvement."""

        return self.send_message(user_message, system_prompt)
    
    def set_model(self, model: str) -> None:
        """Change the LLM model"""
        self.model = model
    
    def get_model(self) -> str:
        """Get current model name"""
        return self.model


# Default client instance
default_client = LLMClient()
