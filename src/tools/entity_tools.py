from ..config import graph
from ..chains.chains import entity_chain
from langchain_neo4j.vectorstores.neo4j_vector import remove_lucene_chars

# Vector Search Tool
def generate_full_text_query(input: str) -> str:
    """
    Generate a full-text search query for a given input string.

    This function constructs a query string suitable for a full-text search.
    It processes the input string by splitting it into words and appending a
    similarity threshold (~2 changed characters) to each word, then combines
    them using the AND operator. Useful for mapping entities from user questions
    to database values, and allows for some misspelings.
    """
    full_text_query = ""
    words = [el for el in remove_lucene_chars(input).split() if el]
    for word in words[:-1]:
        full_text_query += f" {word}~2 AND"
    full_text_query += f" {words[-1]}~2"
    return full_text_query.strip()

def structured_retriever(question: str) -> str:
    """
    Collects the neighborhood of resources mentioned
    in the question
    """
    result = ""
    entities = entity_chain.invoke({"question": question})
    for entity in entities.names:
        response = graph.query(
            """CALL db.index.fulltext.queryNodes('entity', $query, {limit:2})
            YIELD node, score
            
            MATCH (node)-[r]-(neighbor)
            WHERE node.ns1__title IS NOT NULL AND neighbor.ns1__title IS NOT NULL
            
            RETURN CASE
                WHEN startNode(r) = node 
                THEN node.ns1__title + ' - ' + type(r) + ' -> ' + neighbor.ns1__title
                ELSE neighbor.ns1__title + ' - ' + type(r) + ' -> ' + node.ns1__title
            END AS output
            LIMIT 50
            """,
            {"query": generate_full_text_query(entity)},
        )
        result += "\n".join([el['output'] for el in response])
    return result