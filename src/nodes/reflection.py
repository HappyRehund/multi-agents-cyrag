from ..config import logger
from ..models.state import AgentState
from ..chains.chains import reflection_chain

def reflection_node(state: AgentState):
    """Reflects on the failed query and rephrases the question."""
    logger.info("--- Executing Node: reflection ---")
    original_question = state['original_question']
    failed_query = state['cypher_query']
    
    rephrased_result = reflection_chain.invoke({
        "original_question": original_question,
        "cypher_query": failed_query
    })
    
    new_question = rephrased_result.rephrased_question
    iteration_count = state['iteration_count'] + 1
    logger.info(f"Reflection: Rephrasing question to: '{new_question}'. New attempt: {iteration_count}.")
    
    return {"question": new_question, "iteration_count": iteration_count}