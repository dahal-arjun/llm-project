import chromadb
from typing import List, Dict, Any, Optional
from src.core.config import settings

class ChromaDBClient:
    def __init__(self):
        self.client = None
        
    def connect(self):
        """Connect to ChromaDB"""
        try:
            self.client = chromadb.HttpClient(
                host=settings.CHROMA_HOST, 
                port=settings.CHROMA_PORT
            )
            collections = self.client.list_collections()
            print(f"Connected to Chroma. Found {len(collections)} collections.")
            return True
        except Exception as e:
            print(f"Warning: Could not connect to Chroma: {e}")
            print("Make sure Chroma is running.")
            return False
    
    def get_client(self):
        """Get the ChromaDB client"""
        if not self.client:
            self.connect()
        return self.client
    
    def list_collections(self) -> List[str]:
        """List all collections in the database"""
        client = self.get_client()
        collections = client.list_collections()
        return [collection.name for collection in collections]
    
    def create_collection(self, name: str):
        """Create a new collection"""
        client = self.get_client()
        return client.create_collection(name=name)
    
    def get_or_create_collection(self, name: str):
        """Get or create a collection"""
        client = self.get_client()
        return client.get_or_create_collection(name=name)
    
    def get_collection(self, name: str):
        """Get a collection"""
        client = self.get_client()
        return client.get_collection(name=name)
    
    def add_documents(self, collection_name: str, documents: List[str], 
                     ids: List[str], metadatas: List[Dict[str, Any]]):
        """Add documents to a collection"""
        collection = self.get_or_create_collection(collection_name)
        collection.add(
            documents=documents,
            ids=ids,
            metadatas=metadatas
        )
    
    def query_collection(self, collection_name: str, query_text: str, n_results: int = 3):
        """Query a collection"""
        try:
            collection = self.get_collection(name=collection_name)
            results = collection.query(
                query_texts=[query_text],
                n_results=n_results
            )
            
            # Extract documents and metadata
            documents = results['documents'][0] if results['documents'] else []
            metadatas = results['metadatas'][0] if results['metadatas'] else []
            
            # Format context
            context = []
            for doc, meta in zip(documents, metadatas):
                context.append({
                    "content": doc,
                    "metadata": meta
                })
            
            return context
        except Exception as e:
            print(f"Error querying collection: {e}")
            return []

# Create a singleton instance
chroma_client = ChromaDBClient() 