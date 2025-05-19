"""
Chainlit application for gynecology chatbot that communicates with Django backend.
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

# Set authentication token if available
if os.getenv("DJANGO_API_TOKEN"):
    api_client.token = os.getenv("DJANGO_API_TOKEN")

@cl.on_chat_start
async def on_chat_start():
    """Initialize the chat session."""
    # Generate a unique session identifier
    session_id = str(uuid.uuid4())
    cl.user_session.set("session_id", session_id)
    
    # Check if backend is available
    backend_status = await api_client.check_health()
    
    if not backend_status:
        await cl.Message(
            content="⚠️ Warning: Could not connect to the backend server. Please try again later.",
            author="System"
        ).send()
        return
    
    # Create a new conversation in the backend
    try:
        conversation = await api_client.create_conversation("New Conversation")
        if conversation:
            conversation_id = conversation.get("id")
            cl.user_session.set("conversation_id", conversation_id)
            
            # Welcome message
            await cl.Message(
                content="Welcome to the Gynecology Assistant. I'm here to provide information and support regarding gynecological health concerns. How can I help you today?",
                author="Assistant"
            ).send()
        else:
            await cl.Message(
                content="⚠️ Error: Could not create conversation. Please check your API token.",
                author="System"
            ).send()
    except Exception as e:
        await cl.Message(
            content=f"⚠️ Error starting chat: {str(e)}",
            author="System"
        ).send()

# @cl.on_message
# async def on_message(message: cl.Message):
#     """Process user messages and generate responses."""
#     # Get session data
#     conversation_id = cl.user_session.get("conversation_id")
    
#     if not conversation_id:
#         # Try to create a new conversation if none exists
#         try:
#             conversation = await api_client.create_conversation("New Conversation")
#             if conversation:
#                 conversation_id = conversation.get("id")
#                 cl.user_session.set("conversation_id", conversation_id)
#             else:
#                 await cl.Message(
#                     content="Error: Could not create conversation. Please refresh and try again.",
#                     author="System"
#                 ).send()
#                 return
#         except Exception as e:
#             await cl.Message(
#                 content=f"Error creating conversation: {str(e)}",
#                 author="System"
#             ).send()
#             return
    
#     # Send thinking message
#     thinking_msg = cl.Message(content="Thinking...", author="Assistant")
#     await thinking_msg.send()
    
#     try:
#         # Send message to API and get AI response
#         response_data = await api_client.send_message(
#             conversation_id=conversation_id,
#             message=message.content
#         )
        
#         if not response_data:
#             # Handle API error
#             thinking_msg.content = "Sorry, I encountered an error communicating with the backend. Please try again."
#             await thinking_msg.update()
#             return
        
#         # Get the best response
#         best_response = response_data.get("content", "No response generated.")
#         model_name = response_data.get("model_name", "AI")
        
#         # Update the thinking message with the selected response
#         thinking_msg.content = best_response
#         await thinking_msg.update()
        
#     except Exception as e:
#         error_message = f"An error occurred: {str(e)}"
#         thinking_msg.content = error_message
#         await thinking_msg.update()
#         print(f"Error processing message: {str(e)}")

@cl.on_message
async def on_message(message: cl.Message):
    """Process user messages and generate responses."""
    # Get session data
    conversation_id = cl.user_session.get("conversation_id")
    
    if not conversation_id:
        # Try to create a new conversation if none exists
        try:
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
        except Exception as e:
            await cl.Message(
                content=f"Error creating conversation: {str(e)}",
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
            await thinking_msg.update(content="Sorry, I encountered an error communicating with the backend. Please try again.")
            return
        
        # Get the best response
        best_response = response_data.get("content", "No response generated.")
        model_name = response_data.get("model_name", "AI")
        
        # Update the thinking message with the selected response
        await thinking_msg.update(content=best_response)
        
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        await thinking_msg.update(content=error_message)
        print(f"Error processing message: {str(e)}")

@cl.on_chat_end
async def on_chat_end():
    """Clean up resources when chat ends."""
    # Close the API client session
    await api_client.close()

# Add a clear conversation action button
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
