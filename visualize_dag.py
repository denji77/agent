"""
Alternative visualization using text-based DAG representation
This is used as a fallback if graphviz is not available
"""

def generate_text_dag():
    """Generate a text-based representation of the debate DAG"""
    dag = """
╔════════════════════════════════════════════════════════════════════════════╗
║                     MULTI-AGENT DEBATE DAG STRUCTURE                        ║
╚════════════════════════════════════════════════════════════════════════════╝

                                   START
                                     │
                                     ▼
                            ┌──────────────────┐
                            │  UserInputNode   │
                            │  (Get Topic)     │
                            └──────────────────┘
                                     │
                                     ▼
                            ┌──────────────────┐
                            │   MemoryNode     │
                            │ (Initialize)     │
                            └──────────────────┘
                                     │
                    ┌────────────────┴────────────────┐
                    │                                 │
                    ▼                                 ▼
         ╔═══════════════════╗             ╔═══════════════════╗
         ║   ROUND 1-4       ║             ║   ROUND 5-8       ║
         ╚═══════════════════╝             ╚═══════════════════╝
                    │                                 │
    ┌───────────────┼─────────────────┐              │
    │               │                 │              │
    ▼               ▼                 ▼              ▼
┌─────────┐   ┌─────────┐      ┌─────────┐   ┌─────────┐
│ AgentA  │   │ AgentB  │      │ AgentA  │   │ AgentB  │
│(Scientist)  │(Philosopher)    │(Scientist)  │(Philosopher)
│ Round 1 │   │ Round 1 │      │ Round 2 │   │ Round 2 │
└─────────┘   └─────────┘      └─────────┘   └─────────┘
    │               │                 │              │
    └───────────────┼─────────────────┘              │
                    │                                │
                    ▼                                │
           ┌──────────────────┐                     │
           │   MemoryNode     │                     │
           │ (Update Summary) │                     │
           └──────────────────┘                     │
                    │                                │
                    └────────────────────────────────┘
                                   │
                    [After 8 rounds complete]
                                   │
                                   ▼
                          ┌──────────────────┐
                          │    JudgeNode     │
                          │  (Evaluate &     │
                          │  Declare Winner) │
                          └──────────────────┘
                                   │
                                   ▼
                                  END

╔════════════════════════════════════════════════════════════════════════════╗
║                              NODE DESCRIPTIONS                              ║
╚════════════════════════════════════════════════════════════════════════════╝

UserInputNode:    Accepts debate topic from user input
MemoryNode:       Maintains structured summary of debate history
AgentA:           Scientist persona - makes evidence-based arguments
AgentB:           Philosopher persona - makes ethical/conceptual arguments
JudgeNode:        Evaluates all arguments and declares winner with justification

╔════════════════════════════════════════════════════════════════════════════╗
║                              FLOW CONTROL                                   ║
╚════════════════════════════════════════════════════════════════════════════╝

• Total Rounds: 8 (4 arguments per agent)
• Turn Order: AgentA → AgentB (alternating)
• State Validation: Prevents duplicate arguments and turn violations
• Memory Updates: After each round to maintain context
• Judgment: Only triggered after round 8 is complete

"""
    return dag


def save_text_dag(output_path: str = "debate_dag_structure.txt"):
    """Save the text DAG to a file"""
    dag = generate_text_dag()
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(dag)
    print(f"Text-based DAG structure saved to {output_path}")
    return dag


if __name__ == "__main__":
    # Generate and display the DAG
    print(generate_text_dag())
    save_text_dag()
