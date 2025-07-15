from typing import Dict, List, TypedDict, Any
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import StateGraph, END

from src.db.chroma_client import chroma_client
from src.services.ollama_service import ollama_service

# Define the state for our agent
class AgentState(TypedDict):
    query: str
    context: List[Dict[str, Any]]
    answer: str
    messages: List[Any]

class LangGraphService:
    def __init__(self):
        self.agent = self.build_agent_graph()
    
    # Create a function to retrieve context from Chroma
    def retrieve(self, state: AgentState) -> AgentState:
        """Retrieve relevant documents from Chroma"""
        query = state["query"]
        collection_name = state.get("collection_name", "documents")
        
        try:
            # Search for relevant documents using our chroma client
            context = chroma_client.query_collection(
                collection_name=collection_name,
                query_text=query,
                n_results=3
            )
            
            # Add a message about retrieval
            messages = state.get("messages", [])
            messages.append(AIMessage(content=f"I've retrieved {len(context)} relevant documents."))
            
            # Return updated state
            return {**state, "context": context, "messages": messages}
        except Exception as e:
            print(f"Error retrieving context: {e}")
            messages = state.get("messages", [])
            messages.append(AIMessage(content=f"Error retrieving documents: {str(e)}"))
            return {**state, "context": [], "messages": messages}

    # Generate a response based on the retrieved context
    def generate_response(self, state: AgentState) -> AgentState:
        """Generate a response based on the retrieved context"""
        query = state["query"]
        context = state["context"]
        
        # Format the context for the prompt
        context_str = "\n\n".join([f"Document {i+1}:\n{doc['content']}\nSource: {doc['metadata']['source']}" 
                                for i, doc in enumerate(context)])
        
        # Create a system message with instructions
        system_message = """You are a helpful assistant. Answer the user's question based on the provided context.
    Be concise and accurate. If the context doesn't contain the information needed, say so."""
        
        # Create a prompt with the query and context
        prompt = f"""Question: {query}

    Context:
    {context_str if context else 'No context available.'}

    Based on the context, please provide a direct and helpful answer to the question."""
        
        # Generate a response
        answer = ollama_service.generate_response(
            query=prompt,
            context=system_message
        )
        
        # Add the answer to the messages
        messages = state.get("messages", [])
        messages.append(AIMessage(content=answer))
        
        # Return the updated state
        return {**state, "answer": answer, "messages": messages}

    # Build the LangGraph agent
    def build_agent_graph(self):
        """Build the LangGraph agent graph"""
        # Create a new graph
        graph = StateGraph(AgentState)
        
        # Add nodes for each step
        graph.add_node("retrieve", self.retrieve)
        graph.add_node("generate", self.generate_response)
        
        # Define the edges
        graph.add_edge("retrieve", "generate")
        graph.add_edge("generate", END)
        
        # Set the entry point
        graph.set_entry_point("retrieve")
        
        # Compile the graph
        return graph.compile()

    # Function to run the agent
    def run_agent(self, query: str, collection_name: str):
        """Run the LangGraph agent"""
        # Create the initial state
        initial_state = {
            "query": query,
            "collection_name": collection_name,
            "context": [],
            "answer": "",
            "messages": [HumanMessage(content=query)]
        }
        
        # Run the agent
        result = self.agent.invoke(initial_state)
        
        # Return the result
        return {
            "answer": result["answer"],
            "sources": result["context"],
            "messages": result["messages"]
        }

# Create a singleton instance
langgraph_service = LangGraphService() 