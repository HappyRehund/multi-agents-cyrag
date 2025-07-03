# Multi-Agent RAG with a Cybersecurity Knowledge Graph

This project implements a sophisticated multi-agent system designed to answer complex cybersecurity questions. It leverages a Retrieval-Augmented Generation (RAG) pattern combined with multiple knowledge graphs (Neo4j and GraphDB) to provide accurate, context-aware answers.

The system uses a LangGraph-based agentic workflow to decide the best strategy for answering a user's query, whether it's querying for structured data using Cypher/SPARQL or performing a hybrid search over unstructured text.

## Core Components

1.  **Multi-Agent System (Python/LangGraph):** The primary application logic that orchestrates the entire workflow. It includes specialized agents for validating questions, querying databases, reflecting on results, and synthesizing final answers.
2.  **Neo4j Knowledge Graph:** A graph database storing structured cybersecurity data (e.g., from the MITRE ATT&CK framework), which is queried using the Cypher language.
3.  **GraphDB & MCP Server:** An Ontotext GraphDB instance is used for RDF-based knowledge. The agent communicates with this database using the Model Context Protocol (MCP) via a dedicated Node.js server.

## MCP Server Component

This project utilizes an external, open-source MCP server to connect the LangChain agent with the GraphDB instance.

-   **Repository:** [keonchennl/mcp-server-graphdb](https://github.com/keonchennl/mcp-server-graphdb)
-   **Description:** This server provides a read-only bridge to an Ontotext GraphDB repository, exposing tools like `sparqlQuery` and `listGraphs` to an MCP-compatible client.

The server code is included in the `mcp-server/mcp-graphdb/` directory of this project. Full credit for this component goes to its original author.

## Setup and Installation

1.  **Clone this repository:**
    ```sh
    git clone https://github.com/HappyRehund/multi-agents-cyrag.git
    cd multi-agents-rag-cykg
    ```

2.  **Set up the MCP Server:**
    The `mcp-server-graphdb` is included as a submodule or a direct copy. You need to install its dependencies.
    ```sh
    cd mcp-server/mcp-graphdb
    npm install
    npm run build
    cd ../..
    ```

3.  **Install Python Dependencies:**
    This project uses `uv` for package management.
    ```sh
    # Create and activate a virtual environment
    uv venv
    source .venv/bin/activate # or .\.venv\Scripts\activate on Windows

    # Install dependencies
    uv pip install -r requirements.txt
    ```

4.  **Configure Environment Variables:**
    Create a `.env` file in the root directory of the project and add the necessary credentials:
    ```env
    # OpenAI API Key
    OPENAI_API_KEY="sk-..."

    # LangSmith (Optional, for tracing)
    LANGCHAIN_API_KEY="..."
    LANGCHAIN_TRACING="true"
    LANGCHAIN_PROJECT="..."

    # Neo4j Credentials
    NEO4J_URI="bolt://localhost:7687"
    NEO4J_USERNAME="neo4j"
    NEO4J_PASSWORD="..."
    ```

## Usage

The primary logic is contained within the `notebook/multi-agents-final.ipynb` Jupyter notebook and the `mcp-test/mcp_example.py` script.

1.  **Run the Jupyter Notebook:**
    -   Launch Jupyter Lab or Jupyter Notebook.
    -   Open and run the cells in `notebook/multi-agents-final.ipynb` to interact with the Neo4j-based agent.

2.  **Run the MCP Agent Example:**
    -   This script demonstrates how to interact with the GraphDB instance via the MCP server.
    -   Run the script from the root directory:
        ```sh
        python mcp-test/mcp_example.py
