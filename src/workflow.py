from langgraph.graph import StateGraph, END
from .models.state import AgentState
from .nodes import (
    guardrails_node,
    vector_search_node,
    cypher_query_node,
    reflection_node,
    synthesize_node
    # graphdb_mcp_node
)
from .config import logger

# Edge Logic

# graphdb_mcp_agent
def decide_relevance(state: AgentState):
    if state.get('is_relevant'):
        logger.info(
            "Decision: Question is relevant, proceeding to vector Search.")
        return ["vector_agent", "cypher_agent"]
    else:
        logger.info("Decision: Question is irrelevant, ending execution.")
        return END


def decide_after_cypher(state: AgentState):
    """Decides whether to synthesize an answer or reflect and retry."""
    if state.get("cypher_context"):
        logger.info("Decision: Cypher has context. Proceeding to synthesizer.")
        return "synthesizer"

    if state.get("iteration_count", 0) < state.get("max_iterations", 3):
        logger.warning(
            "Decision: Cypher has no context. Proceeding to reflection.")
        return "reflection"
    else:
        logger.error(
            "Decision: Max retries reached. Proceeding to synthesizer.")
        return "synthesizer"

# Graph Definition


def build_workflow():
    workflow = StateGraph(AgentState)

    # Add Nodes
    workflow.add_node("guardrails", guardrails_node)
    workflow.add_node("vector_agent", vector_search_node)
    workflow.add_node("cypher_agent", cypher_query_node)
    # workflow.add_node("graphdb_mcp_agent", graphdb_mcp_node)
    workflow.add_node("reflection", reflection_node)
    workflow.add_node("synthesizer", synthesize_node)

    # Define Edges
    workflow.set_entry_point("guardrails")
    workflow.add_conditional_edges("guardrails", decide_relevance, {
                                   "vector_agent": "vector_agent",
                                   "cypher_agent": "cypher_agent",
                                #    "graphdb_mcp_agent": "graphdb_mcp_agent",
                                   END: END})
    workflow.add_edge("vector_agent", "synthesizer")
    # workflow.add_edge("graphdb_mcp_agent", "synthesizer")
    workflow.add_conditional_edges("cypher_agent", decide_after_cypher, {
                                   "synthesizer": "synthesizer", "reflection": "reflection"})
    workflow.add_edge("reflection", "cypher_agent")
    workflow.add_edge("synthesizer", END)

    # Compile and return the graph
    return workflow.compile()


app = build_workflow()
