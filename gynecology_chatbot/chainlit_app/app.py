"""
Chainlit application for gynecology chatbot that communicates with Django backend.
"""

import os
import chainlit as cl
from dotenv import load_dotenv
from services.api_client import DjangoAPIClient
import uuid
import google.generativeai as genai
import webbrowser


# Load environment variables
load_dotenv()

# Configure Gemini for severity assessment
if os.getenv("GEMINI_API_KEY"):
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

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

def assess_severity(response_text):
    """Assess the severity of a health-related response on a scale of 1-10."""
    try:
        if not os.getenv("GEMINI_API_KEY"):
            print("Gemini API key is missing!")
            return 3  # Default moderate severity if no API key
        
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"""
        As a medical assessment system, analyze the following gynecological health response and rate its severity on a scale of 1-10.
        1 = Completely routine, no concerns
        5 = Moderate concern that needs attention but isn't urgent
        10 = Very serious, requires immediate medical attention
        
        Provide ONLY a single number (1-10) as your response, no explanation.
        
        Response to assess:
        {response_text}
        """
        
        severity_response = model.generate_content(prompt)
        severity_text = severity_response.text.strip()
        
        # Extract just the number
        severity = 1
        for char in severity_text:
            if char.isdigit():
                severity = int(char)
                break
                
        # Ensure value is between 1-10
        return max(1, min(10, severity))
        
    except Exception as e:
        print(f"Error assessing severity: {str(e)}")
        return 3

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
        
        # Assess severity of the response (1-10 scale)
        severity = assess_severity(best_response)
        print(f"Response severity assessment: {severity}/10")
        
        # Update the thinking message with the selected response
        thinking_msg.content = best_response
        
        # Add appointment booking button only if severity is high (>= 6)
        if severity >= 4:
            thinking_msg.actions = [
                cl.Action(
                    name="book_appointment", 
                    value="book_appointment", 
                    label="🩺 Book a Doctor's Appointment",
                    description="Schedule a consultation with a gynecologist"
                )
            ]
        
        await thinking_msg.update()
        
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        thinking_msg.content = error_message
        await thinking_msg.update()
        print(f"Error processing message: {str(e)}")

@cl.on_chat_end
async def on_chat_end():
    """Clean up resources when chat ends."""
    # Close the API client session
    await api_client.close()

@cl.action_callback("book_appointment")
async def on_book_appointment(action):
    """Handle booking appointment button click."""
    appointments_url = "http://localhost:9000/appointments/"
    webbrowser.open(appointments_url)

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
