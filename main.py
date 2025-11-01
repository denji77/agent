"""
Main execution file for the Multi-Agent Debate System
"""
import sys
from state import initialize_state, validate_state
from logger import DebateLogger
from graph import create_debate_graph, visualize_graph
import config


def get_user_topic() -> str:
    """
    Get debate topic from user via CLI
    """
    print("\n" + "="*80)
    print("MULTI-AGENT DEBATE SYSTEM")
    print("="*80)
    print(f"\nDebate Participants:")
    print(f"  • {config.AGENT_A_PERSONA['name']}: {config.AGENT_A_PERSONA['role']}")
    print(f"  • {config.AGENT_B_PERSONA['name']}: {config.AGENT_B_PERSONA['role']}")
    print(f"\nDebate Format: {config.TOTAL_ROUNDS} rounds ({config.ARGUMENTS_PER_AGENT} arguments per agent)")
    print("="*80 + "\n")
    
    topic = input("Enter topic for debate: ").strip()
    
    if not topic:
        print("Error: Topic cannot be empty")
        sys.exit(1)
    
    return topic


def run_debate(topic: str):
    """
    Run the complete debate with the given topic
    """
    # Initialize logger
    logger = DebateLogger(topic)
    
    # Initialize state
    state = initialize_state(topic)
    
    # Validate initial state
    is_valid, error = validate_state(state)
    if not is_valid:
        logger.log_error(f"Initial state invalid: {error}")
        return
    
    # Create graph
    logger._write_to_file("\n[SYSTEM] Building debate graph...\n")
    app = create_debate_graph(logger)
    
    # Generate visualization
    visualize_graph(app, "debate_dag.png")
    
    # Run the debate
    logger._write_to_file("\n[SYSTEM] Starting debate execution...\n\n")
    
    try:
        # Execute the graph with increased recursion limit
        final_state = app.invoke(state, config={"recursion_limit": 100})
        
        # Check for errors
        if final_state.get("error"):
            logger.log_error(f"Debate failed: {final_state['error']}")
            return
        
        # Verify completion
        if not final_state.get("is_complete"):
            logger.log_error("Debate did not complete successfully")
            return
        
        # Success
        logger.finalize()
        print(f"\nDebate completed successfully!")
        print(f"Log file: {logger.log_file}")
        
    except Exception as e:
        logger.log_error(f"Exception during debate: {str(e)}")
        import traceback
        logger._write_to_file(f"\n{traceback.format_exc()}\n")
        raise


def main():
    """
    Main entry point
    """
    # Check for API key
    if not config.PERPLEXITY_API_KEY or config.PERPLEXITY_API_KEY == "your_perplexity_api_key_here":
        print("\n" + "="*80)
        print("ERROR: Perplexity API key not configured")
        print("="*80)
        print("\nPlease set your Perplexity API key:")
        print("1. Copy .env.example to .env")
        print("2. Edit .env and add your API key: PERPLEXITY_API_KEY=your_key_here")
        print("\nOr set it as an environment variable:")
        print("  export PERPLEXITY_API_KEY=your_key_here  (Linux/Mac)")
        print("  $env:PERPLEXITY_API_KEY='your_key_here'  (Windows PowerShell)")
        print("="*80 + "\n")
        sys.exit(1)
    
    # Get topic from user
    topic = get_user_topic()
    
    # Run debate
    run_debate(topic)


if __name__ == "__main__":
    main()
