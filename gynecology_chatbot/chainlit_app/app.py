"""
Chainlit application with Google OAuth authentication
"""

import os
import chainlit as cl
from dotenv import load_dotenv
from services.api_client import DjangoAPIClient
import uuid
import google.generativeai as genai
import webbrowser
import asyncio
import aiohttp

# Load environment variables
load_dotenv()

# Configure Gemini
if os.getenv("GEMINI_API_KEY"):
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize API client
api_client = DjangoAPIClient(
    base_url=os.getenv("DJANGO_API_URL", "http://localhost:9000/api")
)

@cl.oauth_callback
def oauth_callback(
    provider_id: str,
    token: str,
    raw_user_data: dict,
    default_user: cl.User,
) -> cl.User:
    """Handle OAuth callback and sync with Django"""
    return default_user

@cl.on_chat_start
async def on_chat_start():
    """Initialize chat with authentication"""
    user = cl.user_session.get("user")
    
    if not user:
        # User needs to authenticate
        await cl.Message(
            content="Welcome to the Gynecology Assistant! Please sign in with Google to continue.",
        ).send()
        return
    
    # Store user session
    cl.user_session.set("user_id", user.identifier)
    
    # Check backend connection
    backend_status = await api_client.check_health()
    if not backend_status:
        await cl.Message(
            content="⚠️ Warning: Could not connect to the backend server. Please try again later."
        ).send()
        return
    
    # Create conversation
    try:
        conversation = await api_client.create_conversation("New Conversation")
        if conversation:
            cl.user_session.set("conversation_id", conversation.get("id"))
            
            await cl.Message(
                content="Welcome to the Gynecology Assistant powered by Firestore! I'm here to provide information and support regarding gynecological health concerns. How can I help you today?"
            ).send()
        else:
            cl.user_session.set("conversation_id", str(uuid.uuid4()))
            await cl.Message(
                content="⚠️ Authentication issue detected. Starting in demo mode."
            ).send()
    except Exception as e:
        await cl.Message(
            content=f"⚠️ Error starting chat: {str(e)}. Starting in demo mode."
        ).send()
        cl.user_session.set("conversation_id", str(uuid.uuid4()))

# Your existing assess_severity and on_message functions remain the same...
def assess_severity(response_text):
    """Assess the severity of a health-related response on a scale of 1-10 using new Gemini API."""
    try:
        if not os.getenv("GEMINI_API_KEY"):
            print("Gemini API key is missing!")
            return 3
        
        model = genai.GenerativeModel(
            model_name='gemini-1.5-flash',
            generation_config=genai.GenerationConfig(
                temperature=0.1,
                max_output_tokens=10,
                top_k=1,
                top_p=0.1,
            )
        )
        
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
        
        severity = 1
        for char in severity_text:
            if char.isdigit():
                severity = int(char)
                break
                
        return max(1, min(10, severity))
        
    except Exception as e:
        print(f"Error assessing severity: {str(e)}")
        return 3

@cl.on_message
async def on_message(message: cl.Message):
    """Process user messages and generate responses."""
    user = cl.user_session.get("user")
    
    if not user:
        await cl.Message(
            content="Please sign in with Google to use the chatbot."
        ).send()
        return
    
    conversation_id = cl.user_session.get("conversation_id")
    
    if not conversation_id:
        conversation_id = str(uuid.uuid4())
        cl.user_session.set("conversation_id", conversation_id)
    
    try:
        # Send message to API
        response_data = await api_client.send_message(
            conversation_id=conversation_id,
            message=message.content
        )
        
        if not response_data:
            await cl.Message(
                content="I apologize, but I'm experiencing technical difficulties. Please try again in a moment."
            ).send()
            return
        
        best_response = response_data.get("content", "No response generated.")
        model_name = response_data.get("model_name", "AI")
        
        # Assess severity
        severity = assess_severity(best_response)
        print(f"Response severity assessment: {severity}/10")
        
        # Add appointment booking button if severity >= 4
        if severity >= 4:
            actions = [
                cl.Action(
                    name="book_appointment", 
                    icon="mouse-pointer-click",
                    payload={"value": "example_value"},
                    value="book_appointment", 
                    label="🩺 Book a Doctor's Appointment",
                    description="Schedule a consultation with a gynecologist"
                )
            ]
            await cl.Message(content=best_response, actions=actions).send()
        else:
            await cl.Message(content=best_response).send()
        
    except Exception as e:
        error_message = f"I apologize, but I encountered an error: {str(e)}. For immediate health concerns, please contact a healthcare provider directly."
        await cl.Message(content=error_message).send()
        print(f"Error processing message: {str(e)}")

@cl.on_chat_end
async def on_chat_end():
    """Clean up resources when chat ends."""
    await api_client.close()

@cl.action_callback("book_appointment")
async def on_book_appointment(action):
    """Handle booking appointment button click."""
    appointments_url = "http://localhost:9000/appointments/"
    webbrowser.open(appointments_url)