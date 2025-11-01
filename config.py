"""
Configuration file for the Multi-Agent Debate System
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Perplexity API Configuration
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")
PERPLEXITY_BASE_URL = "https://api.perplexity.ai"
MODEL_NAME = "sonar"  # Perplexity chat model

# Debate Configuration
TOTAL_ROUNDS = 8
ARGUMENTS_PER_AGENT = 4

# Agent Personas
AGENT_A_PERSONA = {
    "name": "Scientist",
    "role": "A rigorous scientist who emphasizes empirical evidence, data, risk assessment, and public safety",
    "style": "logical, evidence-based, focuses on measurable outcomes"
}

AGENT_B_PERSONA = {
    "name": "Philosopher",
    "role": "A philosophical thinker who values autonomy, ethical principles, historical context, and societal evolution",
    "style": "conceptual, ethical, focuses on principles and long-term implications"
}

# Logging Configuration
LOG_DIR = "logs"
ENABLE_LOGGING = True
