"""
Google Gemini service adapter for direct API calls if needed.
"""

import google.generativeai as genai
from typing import List, Dict, Any, Optional
import os
import asyncio

class GeminiService:
    """Service for Google Gemini API interactions."""
    
    def __init__(self):
        """Initialize the Gemini service."""
        self.api_key = os.getenv("GEMINI_API_KEY", "")
        self.model = os.getenv("GEMINI_MODEL", "gemini-1.5-pro")
        
        # Configure Gemini client
        if self.api_key:
            genai.configure(api_key=self.api_key)
    
    async def generate_response(
        self,
        prompt: str,
        system_message: str,
        chat_history: Optional[List[Dict[str, Any]]] = None,
        temperature: float = 0.1,
        max_tokens: int = 200
    ) -> str:
        """Generate a response using Google's Gemini."""
        if not self.api_key:
            return "Error: Gemini API key not configured."
        
        try:
            # Format history for Gemini
            formatted_history = []
            
            # Add system instruction
            formatted_history.append({
                "role": "user",
                "parts": [{"text": system_message}]
            })
            
            # Add chat history if provided
            if chat_history:
                for msg in chat_history:
                    role = "user" if msg["role"] == "user" else "model"
                    formatted_history.append({
                        "role": role,
                        "parts": [{"text": msg["content"]}]
                    })
            
            # Add current user prompt
            formatted_history.append({
                "role": "user",
                "parts": [{"text": prompt}]
            })
            
            # Use a synchronous call in an executor to make it async-compatible
            loop = asyncio.get_event_loop()
            
            def generate_response():
                # Initialize the model
                generation_config = {
                    "temperature": temperature,
                    "max_output_tokens": max_tokens,
                }
                
                model = genai.GenerativeModel(
                    model_name=self.model,
                    generation_config=generation_config
                )
                
                # Generate the response
                response = model.generate_content(formatted_history)
                return response.text
            
            # Run synchronous code in executor
            response_text = await loop.run_in_executor(None, generate_response)
            return response_text
            
        except Exception as e:
            return f"Error: {str(e)}"
