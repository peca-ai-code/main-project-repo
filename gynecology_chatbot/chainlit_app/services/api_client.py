"""
API client for communicating with the Django backend using Firestore.
"""

import aiohttp
import os
from typing import Dict, Any, Optional, List

class DjangoAPIClient:
    """Client for Django backend API interactions."""
    
    def __init__(self, base_url: str):
        """Initialize the API client with base URL."""
        self.base_url = base_url
        self.token = os.getenv("DJANGO_API_TOKEN", "")
        self.session = None
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create an aiohttp session."""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()
        return self.session
    
    async def _request(
        self, 
        method: str, 
        endpoint: str, 
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        authenticate: bool = True
    ) -> Optional[Dict[str, Any]]:
        """Make an HTTP request to the API."""
        url = f"{self.base_url}/{endpoint}"
        headers = {}
        
        if authenticate and self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        
        if data is not None:
            headers["Content-Type"] = "application/json"
        
        session = await self._get_session()
        
        try:
            async with session.request(
                method=method,
                url=url,
                json=data,
                params=params,
                headers=headers
            ) as response:
                if response.status in (200, 201):
                    return await response.json()
                elif response.status == 401:
                    print(f"Authentication failed: {response.status}")
                    # Try without authentication for Firestore endpoints
                    if not authenticate:
                        return None
                    return await self._request(method, endpoint, data, params, authenticate=False)
                else:
                    error_text = await response.text()
                    print(f"API Error: {response.status} - {error_text}")
                return None
        except Exception as e:
            print(f"API request error: {str(e)}")
            return None
    
    async def check_health(self) -> bool:
        """Check if the backend is available."""
        try:
            session = await self._get_session()
            # Try Firestore health endpoint first
            async with session.get(f"{self.base_url}/chatbot/health/") as response:
                if response.status == 200:
                    return True
            
            # Fallback to general health endpoint
            async with session.get(f"{self.base_url}/health/") as response:
                return response.status == 200
        except Exception as e:
            print(f"Health check error: {str(e)}")
            return False
    
    async def create_conversation(self, title: str) -> Optional[Dict[str, Any]]:
        """Create a new conversation."""
        data = {"title": title}
        result = await self._request("POST", "chatbot/conversations/", data=data)
        if not result:
            # Try without authentication
            result = await self._request("POST", "chatbot/conversations/", data=data, authenticate=False)
        return result
    
    async def send_message(
        self,
        conversation_id: str,
        message: str,
    ) -> Optional[Dict[str, Any]]:
        """Send a message to the conversation and get AI response."""
        data = {"message": message}
        
        result = await self._request(
            "POST", 
            f"chatbot/conversations/{conversation_id}/send_message/", 
            data=data
        )
        
        if not result:
            # Try without authentication
            result = await self._request(
                "POST", 
                f"chatbot/conversations/{conversation_id}/send_message/", 
                data=data,
                authenticate=False
            )
        
        return result
    
    async def close(self):
        """Close the aiohttp session."""
        if self.session and not self.session.closed:
            await self.session.close()
