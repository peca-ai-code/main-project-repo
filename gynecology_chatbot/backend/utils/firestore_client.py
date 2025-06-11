import os
from google.cloud import firestore
from django.conf import settings
from typing import Dict, List, Any, Optional
import uuid
from datetime import datetime

class FirestoreClient:
    _instance = None
    _client = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FirestoreClient, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._client:
            self._initialize_client()
    
    def _initialize_client(self):
        """Initialize Firestore client"""
        try:
            # Set credentials path
            if hasattr(settings, 'GOOGLE_APPLICATION_CREDENTIALS'):
                os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = settings.GOOGLE_APPLICATION_CREDENTIALS
            
            # Initialize client
            self._client = firestore.Client(project=settings.GOOGLE_CLOUD_PROJECT)
            
            print("Firestore client initialized successfully")
            
        except Exception as e:
            print(f"Error initializing Firestore client: {e}")
            raise
    
    @property
    def client(self):
        """Get Firestore client"""
        return self._client
    
    def create_document(self, collection: str, data: Dict[str, Any], doc_id: str = None) -> str:
        """Create a document in Firestore"""
        try:
            if doc_id:
                doc_ref = self._client.collection(collection).document(doc_id)
            else:
                doc_ref = self._client.collection(collection).document()
            
            # Add timestamps
            data['created_at'] = firestore.SERVER_TIMESTAMP
            data['updated_at'] = firestore.SERVER_TIMESTAMP
            
            doc_ref.set(data)
            return doc_ref.id
        except Exception as e:
            print(f"Error creating document: {e}")
            raise
    
    def get_document(self, collection: str, doc_id: str) -> Optional[Dict[str, Any]]:
        """Get a document from Firestore"""
        try:
            doc_ref = self._client.collection(collection).document(doc_id)
            doc = doc_ref.get()
            
            if doc.exists:
                data = doc.to_dict()
                data['id'] = doc.id
                return data
            return None
        except Exception as e:
            print(f"Error getting document: {e}")
            return None
    
    def update_document(self, collection: str, doc_id: str, data: Dict[str, Any]) -> bool:
        """Update a document in Firestore"""
        try:
            doc_ref = self._client.collection(collection).document(doc_id)
            data['updated_at'] = firestore.SERVER_TIMESTAMP
            doc_ref.update(data)
            return True
        except Exception as e:
            print(f"Error updating document: {e}")
            return False
    
    def delete_document(self, collection: str, doc_id: str) -> bool:
        """Delete a document from Firestore"""
        try:
            doc_ref = self._client.collection(collection).document(doc_id)
            doc_ref.delete()
            return True
        except Exception as e:
            print(f"Error deleting document: {e}")
            return False
    
    def query_collection(self, collection: str, filters: List = None, 
                        order_by: str = None, limit: int = None) -> List[Dict[str, Any]]:
        """Query a collection with optional filters"""
        try:
            query = self._client.collection(collection)
            
            if filters:
                for filter_item in filters:
                    if len(filter_item) == 3:
                        field, operator, value = filter_item
                        query = query.where(field, operator, value)
            
            if order_by:
                query = query.order_by(order_by)
            
            if limit:
                query = query.limit(limit)
            
            docs = query.stream()
            results = []
            
            for doc in docs:
                data = doc.to_dict()
                data['id'] = doc.id
                results.append(data)
            
            return results
        except Exception as e:
            print(f"Error querying collection: {e}")
            return []

# Global instance
firestore_client = FirestoreClient()
