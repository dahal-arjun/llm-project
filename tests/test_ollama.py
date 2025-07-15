#!/usr/bin/env python3
"""
Simple test script to verify the Ollama integration works.
"""

import sys
import os

# Add the parent directory to the path so we can import the src module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.ollama_integration import OllamaModel

def test_ollama_integration():
    """Test the Ollama integration with a simple query"""
    print("Testing Ollama integration...")
    
    # Initialize the model
    model = OllamaModel(model_name="tinyllama:latest")
    
    # Test with a simple query
    query = "What is a vector database?"
    print(f"Query: {query}")
    print("Generating response...")
    
    response = model.generate_response(query=query)
    
    print("Response:")
    print(response)
    
    # Test with a context
    context = """Vector databases are specialized databases designed for storing and querying vector embeddings efficiently.
    They are particularly useful for semantic search, recommendation systems, and other AI applications.
    Vector databases like Chroma enable features such as Retrieval Augmented Generation (RAG),
    long-term memory for AI assistants, and knowledge base creation and querying."""
    
    print("\nTesting with context...")
    print(f"Query: {query}")
    print("Context provided: Yes")
    print("Generating response...")
    
    response_with_context = model.generate_response(query=query, context=context)
    
    print("Response with context:")
    print(response_with_context)
    
    # Test the chat API
    print("\nTesting chat API...")
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is a vector database?"}
    ]
    
    chat_response = model.chat(messages=messages)
    
    print("Chat response:")
    print(chat_response)

if __name__ == "__main__":
    test_ollama_integration() 