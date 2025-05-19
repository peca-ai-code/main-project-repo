"""
System prompts and instructions for AI models.
"""

def get_gynecology_system_prompt() -> str:
    """
    Returns the system prompt for gynecology assistant.
    
    This prompt is used across all AI models to ensure consistent tone and approach.
    """
    return (
        "You are a virtual gynecology assistant designed to provide support, information, "
        "and reassurance to users with gynecological concerns. In your responses:\n"
        "1. Provide clear, accurate, and concise information\n"
        "2. Emphasize when symptoms are likely benign\n"
        "3. Always recommend consulting a healthcare provider for proper diagnosis when appropriate\n"
        "4. Do not provide definitive diagnoses\n"
        "5. Be supportive, informative, and reassuring\n"
        "6. Prioritize accuracy and medical relevance over conversational aspects\n"
        "7. Use professional but accessible language"
    )

def format_conversation_history(messages):
    """
    Format conversation history for different AI models.
    
    Args:
        messages: List of message objects
        
    Returns:
        Dictionary with formatted history for each model type
    """
    openai_format = []
    gemini_format = []
    
    for msg in messages:
        if msg.get("role") == "user":
            # Format for OpenAI
            openai_format.append({
                "role": "user",
                "content": msg.get("content", "")
            })
            
            # Format for Gemini
            gemini_format.append({
                "role": "user",
                "parts": [{"text": msg.get("content", "")}]
            })
        
        elif msg.get("role") == "assistant":
            # Format for OpenAI
            openai_format.append({
                "role": "assistant",
                "content": msg.get("content", "")
            })
            
            # Format for Gemini
            gemini_format.append({
                "role": "model",
                "parts": [{"text": msg.get("content", "")}]
            })
    
    return {
        "openai": openai_format,
        "gemini": gemini_format
    }
