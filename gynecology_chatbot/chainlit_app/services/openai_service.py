"""
OpenAI service adapter for direct API calls if needed.
"""

import openai
from typing import List, Dict, Any, Optional
import os
from openai.error import OpenAIError

class OpenAIService:
    """Service for OpenAI API interactions."""
    
    def __init__(self):
        """Initialize the OpenAI service."""
        self.api_key = os.getenv("OPENAI_API_KEY", "")
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o")
        
        # Configure OpenAI client
        if self.api_key:
            openai.api_key = self.api_key
    
    async def generate_response(
        self,
        prompt: str,
        system_message: str,
        chat_history: Optional[List[Dict[str, Any]]] = None,
        temperature: float = 0.7,
        max_tokens: int = 800
    ) -> str:
        """Generate a response using OpenAI's ChatGPT."""
        if not self.api_key:
            return "Error: OpenAI API key not configured."
        
        try:
            # Format messages
            messages = [{"role": "system", "content": system_message}]
            
            # Add chat history
            if chat_history:
                messages.extend(chat_history)
            
            # Add user prompt
            messages.append({"role": "user", "content": prompt})
            
            # Call OpenAI API
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            return response.choices[0].message.content
            
        except OpenAIError as e:
            return f"Error: {str(e)}"
        except Exception as e:
            return f"Unexpected error: {str(e)}"
