# Multi-Agent Debate System using LangGraph

A sophisticated debate simulation system built with LangGraph where two AI agents (Scientist vs Philosopher) engage in a structured 8-round debate, complete with memory management, state validation, and automated judging.

## 🎯 Project Overview

This system implements a directed acyclic graph (DAG) workflow using LangGraph to orchestrate a debate between two AI agents with distinct personas. The debate includes:

- **8 rounds** of structured argumentation (4 arguments per agent)
- **Memory management** to maintain debate context
- **State validation** to ensure logical flow and prevent duplicates
- **Automated judging** with detailed justification
- **Complete logging** of all interactions and state transitions

## 📋 Features

- ✅ **UserInputNode**: Accepts debate topic at runtime
- ✅ **AgentA (Scientist)**: Makes evidence-based, empirical arguments
- ✅ **AgentB (Philosopher)**: Makes ethical, conceptual arguments
- ✅ **MemoryNode**: Maintains structured debate history
- ✅ **JudgeNode**: Evaluates arguments and declares winner
- ✅ **State Validation**: Prevents turn violations and duplicate arguments
- ✅ **Comprehensive Logging**: All messages and transitions logged to file
- ✅ **CLI Interface**: Clean command-line interaction
- ✅ **DAG Visualization**: Visual representation of the graph structure

## 🏗️ Architecture

### Node Structure

```
START → UserInputNode → MemoryNode → [AgentA ↔ AgentB] × 4 rounds → JudgeNode → END
```

### Key Components

1. **State Management** (`state.py`): Defines debate state, validation logic, and duplicate detection
2. **Nodes** (`nodes.py`): Implements all debate nodes (UserInput, AgentA, AgentB, Memory, Judge)
3. **Graph** (`graph.py`): Constructs the LangGraph workflow with conditional edges
4. **Logger** (`logger.py`): Handles file and console logging
5. **Config** (`config.py`): Centralized configuration for agents and settings
6. **Main** (`main.py`): CLI interface and execution orchestration

### State Flow

```python
DebateState {
    topic: str                    # Debate topic
    current_round: int            # Current round (1-8)
    current_turn: str             # Current agent's turn
    arguments: List[ArgumentEntry]# All arguments made
    memory_summary: str           # Debate history summary
    agent_a_arguments: List[str]  # Agent A's arguments
    agent_b_arguments: List[str]  # Agent B's arguments
    judge_summary: str            # Final summary
    winner: str                   # Winning agent
    winner_reason: str            # Justification
    is_complete: bool             # Completion flag
    error: str                    # Error tracking
}
```

## 🚀 Installation

### Prerequisites

- Python 3.9 or higher
- OpenAI API key

### Setup Steps

1. **Clone or download this repository**

2. **Create a virtual environment (recommended)**
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. **Install dependencies**
   ```powershell
   pip install -r requirements.txt
   ```

4. **Configure OpenAI API Key**
   
   Copy the example environment file:
   ```powershell
   copy .env.example .env
   ```
   
   Edit `.env` and add your OpenAI API key:
   ```
   OPENAI_API_KEY=sk-your-actual-api-key-here
   ```

   Alternatively, set as environment variable:
   ```powershell
   $env:OPENAI_API_KEY='sk-your-actual-api-key-here'
   ```

## 💻 Usage

### Running the Debate

```powershell
python main.py
```

### Example Interaction

```
================================================================================
MULTI-AGENT DEBATE SYSTEM
================================================================================

Debate Participants:
  • Scientist: A rigorous scientist who emphasizes empirical evidence...
  • Philosopher: A philosophical thinker who values autonomy...

Debate Format: 8 rounds (4 arguments per agent)
================================================================================

Enter topic for debate: Should AI be regulated like medicine?

Starting debate between Scientist and Philosopher...
Topic: Should AI be regulated like medicine?

[Round 1] Scientist: AI systems directly impact human health and safety through medical diagnoses, autonomous vehicles, and critical infrastructure. Just as pharmaceutical drugs require rigorous testing and approval processes, AI applications with similar risk profiles must undergo systematic validation to prevent catastrophic failures.

[Round 1] Philosopher: While safety concerns are valid, medicine regulation evolved over centuries through trial and societal consensus. Prematurely imposing rigid frameworks on AI could stifle the philosophical and creative exploration necessary for understanding consciousness, ethics, and human autonomy in the digital age.

[Round 2] Scientist: The difference is that AI can scale instantly and globally, unlike medicines which have natural constraints...

...

[Round 8] Philosopher: History shows that overregulation often delays societal evolution...

================================================================================
JUDGE'S FINAL VERDICT
================================================================================

[Judge] Summary of debate:
The Scientist presented a compelling case grounded in risk assessment, public safety, and empirical evidence of AI's potential harms. They drew strong parallels to pharmaceutical regulation and emphasized the urgency given AI's rapid deployment and scale. The Philosopher countered with concerns about stifling innovation, the need for organic regulatory evolution, and the importance of preserving autonomy and ethical exploration. While both sides presented coherent arguments, the Scientist's focus on measurable risks and precedent in medical regulation provided more concrete justification for immediate action.

[Judge] Winner: Scientist

Reason: The Scientist's arguments were more grounded in demonstrable risks and provided clearer, actionable frameworks. The emphasis on public safety, systematic validation, and learning from established medical regulatory models created a more compelling case for AI regulation. The Philosopher raised important philosophical concerns but lacked specific counterproposals for managing near-term risks.

================================================================================
```

