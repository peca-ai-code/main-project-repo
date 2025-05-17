import asyncio
from typing import Dict, List, Any
from apps.chatbot.api import get_openai_response, get_gemini_response, get_grok_response

async def generate_all_responses(user_message: str, chat_history: List[Any]) -> Dict[str, str]:
    """Generate responses from all AI models concurrently."""
    # Create tasks for all models
    tasks = [
        get_openai_response(user_message, chat_history),
        get_gemini_response(user_message, chat_history),
        get_grok_response(user_message, chat_history)
    ]
    
    # Run tasks concurrently
    responses = await asyncio.gather(*tasks)
    
    # Map responses to model names
    response_dict = {
        "openai": responses[0],
        "gemini": responses[1],
        "grok": responses[2]
    }
    
    return response_dict

def generate_ai_responses(user_message: str, chat_history: List[Any], primary_model: str = 'openai') -> Dict[str, str]:
    """Generate responses from AI models (sync wrapper for async function)."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        response_dict = loop.run_until_complete(
            generate_all_responses(user_message, chat_history)
        )
        return response_dict
    finally:
        loop.close()
