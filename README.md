
# Multi-Agent RAG with a Cybersecurity Knowledge Graph


## Core Components

- Multi-Agent System (Python/LangGraph): The primary application logic that orchestrates the entire workflow. It includes specialized agents for validating questions, querying databases, reflecting on results, and synthesizing final answers
- Neo4j Knowledge Graph: A graph database storing structured cybersecurity data (e.g., from the MITRE ATT&CK framework), which is queried using the Cypher language.


## Setup and Installation

How to use

Make sure that you already have uv installed on your desktop, if not then here's the installation guide : https://docs.astral.sh/uv/getting-started/installation/ 

```bash
  git clone <this-project>
  cd <this-project>
  uv sync
```

After that, you can use the kernel of .venv to run these python notebook project.

```bash
  source .venv/bin/activate
```

Make sure again that the .env file is filled !!!
```bash
OPENAI_API_KEY=
LANGCHAIN_API_KEY=
LANGCHAIN_TRACING_V2=
LANGCHAIN_ENDPOINT=
LANGCHAIN_PROJECT=
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=    
NEO4J_PASSWORD_ICS=
NEO4J_DATABASE=

NEO4J_AURA=
NEO4J_AURA_USERNAME=
NEO4J_AURA_PASSWORD=
NEO4J_AURA_DATABASE=

GRAPHDB_PASSWORD=
GRAPHDB_USERNAME=
```
## Features

- **multi-agents-with-log.ipynb**: This workflow combines Neo4j (Cypher) database graph-based search, vector search, log analysis, and automatic reflection to generate comprehensive answers to user questions regarding threats, attack techniques, mitigation, and suspicious activity in the system.

- **multi-agents-without-log.ipynb** : This workflow combines Neo4j (Cypher) database graph-based search, vector search, and automatic reflection (without log analysis) to generate comprehensive answers to user questions related to attack techniques, mitigation, and threat intelligence.

- **neo4j-cypher-query.ipynb** : MITRE ATT&CK-based cybersecurity knowledge search and analysis using Cypher query on Neo4j database.

- **neo4j-log.ipynb** : Hybrid search that combines system log analysis and Neo4j graph knowledge for user activity investigation.

- **neo4j-log.ipynb** : Neo4j vector and graph-based cybersecurity knowledge retrieval