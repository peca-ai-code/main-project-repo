import os
from google.cloud import firestore
from firebase_admin import credentials, firestore as admin_firestore, initialize_app, get_app
from django.conf import settings
import json
from typing import Dict, List, Any, Optional
import uuid
from datetime import datetime

class FirestoreClient:
    _instance = None
    _client = None
    _admin_client = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FirestoreClient, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._client:
            self._initialize_clients()
    
    def _initialize_clients(self):
        """Initialize both Firestore clients"""
        try:
            # Initialize standard Firestore client
            if hasattr(settings, 'GOOGLE_APPLICATION_CREDENTIALS'):
                os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = settings.GOOGLE_APPLICATION_CREDENTIALS
            
            self._client = firestore.Client(project=settings.GOOGLE_CLOUD_PROJECT)
            
            # Initialize Firebase Admin client
            try:
                # Try to get existing app
                app = get_app()
                self._admin_client = admin_firestore.client(app)
            except ValueError:
                # No app exists, create one
                cred = credentials.Certificate(settings.GOOGLE_APPLICATION_CREDENTIALS)
                app = initialize_app(cred, {'projectId': settings.GOOGLE_CLOUD_PROJECT})
                self._admin_client = admin_firestore.client(app)
            
            print("Firestore clients initialized successfully")
            
        except Exception as e:
            print(f"Error initializing Firestore clients: {e}")
            raise
    
    @property
    def client(self):
        """Get standard Firestore client"""
        return self._client
    
    @property
    def admin_client(self):
        """Get Firebase Admin client"""
        return self._admin_client
    
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
    
    def batch_write(self, operations: List[Dict[str, Any]]) -> bool:
        """Perform batch write operations"""
        try:
            batch = self._client.batch()
            
            for operation in operations:
                op_type = operation.get('type')
                collection = operation.get('collection')
                doc_id = operation.get('doc_id')
                data = operation.get('data', {})
                
                doc_ref = self._client.collection(collection).document(doc_id)
                
                if op_type == 'set':
                    data['created_at'] = firestore.SERVER_TIMESTAMP
                    data['updated_at'] = firestore.SERVER_TIMESTAMP
                    batch.set(doc_ref, data)
                elif op_type == 'update':
                    data['updated_at'] = firestore.SERVER_TIMESTAMP
                    batch.update(doc_ref, data)
                elif op_type == 'delete':
                    batch.delete(doc_ref)
            
            batch.commit()
            return True
        except Exception as e:
            print(f"Error in batch write: {e}")
            return False

# Global instance
firestore_client = FirestoreClient()
