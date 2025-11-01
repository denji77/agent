"""
Graph construction for the Multi-Agent Debate System using LangGraph
"""
from langgraph.graph import StateGraph, END
from state import DebateState
from nodes import DebateNodes


def should_continue_debate(state: DebateState) -> str:
    """
    Conditional edge to determine next node in the graph
    """
    # Check for errors
    if state.get("error"):
        return END
    
    # Check if debate is complete
    if state.get("is_complete"):
        return END
    
    # Determine next node based on current turn
    current_turn = state.get("current_turn", "AgentA")
    
    if current_turn == "AgentA":
        return "agent_a"
    elif current_turn == "AgentB":
        return "agent_b"
    elif current_turn == "Judge":
        return "judge"
    else:
        return END


def create_debate_graph(logger):
    """
    Create and compile the debate graph
    
    Graph structure:
    START -> UserInput -> Memory -> AgentA -> AgentB -> Memory -> ... -> Judge -> END
    """
    # Initialize nodes
    nodes = DebateNodes(logger)
    
    # Create graph
    workflow = StateGraph(DebateState)
    
    # Add nodes
    workflow.add_node("user_input", nodes.user_input_node)
    workflow.add_node("memory", nodes.memory_node)
    workflow.add_node("agent_a", nodes.agent_a_node)
    workflow.add_node("agent_b", nodes.agent_b_node)
    workflow.add_node("judge", nodes.judge_node)
    
    # Set entry point
    workflow.set_entry_point("user_input")
    
    # Add edges
    # UserInput -> Memory (to initialize)
    workflow.add_edge("user_input", "memory")
    
    # Memory -> conditional (to appropriate agent)
    workflow.add_conditional_edges(
        "memory",
        should_continue_debate,
        {
            "agent_a": "agent_a",
            "agent_b": "agent_b",
            "judge": "judge",
            END: END
        }
    )
    
    # AgentA -> AgentB (within same round)
    workflow.add_edge("agent_a", "agent_b")
    
    # AgentB -> conditional (either Memory for next round or Judge if done)
    workflow.add_conditional_edges(
        "agent_b",
        should_continue_debate,
        {
            "agent_a": "memory",  # Go back to memory before next agent A
            "judge": "judge",
            END: END
        }
    )
    
    # Judge -> END
    workflow.add_edge("judge", END)
    
    # Compile graph
    app = workflow.compile()
    
    return app


def visualize_graph(app, output_path: str = "debate_dag.png"):
    """
    Visualize the debate graph and save to file
    """
    try:
        # Get the graph visualization
        graph_image = app.get_graph().draw_mermaid_png()
        
        with open(output_path, 'wb') as f:
            f.write(graph_image)
        
        print(f"Graph visualization saved to {output_path}")
        return True
    except Exception as e:
        print(f"Could not generate graph visualization: {e}")
        print("You may need to install graphviz: pip install graphviz")
        return False
