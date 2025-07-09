# from ..config import logger
# from ..models.state import AgentState
# from ..tools.mcp_tool import run_mcp_agent

# def graphdb_mcp_node(state: AgentState):
#     """
#     Menjalankan GraphDB MCP Agent untuk menjawab pertanyaan.
#     """
#     logger.info("--- Executing Node: graphdb_mcp ---")
#     question = state['question']

#     try:
#         # Panggil tool MCP
#         mcp_result = run_mcp_agent(question)
#         logger.info("GraphDB MCP node executed successfully.")
#         return {"mcp_context": mcp_result}
#     except Exception as e:
#         logger.error(f"GraphDB MCP node failed: {e}", exc_info=True)
#         return {"mcp_context": f"Error during GraphDB MCP execution: {e}"}
