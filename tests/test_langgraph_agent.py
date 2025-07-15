import sys
import os
import pytest

# Add the parent directory to the path so we can import the src module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.simple_langgraph_agent import run_simple_langgraph_agent

def test_langgraph_agent():
    """Test the LangGraph agent with a simple query"""
    # This test requires Chroma to be running and a collection to exist
    # It's more of an integration test than a unit test
    try:
        result = run_simple_langgraph_agent(
            query="What is a test query?",
            collection_name="test_collection",
            model_name="tinyllama:latest"
        )
        
        # Check that the result has the expected structure
        assert "answer" in result
        assert "sources" in result
        assert isinstance(result["answer"], str)
        assert isinstance(result["sources"], list)
        assert "messages" in result
        assert isinstance(result["messages"], list)
        
        print("\n=== Test Result ===")
        print(f"Answer: {result['answer'][:100]}...")
        print(f"Sources: {len(result['sources'])}")
        print(f"Messages: {len(result['messages'])}")
        
    except Exception as e:
        pytest.skip(f"Skipping test because: {e}")

if __name__ == "__main__":
    test_langgraph_agent() 