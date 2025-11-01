"""
State management for the Multi-Agent Debate System
"""
from typing import TypedDict, List, Optional, Annotated
from langgraph.graph import add_messages
import operator


class ArgumentEntry(TypedDict):
    """Structure for a single argument in the debate"""
    round: int
    agent: str
    argument: str


class DebateState(TypedDict):
    """
    The state that flows through the debate graph.
    
    Attributes:
        topic: The debate topic
        current_round: Current round number (1-8)
        current_turn: Which agent's turn (AgentA or AgentB)
        arguments: List of all arguments made
        memory_summary: Structured summary of the debate so far
        agent_a_arguments: List of Agent A's arguments
        agent_b_arguments: List of Agent B's arguments
        judge_summary: Final summary from the judge
        winner: The winning agent
        winner_reason: Justification for the winner
        is_complete: Whether the debate is finished
        error: Any error that occurred
    """
    topic: str
    current_round: int
    current_turn: str
    arguments: Annotated[List[ArgumentEntry], operator.add]
    memory_summary: str
    agent_a_arguments: List[str]
    agent_b_arguments: List[str]
    judge_summary: Optional[str]
    winner: Optional[str]
    winner_reason: Optional[str]
    is_complete: bool
    error: Optional[str]


def initialize_state(topic: str) -> DebateState:
    """Initialize a new debate state"""
    return DebateState(
        topic=topic,
        current_round=1,
        current_turn="AgentA",
        arguments=[],
        memory_summary="",
        agent_a_arguments=[],
        agent_b_arguments=[],
        judge_summary=None,
        winner=None,
        winner_reason=None,
        is_complete=False,
        error=None
    )


def validate_state(state: DebateState) -> tuple[bool, str]:
    """
    Validate the debate state
    
    Returns:
        tuple: (is_valid, error_message)
    """
    # Check round bounds
    if state["current_round"] < 1 or state["current_round"] > 8:
        return False, f"Invalid round number: {state['current_round']}"
    
    # Check turn validity
    if state["current_turn"] not in ["AgentA", "AgentB", "Judge"]:
        return False, f"Invalid turn: {state['current_turn']}"
    
    # Check argument count matches round
    expected_args = state["current_round"]
    actual_args = len(state["arguments"])
    
    # For odd rounds, AgentA should have spoken
    # For even rounds, both agents should have equal arguments so far
    if state["current_round"] <= 8:
        if actual_args != expected_args:
            # Allow for the current argument being added
            if actual_args != expected_args - 1:
                return False, f"Argument count mismatch: expected {expected_args}, got {actual_args}"
    
    return True, ""


def check_duplicate_argument(state: DebateState, new_argument: str, agent: str) -> bool:
    """
    Check if an argument is too similar to previous arguments by the same agent
    
    Returns:
        bool: True if argument is unique enough, False if it's a duplicate
    """
    # Get previous arguments from the same agent
    if agent == "AgentA":
        previous_args = state["agent_a_arguments"]
    else:
        previous_args = state["agent_b_arguments"]
    
    # Simple duplicate check - in production, use semantic similarity
    new_arg_lower = new_argument.lower().strip()
    
    for prev_arg in previous_args:
        prev_arg_lower = prev_arg.lower().strip()
        # Check for exact or very similar matches
        if new_arg_lower == prev_arg_lower:
            return False
        # Check for high similarity (simple word overlap check)
        new_words = set(new_arg_lower.split())
        prev_words = set(prev_arg_lower.split())
        if len(new_words.intersection(prev_words)) / max(len(new_words), len(prev_words)) > 0.8:
            return False
    
    return True
