from ..config import logger
from ..models.state import AgentState
from ..tools.vector_search import query_vector_search

def vector_search_node(state: AgentState):
    """Calls the vector search tool and populates the state."""
    logger.info("--- Executing Node: vector_search ---")
    question = state['question']
    try:
        vector_context = query_vector_search(question)
        logger.info("Vector search completed successfully.")
        logger.info(f"Vector search context found:\n{vector_context}")
        return {"vector_context": vector_context}
    except Exception as e:
        logger.error(f"Vector search failed: {e}")
        return {"vector_context": f"Error during vector search: {e}"}