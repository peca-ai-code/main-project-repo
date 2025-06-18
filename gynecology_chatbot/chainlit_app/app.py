"""
Chainlit application with Google OAuth authentication that syncs with Django/Firestore
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
    """Handle OAuth callback and sync with Django/Firestore"""
    print(f"✅ OAuth callback triggered for provider: {provider_id}")
    print(f"✅ User data received: {raw_user_data}")
    
    try:
        # Extract user information from OAuth data
        user_email = raw_user_data.get('email', '')
        user_name = raw_user_data.get('name', '')
        user_picture = raw_user_data.get('picture', '')
        given_name = raw_user_data.get('given_name', '')
        family_name = raw_user_data.get('family_name', '')
        user_id = raw_user_data.get('id', '')
        
        print(f"✅ Extracted user info: {user_email}, {user_name}")
        
        # Return enhanced user object with metadata
        enhanced_user = cl.User(
            identifier=user_email,
            metadata={
                "name": user_name,
                "email": user_email,
                "picture": user_picture,
                "provider": provider_id,
                "given_name": given_name,
                "family_name": family_name,
                "provider_id": user_id,
                "access_token": token,
                "needs_sync": True
            }
        )
        
        print(f"✅ OAuth callback completed successfully for: {user_email}")
        return enhanced_user
        
    except Exception as e:
        print(f"❌ Error in OAuth callback: {str(e)}")
        return default_user

async def sync_user_with_backend(user_metadata):
    """Sync OAuth user with Django backend and Firestore"""
    try:
        backend_url = os.getenv("DJANGO_API_URL", "http://localhost:9000/api")
        
        user_payload = {
            "provider": user_metadata.get("provider", "google"),
            "email": user_metadata.get("email", ""),
            "name": user_metadata.get("name", ""),
            "given_name": user_metadata.get("given_name", ""),
            "family_name": user_metadata.get("family_name", ""),
            "picture": user_metadata.get("picture", ""),
            "provider_id": user_metadata.get("provider_id", ""),
            "access_token": user_metadata.get("access_token", "")
        }
        
        print(f"🔄 Syncing user with backend: {user_payload['email']}")
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{backend_url}/oauth/sync/",
                json=user_payload,
                headers={"Content-Type": "application/json"}
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    print(f"✅ User synced with backend successfully: {result}")
                    
                    if result.get("tokens", {}).get("access"):
                        api_client.token = result["tokens"]["access"]
                        cl.user_session.set("jwt_token", result["tokens"]["access"])
                        cl.user_session.set("backend_user_id", result.get("user", {}).get("id"))
                        cl.user_session.set("backend_synced", True)
                    
                    return result
                else:
                    print(f"❌ Failed to sync user with backend: {response.status}")
                    error_text = await response.text()
                    print(f"❌ Error details: {error_text}")
                    return None
                    
    except Exception as e:
        print(f"❌ Error syncing user with backend: {str(e)}")
        return None

@cl.on_chat_start
# async def on_chat_start():
#     """Initialize chat with authentication and silent user sync"""
#     user = cl.user_session.get("user")
    
#     if not user:
#         await cl.Message(
#             content="Welcome to the Gynecology Assistant! Please sign in with Google to continue."
#         ).send()
#         return
    
#     user_email = user.metadata.get('email', 'unknown')
#     user_name = user.metadata.get('name', 'there')
#     print(f"🔍 Chat started for user: {user_email}")
    
#     # Show immediate welcome message
#     await cl.Message(
#         content=f"👋 Welcome, {user_name}!\nHow can I help you with your gynecological health concerns today?"
#     ).send()
    
#     # Check if user needs to be synced with backend (SILENT BACKGROUND SYNC)
#     if user.metadata.get("needs_sync", False) and not cl.user_session.get("backend_synced", False):
#         print(f"🔄 Silently syncing user with backend: {user_email}")
        
#         # Sync with Django backend/Firestore in background
#         try:
#             sync_result = await sync_user_with_backend(user.metadata)
            
#             if sync_result:
#                 cl.user_session.set("backend_synced", True)
#                 cl.user_session.set("user_id", sync_result.get("user", {}).get("id"))
#                 print(f"✅ Silent sync completed for: {user_email}")
#             else:
#                 print(f"⚠️ Silent sync failed for: {user_email}")
#         except Exception as e:
#             print(f"❌ Silent sync error: {str(e)}")
    
#     # Check backend connection silently
#     backend_status = await api_client.check_health()
#     if not backend_status:
#         print("⚠️ Backend connection issue detected")
#         # Don't show error message unless it persists
#         return
    
#     # Create conversation silently
#     try:
#         conversation = await api_client.create_conversation("New Conversation")
#         if conversation:
#             cl.user_session.set("conversation_id", conversation.get("id"))
#             print(f"✅ Created conversation: {conversation.get('id')}")
#         else:
#             cl.user_session.set("conversation_id", str(uuid.uuid4()))
#             print("⚠️ Using fallback conversation ID")
#     except Exception as e:
#         print(f"❌ Error creating conversation: {str(e)}")
#         cl.user_session.set("conversation_id", str(uuid.uuid4()))

async def on_chat_start():
    """Initialize chat with authentication and user sync"""
    user = cl.user_session.get("user")
    
    if not user:
        await cl.Message(
            content="Welcome to the Gynecology Assistant! Please sign in with Google to continue."
        ).send()
        return
    
    user_email = user.metadata.get('email', 'unknown')
    print(f"🔍 Chat started for user: {user_email}")
    
    # Check if user needs to be synced with backend
    if user.metadata.get("needs_sync", False) and not cl.user_session.get("backend_synced", False):
        print(f"🔄 Silently syncing user with backend: {user_email}")
        
        # Sync with Django backend/Firestore
        sync_result = await sync_user_with_backend(user.metadata)
        
        if sync_result:
            cl.user_session.set("backend_synced", True)
            cl.user_session.set("user_id", sync_result.get("user", {}).get("id"))
            
            user_name = user.metadata.get('name', 'there')
            if sync_result.get("created"):
                welcome_msg = f"Welcome, {user_name}! \nI'm your Gynecology Assistant. \nHow can I help you today?"
            else:
                welcome_msg = f"Welcome back, {user_name}!\nHow can I help you today?"
            
            await cl.Message(content=welcome_msg).send()
        else:
            await cl.Message(
                content="⚠️ There was an issue setting up your account, but you can still use the chat. However, your conversations may not be saved."
            ).send()
    else:
        # User already synced
        user_name = user.metadata.get('name', 'there')
        await cl.Message(
            content=f"👋 Welcome back, {user_name}! How can I help you with your gynecological health concerns today?"
        ).send()
    
    # Check backend connection
    backend_status = await api_client.check_health()
    if not backend_status:
        await cl.Message(
            content="⚠️ Could not connect to the backend server. Please refresh and try again."
        ).send()
        return
    
    # Create conversation
    try:
        conversation = await api_client.create_conversation("New Conversation")
        if conversation:
            cl.user_session.set("conversation_id", conversation.get("id"))
            print(f"✅ Created conversation: {conversation.get('id')}")
        else:
            cl.user_session.set("conversation_id", str(uuid.uuid4()))
            print("⚠️ Using fallback conversation ID")
    except Exception as e:
        print(f"❌ Error creating conversation: {str(e)}")
        cl.user_session.set("conversation_id", str(uuid.uuid4()))

def assess_severity(response_text):
    """Assess the severity of a health-related response on a scale of 1-10"""
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
    """Process user messages and generate responses"""
    user = cl.user_session.get("user")
    
    if not user:
        await cl.Message(
            content="Please sign in with Google to use the chatbot."
        ).send()
        return
    
    user_email = user.metadata.get('email', 'unknown')
    conversation_id = cl.user_session.get("conversation_id")
    
    if not conversation_id:
        conversation_id = str(uuid.uuid4())
        cl.user_session.set("conversation_id", conversation_id)
    
    try:
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
        
        # Assess severity
        severity = assess_severity(best_response)
        print(f"Response severity assessment: {severity}/10 for user: {user_email}")
        
        # Add appointment booking button if severity >= 4
        if severity >= 4:
            actions = [
                cl.Action(
                    name="book_appointment", 
                    icon="calendar",
                    payload={"severity": severity, "user_email": user_email},
                    value="book_appointment", 
                    label="🩺 Book Doctor's Appointment",
                    description="Schedule a consultation with a gynecologist"
                )
            ]
            await cl.Message(content=best_response, actions=actions).send()
        else:
            await cl.Message(content=best_response).send()
        
    except Exception as e:
        error_message = f"I apologize, but I encountered an error: {str(e)}. For immediate health concerns, please contact a healthcare provider directly."
        await cl.Message(content=error_message).send()
        print(f"❌ Error processing message: {str(e)}")

@cl.on_chat_end
async def on_chat_end():
    """Clean up resources when chat ends"""
    await api_client.close()

@cl.action_callback("book_appointment")
async def on_book_appointment(action):
    """Handle booking appointment button click"""
    user = cl.user_session.get("user")
    user_email = user.metadata.get('email', 'unknown') if user else 'unknown'
    
    appointments_url = "http://localhost:9000/appointments/"
    
    await cl.Message(
        content=f"🩺 Opening appointment booking system...\n\nRedirecting you to schedule a consultation with one of our gynecologists."
    ).send()
    
    try:
        webbrowser.open(appointments_url)
        print(f"✅ Opened appointment booking for user: {user_email}")
    except Exception as e:
        print(f"❌ Could not open browser: {str(e)}")