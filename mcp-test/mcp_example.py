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
    load_dotenv(env_path)

    # Create MCP Client from config
    client = MCPClient.from_config_file(config_path)

    llm = ChatOpenAI(model="gpt-4o")

    strict_system_prompt = """
    You are a specialized cybersecurity assistant. You MUST answer questions ONLY by using the provided tools. Your only source of information is the knowledge graph accessed via tools.

    Your thought process MUST be:
        1.  **Analyze the user's question** to understand the core intent.
        2.  **Select the best tool.** Start with `full_text_search` for simple keyword matching. If that fails or the question is complex, use `text_to_sparql` to convert the question into a precise SPARQL query.
        3.  **Execute the tool.**
        4.  **Analyze the result.**
            - If the result is a **validation error** (like a Pydantic error), it means you provided the wrong arguments to the tool. Read the error message carefully. DO NOT use the same tool with the exact same arguments again. Correct the arguments and retry. For tools requiring `ctx`, DO NOT provide a value for it; the system handles it.
            - If the result is **empty or "not found"**, the information may not exist, or your query was too narrow. Try rephrasing your input for the tool, perhaps using a broader term.
            - If you are stuck in a loop of failures, only then you must state that you could not find the information.
        5.  **NEVER provide an answer from memory.** All answers must be based on tool results.
    """

    query_1 = "can you tell me all the techniques under Initial Access?"
    query_2 = "What are the techniques used for Privilege Escalation?"
    query_3 = "Show 5 available tactics in the database"
    query_4 = "Which MITRE ATT&CK techniques are used by attackers to escalate their privileges within a network?"
    
    # Buat agen
    agent = MCPAgent(llm=llm, client=client, max_steps=30, verbose=True, system_prompt=strict_system_prompt)

    # Jalankan kueri
    result = await agent.run(query_4)
    print(f"\nHasil: {result}")

if __name__ == "__main__":
    asyncio.run(main())
