from typing_extensions import TypedDict, Annotated
from typing import List, Optional
from langgraph.graph import add_messages

class AgentState(TypedDict):
    question: str
    original_question: str
    is_relevant: bool
    vector_context: Optional[str]
    cypher_context: Optional[List[dict]]
    # mcp_context: Optional[str]
    answer: Optional[str]
    cypher_query: Optional[str]
    error: Optional[str]
    messages: Annotated[list, add_messages]
    iteration_count: int
    max_iterations: int