from ..config import logger
from ..models.state import AgentState
from ..tools.cypher_tools import query_cypher

def cypher_query_node(state: AgentState):
    """Calls the cypher search tool and populates the state."""
    logger.info(
        f"--- Executing Node: cypher_agent (Attempt: {state.get('iteration_count', 1)}) ---")
    question = state['question']
    try:
        cypher_result = query_cypher(question)
        context = cypher_result.get("context", [])
        generated_query = cypher_result.get("query", "")

        if not context:
            logger.warning(
                f"Cypher agent: No results found for query: {generated_query}")
        else:
            logger.info(
                f"Cypher agent: Found context. Query: {generated_query}")

        return {
            "cypher_query": generated_query,
            "cypher_context": context
        }
    except Exception as e:
        logger.error(f"Cypher agent failed: {e}", exc_info=True)
        return {
            "error": f"Gagal menjalankan query Cypher: {e}",
            "cypher_context": [],
            "cypher_query": "Failed to generate Cypher query due to an error."
        }