import asyncio
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from mcp_use import MCPAgent, MCPClient
from pathlib import Path


async def main():
    # Get the parent directory path
    os.environ["MCP_USE_ANONYMIZED_TELEMETRY"] = "false"
    parent_dir = Path(__file__).parent.parent
    script_dir = Path(__file__).parent
    # Construct path to .env file
    env_path = os.path.join(parent_dir, '.env')
    config_path = os.path.join(script_dir, "browser_mcp.json")
    # Muat variabel lingkungan
    load_dotenv(env_path)

    # Buat MCPClient dari file konfigurasi
    client = MCPClient.from_config_file(config_path)

    # Buat LLM (pastikan model mendukung pemanggilan alat)
    llm = ChatOpenAI(model="gpt-4o")

    strict_system_prompt = """
    You are a specialized cybersecurity assistant that answers questions ONLY by using the provided tools.
    You MUST NOT answer any questions from your own knowledge. Your only source of information is the connected database.

    Your thought process should be:
    1.  Analyze the user's question.
    2.  Formulate a SPARQL query to answer the question and execute it using the `read_graphdb_sparql` tool.
    3.  **CRITICAL REFLECTION STEP:** Examine the result from the tool.
        - If the result is an empty list `[]`, it signifies a potential mismatch between your query and the database schema.
        - **DO NOT STOP.** Your next step is to debug the query.
        - First, use the `get_graphdb_schema` tool to retrieve the correct schema.
        - Second, you MUST analyze your previous, failed SPARQL query in light of the new schema information. Identify the specific error (e.g., incorrect class name, wrong property URI, invalid path).
        - Third, construct an improved SPARQL query by correcting ONLY the identified error from your previous attempt. This is an iterative improvement, not a completely new query.
        - Execute the improved query. Repeat this reflection cycle if the result is still empty.
    4.  If after several attempts at correcting the query you still cannot find an answer, only then you must state that you could not find the information in the database.
    5.  NEVER provide an answer from memory or without a successful tool call.
    """

    query_1 = "can you tell me all the techniques under Initial Access?"
    query_2 = "What are the techniques used for Privilege Escalation?"
    query_3 = "Show 5 available tactics in the database"
    # Buat agen
    agent = MCPAgent(llm=llm, client=client, max_steps=30,
                     verbose=True,
                     system_prompt=strict_system_prompt
                     )

    # Jalankan kueri
    result = await agent.run(query_2)
    print(f"\nHasil: {result}")

if __name__ == "__main__":
    asyncio.run(main())
