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
    Always start by thinking about which tool to use. If the initial tools don't provide enough information about the database schema, use tools like `listGraphs` to understand what data is available.
    If after using the tools you cannot find an answer, you must state that you could not find the information in the database.
    NEVER provide an answer from memory.
    """
    # Buat agen
    agent = MCPAgent(llm=llm, client=client, max_steps=30,
                     verbose=True, system_prompt=strict_system_prompt)

    # Jalankan kueri
    result = await agent.run("What techniques are used for credential dumping on Windows systems?")
    print(f"\nHasil: {result}")

if __name__ == "__main__":
    asyncio.run(main())
