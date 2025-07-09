from ..config import logger
from ..models.state import AgentState
from ..chains.chains import synthesis_chain


def synthesize_node(state: AgentState):
    """Generates the final answer for the user based on all gathered context."""
    logger.info("--- Executing Node: synthesizer ---")

    # Check if there is any context at all to synthesize
    # and not state.get('mcp_context')
    if not state.get('cypher_context') and not state.get('vector_context'):
        logger.warning(
            "Synthesizer: No context found from any source after all attempts.")
        final_answer = "Sorry, I could not find any information related to your question after several attempts."
    else:
        logger.info(
            "Synthesizer: Context found. Generating final synthesized answer.")
        final_answer = synthesis_chain.invoke({
            "question": state['original_question'],
            "cypher_context": str(state.get('cypher_context', 'No data was found from the structured query.')),
            "vector_context": str(state.get('vector_context', 'No data was found from the vector search.')),
            # "mcp_context": str(state.get('mcp_context', 'No data was found from the GraphDB Tool Agent.'))
        })

    return {"answer": final_answer}