## 📊 Output Files

After each debate, the system generates:

1. **Log File**: `logs/debate_log_YYYYMMDD_HHMMSS.txt`
   - Complete transcript of all arguments
   - State transitions between nodes
   - Memory updates
   - Final judgment and reasoning

2. **DAG Visualization**: `debate_dag.png` (if graphviz is available)
   - Visual representation of the graph structure

3. **Text DAG**: `debate_dag_structure.txt`
   - ASCII art representation of the workflow

## 🔧 Configuration

Edit `config.py` to customize:

- **Model**: Change `MODEL_NAME` (e.g., "gpt-4", "gpt-3.5-turbo")
- **Rounds**: Modify `TOTAL_ROUNDS` (default: 8)
- **Agent Personas**: Customize `AGENT_A_PERSONA` and `AGENT_B_PERSONA`
- **Logging**: Configure `LOG_DIR` and `ENABLE_LOGGING`

## 📁 Project Structure

```
agent/
├── main.py                  # Main entry point and CLI
├── config.py                # Configuration settings
├── state.py                 # State management and validation
├── nodes.py                 # LangGraph node implementations
├── graph.py                 # Graph construction and visualization
├── logger.py                # Logging utilities
├── visualize_dag.py         # DAG visualization helper
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variable template
├── .gitignore              # Git ignore rules
├── README.md               # This file
└── logs/                   # Generated log files
    └── debate_log_*.txt
```

## 🧪 State Validation

The system implements comprehensive validation:

- **Turn Control**: Ensures agents only speak during their assigned turn
- **Round Bounds**: Validates round numbers stay within 1-8
- **Duplicate Detection**: Prevents repeated arguments using similarity checking
- **Logical Coherence**: Validates state consistency across transitions

## 🎨 DAG Visualization

The system can generate visualizations in two formats:

1. **PNG Image** (requires graphviz):
   ```python
   from graph import visualize_graph
   visualize_graph(app, "debate_dag.png")
   ```

2. **Text-based ASCII art**:
   ```powershell
   python visualize_dag.py
   ```

## 🐛 Troubleshooting

### "Import could not be resolved" errors

These are IDE warnings before dependencies are installed. Run:
```powershell
pip install -r requirements.txt
```

### "OpenAI API key not configured"

Ensure your `.env` file contains a valid API key:
```
OPENAI_API_KEY=sk-your-key-here
```

### Graphviz visualization fails

Install graphviz separately:
```powershell
pip install graphviz
# For Windows, also install the graphviz executable from: https://graphviz.org/download/
```

The text-based DAG will be generated as a fallback.

## 📝 Example Log Output

See `logs/` directory for complete examples. Each log includes:

- Debate topic and timestamp
- State transitions: `[STATE TRANSITION] Round X: NodeA -> NodeB`
- Arguments: `[Round X] Agent: argument text`
- Memory updates: `[MEMORY UPDATE - Round X]`
- Validation checks: `[VALIDATION] message`
- Final verdict with summary, winner, and reasoning

## 🎥 Demo Video

The demo video should cover:
1. Project structure walkthrough
2. Running the CLI
3. Observing the debate flow
4. Examining the judge's decision process
5. Reviewing the log files

## 📚 Technical Details

### LangGraph Integration

- Uses `StateGraph` for workflow definition
- Conditional edges for dynamic routing
- State persistence across nodes
- Built-in support for cyclic flows

### Agent Personas

**Scientist**:
- Focus: Empirical evidence, data, risk assessment
- Style: Logical, evidence-based, measurable outcomes
- Strength: Concrete examples and precedents

**Philosopher**:
- Focus: Ethical principles, autonomy, societal evolution
- Style: Conceptual, historical context, long-term implications
- Strength: Fundamental principles and philosophical depth

### Judge Logic

The judge evaluates:
1. Logical coherence of arguments
2. Quality and relevance of evidence
3. Persuasiveness and structure
4. Addressing counterarguments
5. Overall debate strategy

## 🤝 Contributing

This is a technical assignment project. For production use, consider:
- Adding more sophisticated duplicate detection (semantic embeddings)
- Implementing multiple judge consensus
- Supporting custom agent personas
- Adding debate topic suggestions
- Real-time web interface

## 📄 License

This project is created for educational and demonstration purposes.

## 👤 Author

Created as part of the ATG Technical Assignment for Machine Learning Intern position.

## 🙏 Acknowledgments

- Built with [LangGraph](https://github.com/langchain-ai/langgraph)
- Powered by [LangChain](https://github.com/langchain-ai/langchain)
- Uses OpenAI GPT models

---

**Note**: This system is designed to meet all requirements of the ATG Technical Assignment, including:
- ✅ LangGraph-based DAG workflow
- ✅ Two alternating agents with distinct personas
- ✅ Exactly 8 rounds (4 arguments per agent)
- ✅ Memory node with structured summaries
- ✅ Judge node with logical evaluation
- ✅ State validation (turn control, duplicate prevention)
- ✅ Complete logging to file
- ✅ CLI interface
- ✅ DAG visualization
- ✅ Comprehensive documentation
