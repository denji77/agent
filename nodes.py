"""
Node implementations for the Multi-Agent Debate System
"""
from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import config
from state import DebateState, check_duplicate_argument


class DebateNodes:
    """Container for all debate node functions"""
    
    def __init__(self, logger):
        """Initialize nodes with logger and LLM"""
        self.logger = logger
        self.llm = ChatOpenAI(
            model=config.MODEL_NAME,
            temperature=0.7,
            api_key=config.PERPLEXITY_API_KEY,
            base_url=config.PERPLEXITY_BASE_URL
        )
    
    def user_input_node(self, state: DebateState) -> Dict[str, Any]:
        """
        UserInputNode: Accepts the debate topic (already set in initial state)
        This node just validates and passes through the topic
        """
        self.logger.log_state_transition("START", "UserInputNode", state["current_round"])
        
        if not state["topic"]:
            return {
                "error": "No topic provided",
                "is_complete": True
            }
        
        self.logger._write_to_file(f"\n[UserInputNode] Topic accepted: {state['topic']}\n")
        print(f"\nStarting debate between {config.AGENT_A_PERSONA['name']} and {config.AGENT_B_PERSONA['name']}...")
        print(f"Topic: {state['topic']}\n")
        
        return {}
    
    def agent_a_node(self, state: DebateState) -> Dict[str, Any]:
        """
        Agent A Node: Scientist making an argument
        """
        self.logger.log_state_transition(
            "MemoryNode" if state["current_round"] > 1 else "UserInputNode",
            "AgentA",
            state["current_round"]
        )
        
        # Validate it's Agent A's turn
        if state["current_turn"] != "AgentA":
            error_msg = f"State error: Not Agent A's turn (current: {state['current_turn']})"
            self.logger.log_error(error_msg)
            return {"error": error_msg}
        
        # Build context from memory
        context = self._build_agent_context(state, "AgentA")
        
        # Generate argument
        prompt = ChatPromptTemplate.from_messages([
            ("system", f"""You are a {config.AGENT_A_PERSONA['role']}.
Your style: {config.AGENT_A_PERSONA['style']}

You are in round {state['current_round']} of 8 in a debate.
Topic: {state['topic']}

{context}

Provide a compelling argument supporting your position. Be concise (2-3 sentences).
Make sure your argument is unique and builds on the debate so far."""),
            ("user", "Make your argument for this round.")
        ])
        
        chain = prompt | self.llm
        response = chain.invoke({})
        argument = response.content.strip()
        
        # Check for duplicate
        if not check_duplicate_argument(state, argument, "AgentA"):
            self.logger.log_validation("Duplicate argument detected, regenerating...")
            # Regenerate with stronger uniqueness requirement
            prompt = ChatPromptTemplate.from_messages([
                ("system", f"""You are a {config.AGENT_A_PERSONA['role']}.
Your previous arguments: {', '.join(state['agent_a_arguments'])}

Make a NEW, DIFFERENT argument. Topic: {state['topic']}"""),
                ("user", "Provide a fresh perspective.")
            ])
            chain = prompt | self.llm
            response = chain.invoke({})
            argument = response.content.strip()
        
        # Log argument
        self.logger.log_argument(state["current_round"], config.AGENT_A_PERSONA['name'], argument)
        
        # AgentA always passes to AgentB in the same round
        return {
            "arguments": [{
                "round": state["current_round"],
                "agent": "AgentA",
                "argument": argument
            }],
            "agent_a_arguments": state["agent_a_arguments"] + [argument],
            "current_turn": "AgentB"
        }
    
    def agent_b_node(self, state: DebateState) -> Dict[str, Any]:
        """
        Agent B Node: Philosopher making an argument
        """
        self.logger.log_state_transition("AgentA", "AgentB", state["current_round"])
        
        # Validate it's Agent B's turn
        if state["current_turn"] != "AgentB":
            error_msg = f"State error: Not Agent B's turn (current: {state['current_turn']})"
            self.logger.log_error(error_msg)
            return {"error": error_msg}
        
        # Build context from memory
        context = self._build_agent_context(state, "AgentB")
        
        # Generate argument
        prompt = ChatPromptTemplate.from_messages([
            ("system", f"""You are a {config.AGENT_B_PERSONA['role']}.
Your style: {config.AGENT_B_PERSONA['style']}

You are in round {state['current_round']} of 8 in a debate.
Topic: {state['topic']}

{context}

Provide a compelling argument supporting your position. Be concise (2-3 sentences).
Make sure your argument is unique and builds on the debate so far."""),
            ("user", "Make your argument for this round.")
        ])
        
        chain = prompt | self.llm
        response = chain.invoke({})
        argument = response.content.strip()
        
        # Check for duplicate
        if not check_duplicate_argument(state, argument, "AgentB"):
            self.logger.log_validation("Duplicate argument detected, regenerating...")
            prompt = ChatPromptTemplate.from_messages([
                ("system", f"""You are a {config.AGENT_B_PERSONA['role']}.
Your previous arguments: {', '.join(state['agent_b_arguments'])}

Make a NEW, DIFFERENT argument. Topic: {state['topic']}"""),
                ("user", "Provide a fresh perspective.")
            ])
            chain = prompt | self.llm
            response = chain.invoke({})
            argument = response.content.strip()
        
        # Log argument
        self.logger.log_argument(state["current_round"], config.AGENT_B_PERSONA['name'], argument)
        
        # Check if this was the last round (round 8)
        if state["current_round"] >= 8:
            # Debate complete, go to judge
            return {
                "arguments": [{
                    "round": state["current_round"],
                    "agent": "AgentB",
                    "argument": argument
                }],
                "agent_b_arguments": state["agent_b_arguments"] + [argument],
                "current_turn": "Judge"
            }
        else:
            # Move to next round
            new_round = state["current_round"] + 1
            return {
                "arguments": [{
                    "round": state["current_round"],
                    "agent": "AgentB",
                    "argument": argument
                }],
                "agent_b_arguments": state["agent_b_arguments"] + [argument],
                "current_round": new_round,
                "current_turn": "AgentA"
            }
    
    def memory_node(self, state: DebateState) -> Dict[str, Any]:
        """
        Memory Node: Updates and maintains debate summary
        """
        self.logger.log_state_transition(
            "AgentB" if state["current_round"] > 1 else "UserInputNode",
            "MemoryNode",
            state["current_round"]
        )
        
        # Build summary of debate so far
        if len(state["arguments"]) == 0:
            summary = "Debate is about to begin."
        else:
            # Create structured summary
            summary_parts = [f"Topic: {state['topic']}\n"]
            summary_parts.append(f"Rounds completed: {len(state['arguments']) // 2}\n")
            summary_parts.append("\nRecent arguments:")
            
            # Show last 4 arguments for context
            recent_args = state["arguments"][-4:] if len(state["arguments"]) > 4 else state["arguments"]
            for arg in recent_args:
                agent_name = config.AGENT_A_PERSONA['name'] if arg['agent'] == 'AgentA' else config.AGENT_B_PERSONA['name']
                summary_parts.append(f"\n- Round {arg['round']} ({agent_name}): {arg['argument']}")
            
            summary = "\n".join(summary_parts)
        
        self.logger.log_memory_update(state["current_round"], summary)
        
        return {
            "memory_summary": summary
        }
    
    def judge_node(self, state: DebateState) -> Dict[str, Any]:
        """
        Judge Node: Evaluates all arguments and declares a winner
        """
        self.logger.log_state_transition("AgentB", "JudgeNode", 8)
        
        # Build complete debate transcript
        transcript = self._build_full_transcript(state)
        
        # Generate judgment
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an impartial debate judge. Analyze the debate carefully and:
1. Provide a comprehensive summary of the key arguments from both sides
2. Evaluate the logical coherence, evidence quality, and persuasiveness of each side
3. Declare a winner and provide detailed justification

