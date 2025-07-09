from pydantic import BaseModel, Field
from typing import List, Literal

class GuardrailsOutput(BaseModel):
    decision: Literal["relevant", "irrelevant"] = Field(
        description="Is the question relevant to cybersecurity, MITRE ATT&CK, tactics, malware, or threat actors?")
    
class RephrasedQuestion(BaseModel):
    rephrased_question: str = Field(description="A rephrased, more specific version of the original question to improve Cypher query generation.")
    
class Entities(BaseModel):
    """Identifying information about resources."""

    names: List[str] = Field(
        ...,
        description="All the tactics, techniques, or software entities that "
        "appear in the text",
    )