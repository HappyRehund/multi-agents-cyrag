import os
import logging
from langchain_openai import ChatOpenAI
from langchain_neo4j import Neo4jGraph
from dotenv import load_dotenv

# Muat variabel dari file .env
load_dotenv()

# --- Konfigurasi Kredensial dan Tracing ---
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
NEO4J_URI = os.environ.get("NEO4J_URI")
NEO4J_USERNAME = os.environ.get("NEO4J_USERNAME")
NEO4J_PASSWORD = os.environ.get("NEO4J_PASSWORD")

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "Multi-Agent CyKG"
os.environ["LANGCHAIN_API_KEY"] = os.environ.get("LANGCHAIN_API_KEY", "")
os.environ["LANGCHAIN_ENDPOINT"] = os.environ.get("LANGCHAIN_ENDPOINT", "")

# --- Konfigurasi Logging ---
log_dir = "./src/log"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(log_dir, 'multi_agent_cykg.log'), encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# --- Inisialisasi Objek Global ---
try:
    graph = Neo4jGraph()
    llm = ChatOpenAI(temperature=0, model_name="gpt-4o")
    DEFAULT_MAX_ITERATIONS = 3
    NEO4J_SCHEMA_RAW = graph.schema
    NEO4J_SCHEMA_ESCAPED_FOR_PROMPT = NEO4J_SCHEMA_RAW.replace(
        "{", "{{").replace("}", "}}")
    logger.info("Successfully initialized Neo4jGraph, LLM, and schema.")
except Exception as e:
    logger.error(f"Failed to initialize global objects: {e}", exc_info=True)
    graph = None
    llm = None