Be objective and focus on the quality of reasoning, not personal bias."""),
            ("user", f"""Topic: {state['topic']}

Full Debate Transcript:
{transcript}

Provide your judgment in the following format:
SUMMARY: [comprehensive summary]
WINNER: [AgentA or AgentB]
REASON: [detailed justification]""")
        ])
        
        chain = prompt | self.llm
        response = chain.invoke({})
        judgment = response.content.strip()
        
        # Parse judgment
        summary, winner, reason = self._parse_judgment(judgment)
        
        # Map to agent names
        winner_name = config.AGENT_A_PERSONA['name'] if winner == "AgentA" else config.AGENT_B_PERSONA['name']
        
        # Log judgment
        self.logger.log_judge_summary(summary, winner_name, reason)
        
        return {
            "judge_summary": summary,
            "winner": winner_name,
            "winner_reason": reason,
            "is_complete": True
        }
    
    def _build_agent_context(self, state: DebateState, agent: str) -> str:
        """Build context for an agent from memory"""
        if len(state["arguments"]) == 0:
            return "This is the opening argument."
        
        context_parts = ["Previous arguments in this debate:"]
        for arg in state["arguments"]:
            agent_name = config.AGENT_A_PERSONA['name'] if arg['agent'] == 'AgentA' else config.AGENT_B_PERSONA['name']
            context_parts.append(f"- {agent_name}: {arg['argument']}")
        
        return "\n".join(context_parts)
    
    def _build_full_transcript(self, state: DebateState) -> str:
        """Build complete debate transcript"""
        transcript_parts = []
        for arg in state["arguments"]:
            agent_name = config.AGENT_A_PERSONA['name'] if arg['agent'] == 'AgentA' else config.AGENT_B_PERSONA['name']
            transcript_parts.append(f"[Round {arg['round']}] {agent_name}: {arg['argument']}")
        return "\n\n".join(transcript_parts)
    
    def _parse_judgment(self, judgment: str) -> tuple[str, str, str]:
        """Parse the judgment response"""
        summary = ""
        winner = ""
        reason = ""
        
        lines = judgment.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            if line.startswith("SUMMARY:"):
                current_section = "summary"
                summary = line.replace("SUMMARY:", "").strip()
            elif line.startswith("WINNER:"):
                current_section = "winner"
                winner_text = line.replace("WINNER:", "").strip()
                # Extract AgentA or AgentB
                if "Scientist" in winner_text or "Agent A" in winner_text or "AgentA" in winner_text:
                    winner = "AgentA"
                elif "Philosopher" in winner_text or "Agent B" in winner_text or "AgentB" in winner_text:
                    winner = "AgentB"
                else:
                    winner = "AgentA"  # Default
            elif line.startswith("REASON:"):
                current_section = "reason"
                reason = line.replace("REASON:", "").strip()
            elif current_section and line:
                if current_section == "summary":
                    summary += " " + line
                elif current_section == "reason":
                    reason += " " + line
        
        return summary.strip(), winner, reason.strip()
