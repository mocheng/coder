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
        system_prompt = """You are an expert code reviewer. Focus ONLY on issues that need to be fixed or improved. Do not mention what is good or working well.

Analyze the code for:
1. Bugs and potential errors
2. Security vulnerabilities  
3. Performance issues
4. Code quality problems
5. Best practice violations
6. Language issues in comments (typos, grammar, unclear wording)

IMPORTANT: 
- Only report problems that need fixing
- Always include line numbers in "Line X:" format for specific issues
- Be concise and actionable
- Skip positive feedback entirely
- Check spelling and grammar in comments and variable names
- Do not require documentation or docstrings"""

        user_message = f"""Review this code and report ONLY the issues that need to be fixed:

File: {file_path}

```
{file_content}
```

List only problems that require code changes. Include line numbers using "Line X:" format. Focus on bugs, security, performance, and language quality - not documentation."""

        return self.send_message(user_message, system_prompt)
    
    def set_model(self, model: str) -> None:
        """Change the LLM model"""
        self.model = model
    
    def get_model(self) -> str:
        """Get current model name"""
        return self.model


# Default client instance
default_client = LLMClient()
