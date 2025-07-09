# import os
# import asyncio
# from pathlib import Path

# os.environ["MCP_USE_ANONYMIZED_TELEMETRY"] = "false"
# os.environ["PYTHONIOENCODING"] = "utf-8"

# from mcp_use import MCPAgent, MCPClient
# from ..config import llm
# from ..prompts import mcp_system_prompt

# # Inisialisasi klien sekali saja untuk efisiensi
# _mcp_client = None
# def get_mcp_client():
#     """Menginisialisasi dan mengembalikan MCPClient."""
#     global _mcp_client
#     if _mcp_client is None:
#         # Tentukan path ke file konfigurasi MCP
#         # Asumsi file config ada di dalam folder 'mcp-test' di root project
#         project_root = Path(__file__).parent.parent.parent
#         config_path = project_root / "mcp-test" / "browser_mcp.json"

#         if not config_path.exists():
#             raise FileNotFoundError(
#                 f"MCP config file not found at {config_path}")

#         _mcp_client = MCPClient.from_config_file(str(config_path))
#     return _mcp_client


# def run_mcp_agent(question: str) -> str:
#     """
#     Menjalankan MCPAgent dengan pertanyaan yang diberikan dan mengembalikan hasilnya.
#     """
#     client = get_mcp_client()

#     # Buat agen MCP
#     # Menggunakan LLM dari config utama untuk konsistensi
#     agent = MCPAgent(
#         llm=llm,
#         client=client,
#         max_steps=5,
#         verbose=False,
#         system_prompt=mcp_system_prompt
#     )

#     # Jalankan kueri secara asynchronous
#     # asyncio.run() digunakan untuk menjalankan fungsi async dari konteks sync
#     result = asyncio.run(agent.run(question))
#     return result
