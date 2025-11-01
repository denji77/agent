"""
Logging utilities for the Multi-Agent Debate System
"""
import os
from datetime import datetime
from typing import Optional
import config


class DebateLogger:
    """Handles logging of all debate activities to file and console"""
    
    def __init__(self, topic: str):
        """Initialize logger with a topic"""
        self.topic = topic
        self.log_entries = []
        
        # Create logs directory if it doesn't exist
        if not os.path.exists(config.LOG_DIR):
            os.makedirs(config.LOG_DIR)
        
        # Create log file with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = os.path.join(config.LOG_DIR, f"debate_log_{timestamp}.txt")
        
        # Write header
        self._write_header()
    
    def _write_header(self):
        """Write the log file header"""
        header = f"""
{'='*80}
MULTI-AGENT DEBATE LOG
{'='*80}
Topic: {self.topic}
Date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
{'='*80}

"""
        self._write_to_file(header)
    
    def _write_to_file(self, content: str):
        """Write content to log file"""
        if config.ENABLE_LOGGING:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(content)
    
    def log_state_transition(self, from_node: str, to_node: str, round_num: int):
        """Log a state transition between nodes"""
        entry = f"\n[STATE TRANSITION] Round {round_num}: {from_node} -> {to_node}\n"
        self._write_to_file(entry)
        self.log_entries.append(entry)
    
    def log_argument(self, round_num: int, agent: str, argument: str):
        """Log an argument from an agent"""
        # Add extra line break between rounds for readability
        if agent == "Scientist":
            entry = f"\n{'='*80}\n[Round {round_num}] {agent}: {argument}\n"
            print(f"\n{'='*80}")
        else:
            entry = f"\n[Round {round_num}] {agent}: {argument}\n"
        
        print(f"[Round {round_num}] {agent}: {argument}")
        self._write_to_file(entry)
        self.log_entries.append(entry)
    
    def log_memory_update(self, round_num: int, summary: str):
        """Log memory summary update"""
        entry = f"\n[MEMORY UPDATE - Round {round_num}]\n{summary}\n"
        self._write_to_file(entry)
        self.log_entries.append(entry)
    
    def log_judge_summary(self, summary: str, winner: str, reason: str):
        """Log the final judge's decision"""
        entry = f"""
{'='*80}
JUDGE'S FINAL VERDICT
{'='*80}

[Judge] Summary of debate:
{summary}

[Judge] Winner: {winner}

Reason: {reason}

{'='*80}
"""
        print(entry)
        self._write_to_file(entry)
        self.log_entries.append(entry)
    
    def log_error(self, error: str):
        """Log an error"""
        entry = f"\n[ERROR] {error}\n"
        print(entry)
        self._write_to_file(entry)
        self.log_entries.append(entry)
    
    def log_validation(self, message: str):
        """Log validation checks"""
        entry = f"[VALIDATION] {message}\n"
        self._write_to_file(entry)
        self.log_entries.append(entry)
    
    def finalize(self):
        """Write final footer to log"""
        footer = f"\n{'='*80}\nDEBATE COMPLETED\nLog saved to: {self.log_file}\n{'='*80}\n"
        print(footer)
        self._write_to_file(footer)
