from ..config import logger
from ..models.state import AgentState
from ..chains.chains import guardrails_chain

def guardrails_node(state: AgentState):
    """Decides if the question is relevant."""
    logger.info("--- Executing Node: guardrails ---")
    question = state['question']
    result = guardrails_chain.invoke({"question": question})
    if result.decision == "irrelevant":
        logger.warning(
            f"Guardrails: Irrelevant question detected -> '{question}'")
        return {"is_relevant": False, "answer": "Sorry, I can only answer questions related to cybersecurity and MITRE ATT&CK."}
    else:
        logger.info("Guardrails: Question is relevant.")
        return {"is_relevant": True}
