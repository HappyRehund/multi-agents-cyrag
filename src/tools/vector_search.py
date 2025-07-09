from langchain_openai import OpenAIEmbeddings
from langchain_neo4j.vectorstores.neo4j_vector import Neo4jVector
from .entity_tools import structured_retriever

vector_index = Neo4jVector.from_existing_graph(
    OpenAIEmbeddings(),
    search_type="hybrid",
    node_label="Resource",
    text_node_properties=["ns1__description"],
    embedding_node_property="embedding"
)

def query_vector_search(question: str):
    """
    Query the graph and vector index using a hybrid approach for vector similarity search.
    Use this for questions that require finding similar concepts or descriptions,
    like "Show me techniques related to 'SQL Injection'".
    """
    print(f"--- Executing Vector Search for: {question} ---")
    structured_data = structured_retriever(question)
    unstructured_data = [
        el.page_content for el in vector_index.similarity_search(question)]
    final_data = f"""Structured data:
    {structured_data}
    Unstructured data:
    {"#Resource ". join(unstructured_data)}
    """
    return final_data
