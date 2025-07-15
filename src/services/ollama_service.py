import requests
from typing import List, Optional, Dict, Any
from src.core.config import settings

class OllamaService:
    def __init__(self):
        self.host = f"http://{settings.OLLAMA_HOST}:{settings.OLLAMA_PORT}"
        self.model_name = settings.DEFAULT_MODEL
        self.generate_endpoint = f"{self.host}/api/generate"
        self.chat_endpoint = f"{self.host}/api/chat"
        self.is_connected = False
    
    def connect(self):
        """Test connection to Ollama"""
        try:
            response = requests.get(f"{self.host}/api/tags")
            if response.status_code == 200:
                models = response.json().get("models", [])
                model_names = [model["name"] for model in models]
                if self.model_name not in model_names:
                    print(f"Warning: Model '{self.model_name}' not found in Ollama. Available models: {model_names}")
                    print(f"Will attempt to use '{self.model_name}' anyway, which may trigger a download.")
                else:
                    print(f"Successfully connected to Ollama. Using model: {self.model_name}")
                self.is_connected = True
                return True
            else:
                print(f"Warning: Could not list models from Ollama. Status code: {response.status_code}")
                return False
        except Exception as e:
            print(f"Warning: Could not connect to Ollama at {self.host}: {e}")
            print("Make sure Ollama is running.")
            return False
    
    def generate_response(self, query: str, context: Optional[str] = None, 
                         max_tokens: int = 512, temperature: float = 0.7, 
                         top_p: float = 0.95) -> str:
        """
        Generate a response from the model
        
        Args:
            query: The user query
            context: Optional context from vector database retrieval
            max_tokens: Maximum number of tokens to generate
            temperature: Temperature for sampling
            top_p: Top-p for nucleus sampling
            
        Returns:
            The generated response text
        """
        # Construct the prompt with context if provided
        if context:
            prompt = f"Context information:\n{context}\n\nQuestion: {query}\n\nAnswer:"
        else:
            prompt = f"Question: {query}\n\nAnswer:"
        
        # Prepare the request payload
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
                "top_p": top_p,
                "num_predict": max_tokens
            }
        }
        
        try:
            response = requests.post(self.generate_endpoint, json=payload)
            if response.status_code == 200:
                result = response.json()
                return result.get("response", "").strip()
            else:
                error_msg = f"Error: Ollama API returned status code {response.status_code}"
                try:
                    error_details = response.json()
                    error_msg += f", {error_details.get('error', '')}"
                except:
                    pass
                raise Exception(error_msg)
        except Exception as e:
            raise Exception(f"Failed to generate response: {str(e)}")
    
    def generate_rag_response(self, query: str, documents: List[str], 
                             max_tokens: int = 512, temperature: float = 0.7) -> str:
        """
        Generate a response using retrieved documents as context
        
        Args:
            query: The user query
            documents: List of retrieved documents from Chroma
            max_tokens: Maximum number of tokens to generate
            temperature: Temperature for sampling
            
        Returns:
            The generated response text
        """
        # Format the context from retrieved documents
        if documents and len(documents) > 0:
            context = "\n\n".join([doc for doc in documents])
            return self.generate_response(query, context, max_tokens, temperature)
        else:
            return self.generate_response(query, None, max_tokens, temperature)
            
    def chat(self, messages: List[Dict[str, str]], 
            max_tokens: int = 512, temperature: float = 0.7) -> str:
        """
        Generate a chat response using Ollama's chat API
        
        Args:
            messages: List of message dictionaries with 'role' and 'content' keys
            max_tokens: Maximum number of tokens to generate
            temperature: Temperature for sampling
            
        Returns:
            The generated response text
        """
        # Prepare the request payload
        payload = {
            "model": self.model_name,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens
            }
        }
        
        try:
            response = requests.post(self.chat_endpoint, json=payload)
            if response.status_code == 200:
                result = response.json()
                return result.get("message", {}).get("content", "").strip()
            else:
                error_msg = f"Error: Ollama API returned status code {response.status_code}"
                try:
                    error_details = response.json()
                    error_msg += f", {error_details.get('error', '')}"
                except:
                    pass
                raise Exception(error_msg)
        except Exception as e:
            raise Exception(f"Failed to generate chat response: {str(e)}")

# Create a singleton instance
ollama_service = OllamaService() 