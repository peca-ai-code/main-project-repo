"""
Streamlined Chainlit application that communicates with Django backend.
All LLM orchestration happens on the backend.
"""

import os
import chainlit as cl
from dotenv import load_dotenv
from services.api_client import DjangoAPIClient
import uuid

# Load environment variables
load_dotenv()

# Initialize API client
api_client = DjangoAPIClient(
    base_url=os.getenv("DJANGO_API_URL", "http://localhost:9000/api")
)

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
            content="⚠️ Warning: Could not connect to the backend server. Please try again later.",
            author="System"
        ).send()
        return
    
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
            await cl.Message(
                content="⚠️ Authentication failed. Please check your API token.",
                author="System"
            ).send()
            return
    
    # Create a new conversation in the backend
    conversation = await api_client.create_conversation("New Conversation")
    if conversation:
        conversation_id = conversation.get("id")
        cl.user_session.set("conversation_id", conversation_id)
    
    # Welcome message
    await cl.Message(
        content="Welcome to the AI Assistant. How can I help you today?",
        author="Assistant"
    ).send()

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
        else:
            await cl.Message(
                content="Error: Could not create conversation. Please refresh and try again.",
                author="System"
            ).send()
            return
    
    # Send thinking message
    thinking_msg = cl.Message(content="Thinking...", author="Assistant")
    await thinking_msg.send()
    
    try:
        # Send message to API and get AI response
        response_data = await api_client.send_message(
            conversation_id=conversation_id,
            message=message.content
        )
        
        if not response_data:
            # Handle API error
            thinking_msg.content = "Sorry, I encountered an error communicating with the backend. Please try again."
            await thinking_msg.update()
            return
        
        # Get the best response
        best_response = response_data.get("content", "No response generated.")
        model_name = response_data.get("model_name", "AI")
        
        # Update the thinking message with the selected response
        thinking_msg.content = best_response
        
        # Optionally add metadata about which model generated the response
        thinking_msg.metadata = {"model": model_name}
        
        await thinking_msg.update()
        
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        thinking_msg.content = error_message
        await thinking_msg.update()
        cl.logger.error(f"Error processing message: {str(e)}")

@cl.action_callback("clear_conversation")
async def clear_conversation(action):
    """Clear the current conversation."""
    conversation_id = cl.user_session.get("conversation_id")
    
    if conversation_id:
        # Clear conversation in backend
        success = await api_client.clear_conversation(conversation_id)
        
        if success:
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
