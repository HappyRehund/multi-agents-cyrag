from ..config import llm
from ..prompts import guardrails_prompt, reflection_prompt, synthesis_prompt, entity_prompt
from ..models.schemas import GuardrailsOutput, RephrasedQuestion, Entities
from langchain_core.output_parsers.string import StrOutputParser

# Guardrails_chain
guardrails_chain = guardrails_prompt | llm.with_structured_output(GuardrailsOutput)

# Reflection chain
reflection_chain = reflection_prompt | llm.with_structured_output(RephrasedQuestion)

# Synthesis chain
synthesis_chain = synthesis_prompt | llm | StrOutputParser()

# Entity Extraction Chain
entity_chain = entity_prompt | llm.with_structured_output(Entities)