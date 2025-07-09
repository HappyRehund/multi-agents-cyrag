from .config import NEO4J_SCHEMA_ESCAPED_FOR_PROMPT
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate

# Entity Extraction Prompt
entity_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are extracting attack techniques, tactics, malware, mitigations entities from the text.",
        ),
        (
            "human",
            "Use the given format to extract information from the following "
            "input: {question}",
        ),
    ]
)

# Cypher Generation Prompt
cypher_generation_template = """
You are an expert Neo4j Cypher translator who converts English to Cypher based on the Neo4j Schema provided, following the instructions below:
        1. Generate Cypher query compatible ONLY for Neo4j Version 5
        2. Do not use EXISTS, SIZE, HAVING keywords in the cypher. Use alias when using the WITH keyword
        3. Use only Nodes and relationships mentioned in the schema
        5. Never use relationships that are not mentioned in the given schema
        6. For all node labels and relationship types, add namespace prefix `ns0__` before the actual label or relationship type. E.g., `MATCH (n:ns0__NodeLabel)-[:ns0__RelationshipType]->(m:ns0__NodeLabel)`.
        7. Node properties with `created`, `description`, `identifier`, `modified`, `title` and `version`, add prefix `ns1__` instead. E.g., `MATCH (n:ns0__NodeLabel) RETURN n.ns1__title AS Title`.
        8. Always do a case-insensitive and fuzzy search for any properties related search. Eg: to search for a Tactic, use `toLower(Tactic.ns1__title) contains 'persistence'`.
        9. Always assign a meaningful name to every node and relationship in the MATCH clause
        10. Never return components not explicitly named in the MATCH clause.
        11. In the RETURN clause, include all named components (nodes, relationships, or properties) to ensure consistency and understanding.
        12. Always return all the nodes used in the MATCH clause to provide complete information to the user.
        13. When counting distinct items that come from an `OPTIONAL MATCH`, prefer to `collect()` them first and then use `size()` on the collected list to avoid warnings about null values. For example, instead of `count(DISTINCT optional_item)`, use `WITH main_node, collect(DISTINCT optional_item) AS items` and then in the `RETURN` clause use `size(items) AS itemCount`.
        14. To create unique pairs of nodes for comparison (e.g., for similarity calculations), use the `elementId()` function instead of the deprecated `id()` function. For example: `WHERE elementId(node1) < elementId(node2)`.
        15. use `toLower()` function to ensure case-insensitive comparisons for string properties.

Schema:
{schema}

Note: 
Do not include any explanations or apologies in your responses.
Do not respond to any questions that might ask anything other than
for you to construct a Cypher statement. Do not include any text except
the generated Cypher statement. Make sure the direction of the relationship is
correct in your queries. Make sure you alias both entities and relationships
properly. Do not run any queries that would add to or delete from
the database. Make sure to alias all statements that follow as with
statement

In Cypher, you can alias nodes and relationships, but not entire pattern matches using AS directly after a MATCH clause.If you want to alias entire patterns or results of more complex expressions, that should be done in the RETURN clause, not the MATCH clause.
If you want to include any specific properties from these nodes in your results, you can add them to your RETURN statement.

Examples : 

1. Which techniques are commonly used by at least 3 different threat groups?
MATCH (g:ns0__Group)-[:ns0__usesTechnique]->(t:ns0__Technique)
WITH t, count(g) as groupCount
WHERE groupCount >= 3
MATCH (g:ns0__Group)-[:ns0__usesTechnique]->(t)
RETURN t.ns1__title as CommonTechnique, t.ns1__identifier as TechniqueID, 
       groupCount as NumberOfGroups,
       collect(g.ns1__title) as Groups
ORDER BY groupCount DESC

2. Find tactical areas where we have the most significant defensive gaps by identifying tactics that have many techniques but few mitigations, and rank them by coverage percentage!

MATCH (tactic:ns0__Tactic)<-[:ns0__accomplishesTactic]-(technique:ns0__Technique)
WITH tactic, collect(technique) as techniques, count(technique) as techniqueCount
UNWIND techniques as technique
OPTIONAL MATCH (mitigation:ns0__Mitigation)-[:ns0__preventsTechnique]->(technique)
WITH tactic, techniqueCount, technique, count(mitigation) > 0 as hasMitigation

WITH tactic, techniqueCount, 
     sum(CASE WHEN hasMitigation THEN 1 ELSE 0 END) as mitigatedTechniques,
     collect(CASE WHEN NOT hasMitigation THEN technique.ns1__title ELSE NULL END) as unmitigatedTechniques

WITH tactic, techniqueCount, mitigatedTechniques,
     [x IN unmitigatedTechniques WHERE x IS NOT NULL] as filteredUnmitigatedTechniques,
     (toFloat(mitigatedTechniques) / techniqueCount * 100) as coveragePercentage

RETURN tactic.ns1__title as Tactic,
       tactic.ns1__identifier as TacticID,
       techniqueCount as TotalTechniques,
       mitigatedTechniques as MitigatedTechniques,
       techniqueCount - mitigatedTechniques as UnmitigatedTechniqueCount,
       toInteger(coveragePercentage) as CoveragePercentage,
       CASE 
         WHEN coveragePercentage < 30 THEN "CRITICAL" 
         WHEN coveragePercentage < 60 THEN "HIGH" 
         WHEN coveragePercentage < 80 THEN "MEDIUM"
         ELSE "LOW"
       END as RiskLevel,
       filteredUnmitigatedTechniques as UnmitigatedTechniques
ORDER BY coveragePercentage ASC, techniqueCount DESC


The question is:
{question}

"""

