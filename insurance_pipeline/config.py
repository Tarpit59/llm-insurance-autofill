import os
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"

load_dotenv(ENV_PATH)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
CONVERTAPI_API_KEY = os.getenv("CONVERTAPI_API_KEY")

CHUNK_SIZE = 400
CHUNK_OVERLAP = 100

OPENROUTER_LLM_FIELD_UNDERSTANDING_MODEL = "deepseek/deepseek-r1-0528-qwen3-8b:free"
GROQ_LLM_QA_MODEL = "deepseek-r1-distill-llama-70b"

EMBEDDINGS_MODEL_NAME = "models/embedding-001"
COHERE_RERANK_MODEL = "rerank-english-v3.0"

PINECONE_INDEX_NAME = 'langcha'

