# config.py
import os


class Config:
    DOCUMENTS_DIR = "resumes"
    COLLECTION_NAME = "CVs"
    PERSISTENT_DIR = "data/chromadb"
    # Embedding
    MODEL_NAME = "text-embedding-3-small"
    OPENAI_KEY = "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"
    # Completamento
    ### ollama
    # LLM_MODEL = "llama3.2"  # "deepseek-r1:1.5b"  # "llama3.2" #  "deepseek-r1:1.5b"
    # LLM_MODEL_LOW = "llama3.2"  # "deepseek-r1:1.5b"  # "llama3.2" #  "deepseek-r1:1.5b"
    # AI_API_URL = "http://localhost:11434/v1"
    # AI_API_KEY = "ollama"
    ### openai
    LLM_MODEL = "gpt-4o"
    LLM_MODEL_LOW = "gpt-4o-mini"
    AI_API_URL = "https://api.openai.com/v1/"
    AI_API_KEY = "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"
