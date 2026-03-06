from __future__ import annotations

import os
from pathlib import Path


class Config:
    MODEL = os.getenv("OLLAMA_MODEL", "phi3")
    EMBEDDING_MODEL = os.getenv("OLLAMA_EMBEDDING_MODEL", "nomic-embed-text")

    PROJECT_ROOT = Path(__file__).resolve().parents[1]
    OUTPUT_DIR = PROJECT_ROOT / "outputs"
    VECTOR_DB = OUTPUT_DIR / "vector_db"
    DATA_DIR = OUTPUT_DIR / "data"

    MAX_INGEST_WORKERS = int(os.getenv("MAX_INGEST_WORKERS", "8"))
    WEB_TIMEOUT_SECONDS = int(os.getenv("WEB_TIMEOUT_SECONDS", "10"))

    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "900"))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "120"))

    RETRIEVAL_TOP_K = int(os.getenv("RETRIEVAL_TOP_K", "6"))
    RETRIEVAL_GRAPH_K = int(os.getenv("RETRIEVAL_GRAPH_K", "3"))

    REVIEW_SCORE_THRESHOLD = int(os.getenv("REVIEW_SCORE_THRESHOLD", "90"))
    MAX_REWRITE_ROUNDS = int(os.getenv("MAX_REWRITE_ROUNDS", "2"))


Config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
Config.VECTOR_DB.mkdir(parents=True, exist_ok=True)
Config.DATA_DIR.mkdir(parents=True, exist_ok=True)
