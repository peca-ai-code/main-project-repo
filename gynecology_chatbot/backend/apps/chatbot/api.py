import os
import asyncio
import openai
import google.generativeai as genai
from django.conf import settings

# Configure API clients
openai.api_key = settings.OPENAI_API_KEY
if settings.GEMINI_API_KEY:
    genai.configure(api_key=settings.GEMINI_API_KEY)

async def get_openai_response(user_message, chat_history=None):
    """Get response from OpenAI's GPT model."""
    if not settings.OPENAI_API_KEY:
        return "Error: OpenAI API key not configured."
    
    try:
        # Create messages array with system prompt
        messages = [{"role": "system", "content": settings.GYNECOLOGY_SYSTEM_PROMPT}]
        
        # Add chat history if provided
        if chat_history:
            for msg in chat_history:
                role = "user" if msg.message_type == "user" else "assistant"
                messages.append({"role": role, "content": msg.content})
        
        # Add current user message
        messages.append({"role": "user", "content": user_message})
        
        # Call OpenAI API
        response = await openai.ChatCompletion.acreate(
            model=settings.OPENAI_MODEL,
            messages=messages,
            max_tokens=500,
            temperature=0.7
        )
        
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating response from ChatGPT: {str(e)}"

async def get_gemini_response(user_message, chat_history=None):
    """Get response from Google's Gemini model."""
    if not settings.GEMINI_API_KEY:
        return "Error: Gemini API key not configured."
    
    try:
        # Format history for Gemini
        formatted_history = []
        
        # Add system instruction
        formatted_history.append({
            "role": "user",
            "parts": [{"text": settings.GYNECOLOGY_SYSTEM_PROMPT}]
        })
        
        # Add chat history if provided
        if chat_history:
            for msg in chat_history:
                role = "user" if msg.message_type == "user" else "model"
                formatted_history.append({
                    "role": role,
                    "parts": [{"text": msg.content}]
                })
        
        # Add current user message
        formatted_history.append({
            "role": "user",
            "parts": [{"text": user_message}]
        })
        
        # Make synchronous call in executor to be async-compatible
        loop = asyncio.get_event_loop()
        
        # Define the function to call in the executor
        def generate_response():
            try:
                # Initialize Gemini model
                generation_config = {
                    "temperature": 0.7,
                    "max_output_tokens": 500,
                }
                
                model = genai.GenerativeModel(
                    model_name=settings.GEMINI_MODEL,
                    generation_config=generation_config
                )
                
                # Generate response
                response = model.generate_content(formatted_history)
                return response.text
            except Exception as e:
                return f"Error in Gemini generation: {str(e)}"
        
        # Run in executor
        response_text = await loop.run_in_executor(None, generate_response)
        return response_text
        
    except Exception as e:
        return f"Error generating response from Gemini: {str(e)}"

async def get_grok_response(user_message, chat_history=None):
    """Simulate a response from Grok (as no public API exists yet)."""
    await asyncio.sleep(1)  # Simulate API delay
    
    return (
        f"[SIMULATED GROK RESPONSE] As Grok doesn't have a public API yet, "
        f"this is a simulated response to demonstrate functionality.\n\n"
        f"In response to your query about '{user_message[:30]}...', "
        f"I would provide gynecological information while recommending "
        f"consultation with a healthcare provider for proper diagnosis."
    )