cyper_generation_prompt = PromptTemplate(
    template=cypher_generation_template,
    input_variables=["schema", "question"]
)

#  QA Generation Prompt
qa_template = """
You are an assistant that takes the results from a Neo4j Cypher query and forms a human-readable response. The query results section contains the results of a Cypher query that was generated based on a user's natural language question. The provided information is authoritative; you must never question it or use your internal knowledge to alter it. Make the answer sound like a response to the question.
Final answer should be easily readable and structured.
Query Results:
{context}

Question: {question}
If the provided information is empty, respond by stating that you don't know the answer. Empty information is indicated by: []
If the information is not empty, you must provide an answer using the results. If the question involves a time duration, assume the query results are in units of days unless specified otherwise.
Never state that you lack sufficient information if data is present in the query results. Always utilize the data provided.
Helpful Answer:
"""

qa_generation_prompt = PromptTemplate(
    template=qa_template,
    input_variables=["context", "question"]
)

# MCP Agent System Prompt
# mcp_system_prompt = """
#     You are a specialized cybersecurity assistant that answers questions ONLY by using the provided tools.
#     You MUST NOT answer any questions from your own knowledge. Your only source of information is the connected database.
#     Always start by thinking about which tool to use. If the initial tools don't provide enough information about the database schema, use tools like `listGraphs` to understand what data is available.
#     If after using the tools you cannot find an answer, you must state that you could not find the information in the database.
#     NEVER provide an answer from memory.
#     """

# Guardrails Prompt
guardrails_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a gatekeeper for a cybersecurity Q&A system. Your task is to determine if a user's question is related to cybersecurity topics like MITRE ATT&CK, attack techniques, malware, threat groups, or mitigations. Only allow relevant questions to pass."),
    ("human", "Question: {question}"),
])

# Reflection Prompt
reflection_prompt = ChatPromptTemplate.from_messages([
    ("system", f"""You are a query correction expert. A Cypher query returned no results.
Your task is to rephrase the user's question to be more specific and likely to succeed with the given Neo4j graph schema.
Analyze the failed query and the schema. For example, if the question was too broad, make it more specific. If it used terms not in the schema, suggest alternatives.
Do not just repeat the question. Provide a meaningful improvement.

Schema:
{NEO4J_SCHEMA_ESCAPED_FOR_PROMPT}"""),
    ("human", "Original Question: {original_question}\n\nFailed Cypher Query:\n{cypher_query}\n\nRephrase the question to improve the chances of getting a result."),
])

# Synthesis Prompt
synthesis_prompt = ChatPromptTemplate.from_template("""You are an expert cybersecurity assistant tasked with synthesizing information from multiple sources to answer a user's question.
Your job is to generate a comprehensive final answer. Follow these steps:
1.  Review the "Original Question" from the user.
2.  Review the "Context from Cypher Query," which is structured data retrieved from the knowledge graph.
3.  Review the "Context from Vector Search," which contains both structured relationships and unstructured text.
4.  Clearly present the key findings from each source. If a source provided no data, state that.
5.  Critically analyze how well the combined information answers the "Original Question." If the information is incomplete or doesn't fully address the user's query, explain the potential reasons.
6.  Construct a final, well-structured answer that includes the retrieved data and your analysis.

The provided context is authoritative. Do not add any information not present in the results.
If all contexts are empty after all attempts, state that you could not find an answer.

Original Question: {question}

Context from Cypher Query:
{cypher_context}

Context from Vector Search:
{vector_context}


Synthesized Answer:
""")

# Context from GraphDB Tool Agent:
# {mcp_context}

# 4.  Review the "Context from GraphDB Tool Agent," which provides answers from a tool-using agent.
