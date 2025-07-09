import sys
from .workflow import app
from .config import DEFAULT_MAX_ITERATIONS


def run_agent(query: str):
    """
    Runs the multi-agent system with a given query.
    """
    initial_state = {
        "question": query,
        "original_question": query,
        "messages": [("human", query)],
        "iteration_count": 1,
        "max_iterations": DEFAULT_MAX_ITERATIONS,
    }

    config = {"recursion_limit": 10}

    # The final result is a stream of events, get the last one for the final state
    final_result = None
    for event in app.stream(initial_state, config=config):
        final_result = event

    # The actual final state is in the 'data' of the last event
    if final_result:
        final_state_data = list(final_result.values())[0]
        print("\n--- Final Answer ---")
        print(final_state_data.get('answer'))
    else:
        print("The agent execution did not produce a result.")


if __name__ == "__main__":
    # You can run this script with a question from the command line
    # Example: python -m src.main "What is phishing?"
    query_1 = "Which MITRE ATT&CK techniques are used by attackers to escalate their privileges within a network?"
    query_2 = "Which malware are launched by lazarus group?"
    query_3 = "I'm preparing a threat briefing on evasive maneuvers. Can you list out the techniques that fall under the 'Evasion' tactic so I can compare them with what we're currently monitoring?"
    if len(sys.argv) > 1:
        input_query = " ".join(sys.argv[1:])
    else:
        # Default query if none is provided
        input_query = query_3

    print(f"Executing agent with query: '{input_query}'")
    run_agent(input_query)
