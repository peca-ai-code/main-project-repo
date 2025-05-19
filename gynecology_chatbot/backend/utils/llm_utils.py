import asyncio
from typing import Dict, List, Any, Tuple
import google.generativeai as genai
from django.conf import settings
from apps.chatbot.api import get_openai_response, get_gemini_response, get_grok_response

# Configure Gemini for evaluation
if settings.GEMINI_API_KEY:
    genai.configure(api_key=settings.GEMINI_API_KEY)

async def generate_all_responses(user_message: str, chat_history: List[Any]) -> Dict[str, str]:
    """Generate responses from all AI models concurrently."""
    # Create tasks for all models
    tasks = [
        get_openai_response(user_message, chat_history),
        get_gemini_response(user_message, chat_history),
        get_grok_response(user_message, chat_history)
    ]
    
    # Run tasks concurrently
    responses = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Filter out exceptions and map responses to model names
    response_dict = {}
    models = ["openai", "gemini", "grok"]
    
    for i, response in enumerate(responses):
        if not isinstance(response, Exception):
            response_dict[models[i]] = response
    
    return response_dict

async def evaluate_responses(responses: Dict[str, str], user_message: str) -> Tuple[str, str, str]:
    """
    Use Gemini to evaluate and select the best response from multiple LLMs.
    
    Args:
        responses: Dictionary mapping model names to their responses
        user_message: The original user message
        
    Returns:
        Tuple containing (best_model_name, best_response, explanation)
    """
    # If only one response is available, return it without evaluation
    if len(responses) == 1:
        model_name = list(responses.keys())[0]
        return model_name, responses[model_name], "Only one model response was available."
    
    # If no responses available, return error
    if not responses:
        return "system", "I'm sorry, all AI models are currently unavailable. Please try again later.", ""
    
    try:
        # Prepare the prompt for Gemini evaluation
        evaluation_prompt = f"""
        You are an expert evaluator of AI assistant responses. Your job is to select the best response to a user's query.
        
        User query: "{user_message}"
        
        Available responses:
        """
        
        # Add each model's response to the prompt
        for model_name, response in responses.items():
            evaluation_prompt += f"\n{model_name.upper()} RESPONSE:\n{response}\n"
        
        evaluation_prompt += """
        Please evaluate each response based on the following criteria:
        1. Accuracy and relevance to the query
        2. Helpfulness and comprehensiveness
        3. Clarity and readability
        
        Select the BEST response and provide a brief explanation of why it was selected.
        
        FORMAT YOUR ANSWER EXACTLY LIKE THIS:
        BEST_MODEL: [model name]
        EXPLANATION: [brief explanation]
        """
        
        # Call Gemini for evaluation
        model = genai.GenerativeModel(
            model_name=settings.GEMINI_MODEL,
            generation_config={"temperature": 0.2, "max_output_tokens": 500}
        )
        
        result = model.generate_content(evaluation_prompt)
        evaluation_result = result.text
        
        # Parse the evaluation result
        best_model = None
        explanation = ""
        
        for line in evaluation_result.strip().split('\n'):
            if line.startswith("BEST_MODEL:"):
                best_model = line.replace("BEST_MODEL:", "").strip().lower()
            elif line.startswith("EXPLANATION:"):
                explanation = line.replace("EXPLANATION:", "").strip()
        
        # Validate the selected model
        if best_model and best_model in responses:
            return best_model, responses[best_model], explanation
        
        # Default to the first model if parsing failed
        default_model = list(responses.keys())[0]
        return default_model, responses[default_model], "Evaluation could not determine the best model."
        
    except Exception as e:
        # Fallback to the first model in case of evaluation error
        default_model = list(responses.keys())[0]
        return default_model, responses[default_model], f"Evaluation error: {str(e)}"

def generate_ai_responses(user_message: str, chat_history: List[Any]) -> Dict[str, Any]:
    """
    Generate responses from multiple models and select the best one.
    
    Args:
        user_message: The user's message
        chat_history: Previous conversation history
        
    Returns:
        Dictionary containing the best response and metadata
    """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        # Get responses from all models
        all_responses = loop.run_until_complete(
            generate_all_responses(user_message, chat_history)
        )
        
        # Evaluate and select the best response
        best_model, best_response, explanation = loop.run_until_complete(
            evaluate_responses(all_responses, user_message)
        )
        
        return {
            "all_responses": all_responses,
            "best_model": best_model,
            "best_response": best_response,
            "explanation": explanation
        }
    finally:
        loop.close()
