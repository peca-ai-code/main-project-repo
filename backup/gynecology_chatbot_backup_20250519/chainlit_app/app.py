"""
Chainlit application for the Virtual Gynecology Chatbot.
This frontend communicates with a Django backend API.
"""

import os
import chainlit as cl
from dotenv import load_dotenv
from services.api_client import DjangoAPIClient
from components.comparison import create_comparison_element, create_css_element
import asyncio
import uuid

# Load environment variables
load_dotenv()

# Initialize API client
api_client = DjangoAPIClient(
    base_url=os.getenv("DJANGO_API_URL", "http://localhost:8000/api")
)

# Store conversation data
conversation_data = {}

@cl.on_chat_start
async def on_chat_start():
    """Initialize the chat session."""
    # Generate a unique session identifier
    session_id = str(uuid.uuid4())
    
    # Store the session ID
    cl.user_session.set("session_id", session_id)
    
    # Check if backend is available
    backend_status = await api_client.check_health()
    
    if not backend_status:
        await cl.Message(
            content="⚠️ Warning: Could not connect to the backend server. Some features may be limited.",
            author="System"
        ).send()
    
    # Try to authenticate if token exists
    token = os.getenv("DJANGO_API_TOKEN", "")
    if token:
        auth_status = await api_client.authenticate(token)
        if auth_status:
            cl.user_session.set("authenticated", True)
            
            # Get user settings
            user_settings = await api_client.get_user_settings()
            if user_settings:
                cl.user_session.set("settings", user_settings)
        else:
            cl.user_session.set("authenticated", False)
    
    # Create a new conversation in the backend
    conversation = await api_client.create_conversation("New Conversation")
    if conversation:
        conversation_id = conversation.get("id")
        cl.user_session.set("conversation_id", conversation_id)
        conversation_data[session_id] = {
            "id": conversation_id,
            "title": "New Conversation",
            "messages": []
        }
    
    # Add CSS for model comparison
    css_element = await create_css_element()
    await cl.Message(content="", elements=[css_element]).send()
    
    # Welcome message
    await cl.Message(
        content="Welcome to the Virtual Gynecology Assistant. How can I help you today?",
        author="Assistant"
    ).send()
    
    # Set chat settings
    settings = cl.user_session.get("settings", {
        "preferred_model": "openai",
        "show_all_models": True
    })
    
    settings_elements = [
        cl.Switch(
            id="show_all_models",
            label="Show All Model Responses",
            value=settings.get("show_all_models", True)
        ),
        cl.Select(
            id="primary_model",
            label="Primary Response Model",
            values=[
                {"value": "openai", "label": "ChatGPT"},
                {"value": "gemini", "label": "Gemini"},
                {"value": "grok", "label": "Grok"}
            ],
            value=settings.get("preferred_model", "openai")
        )
    ]
    
    await cl.ChatSettings(elements=settings_elements).send()

@cl.on_message
async def on_message(message: cl.Message):
    """Process user messages and generate responses."""
    # Get session data
    session_id = cl.user_session.get("session_id")
    conversation_id = cl.user_session.get("conversation_id")
    
    if not conversation_id:
        # Create a new conversation if none exists
        conversation = await api_client.create_conversation("New Conversation")
        if conversation:
            conversation_id = conversation.get("id")
            cl.user_session.set("conversation_id", conversation_id)
    
    # Get settings
    settings = cl.user_session.get("settings", {
        "preferred_model": "openai",
        "show_all_models": True
    })
    
    # Extract settings values
    show_all_models = settings.get("show_all_models", True)
    primary_model = settings.get("preferred_model", "openai")
    
    # Send thinking message
    thinking_msg = cl.Message(content="Generating responses...", author="Assistant")
    await thinking_msg.send()
    
    try:
        # Send message to API and get AI responses
        response_data = await api_client.send_message(
            conversation_id=conversation_id,
            message=message.content,
            primary_model=primary_model,
            show_all_models=show_all_models
        )
        
        if not response_data:
            # Handle API error
            thinking_msg.content = "Sorry, I encountered an error communicating with the backend. Please try again."
            await thinking_msg.update()
            return
        
        # Get the primary response and all model responses
        all_responses = response_data.get("model_responses", {})
        primary_response = all_responses.get(primary_model, "No response generated.")
        
        # Update the thinking message with the primary response
        thinking_msg.content = primary_response
        await thinking_msg.update()
        
        # Add to conversation data
        if session_id in conversation_data:
            conversation_data[session_id]["messages"].extend([
                {"role": "user", "content": message.content},
                {"role": "assistant", "content": primary_response, "model": primary_model}
            ])
        
        # If show_all_models is enabled, display all model responses
        if show_all_models and len(all_responses) > 1:
            # Create model comparison element
            comparison = await create_comparison_element(
                user_message=message.content,
                responses=all_responses,
                chat_id=session_id
            )
            
            # Send comparison as element attached to a message
            await cl.Message(content="Model Comparison:", elements=[comparison]).send()
            
            # Show individual model responses (except the primary one)
            for model_name, response_text in all_responses.items():
                if model_name != primary_model:
                    # Map internal model names to display names
                    display_names = {
                        "openai": "ChatGPT",
                        "gemini": "Gemini",
                        "grok": "Grok"
                    }
                    display_name = display_names.get(model_name, model_name)
                    
                    await cl.Message(
                        content=f"**{display_name} Response:**\n\n{response_text}",
                        author=f"AI - {display_name}"
                    ).send()
    
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        thinking_msg.content = error_message
        await thinking_msg.update()
        cl.logger.error(f"Error processing message: {str(e)}")

@cl.on_settings_update
async def on_settings_update(settings):
    """Handle updates to chat settings."""
    # Map settings to the format used by the backend
    backend_settings = {
        "preferred_model": settings.get("primary_model", "openai"),
        "show_all_models": settings.get("show_all_models", True)
    }
    
    # Store settings in session
    cl.user_session.set("settings", backend_settings)
    
    # Update user settings in backend if authenticated
    if cl.user_session.get("authenticated", False):
        await api_client.update_user_settings(backend_settings)
    
    # Send confirmation message
    model_display_names = {
        "openai": "ChatGPT",
        "gemini": "Gemini",
        "grok": "Grok"
    }
    
    model_name = model_display_names.get(backend_settings["preferred_model"], backend_settings["preferred_model"])
    show_all = backend_settings["show_all_models"]
    
    message = f"Settings updated: Primary model set to {model_name}."
    if show_all:
        message += " All model responses will be shown."
    else:
        message += " Only primary model responses will be shown."
    
    await cl.Message(content=message, author="System").send()

@cl.action_callback("clear_conversation")
async def clear_conversation(action):
    """Clear the current conversation."""
    conversation_id = cl.user_session.get("conversation_id")
    session_id = cl.user_session.get("session_id")
    
    if conversation_id:
        # Clear conversation in backend
        success = await api_client.clear_conversation(conversation_id)
        
        if success:
            # Clear local conversation data
            if session_id in conversation_data:
                conversation_data[session_id]["messages"] = []
            
            await cl.Message(
                content="Conversation cleared successfully.",
                author="System"
            ).send()
        else:
            await cl.Message(
                content="Failed to clear conversation. Please try again.",
                author="System"
            ).send()

if __name__ == "__main__":
    # Chainlit takes care of running the app
    pass
