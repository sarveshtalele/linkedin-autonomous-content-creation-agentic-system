from __future__ import annotations

import hashlib
from pathlib import Path

from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings

from src.config import Config

try:
    from langchain_chroma import Chroma
except ImportError:  # pragma: no cover - compatibility fallback
    from langchain_community.vectorstores import Chroma

_embeddings = OllamaEmbeddings(model=Config.EMBEDDING_MODEL)
_vector_db = Chroma(
    collection_name="linkedin_memory",
    embedding_function=_embeddings,
    persist_directory=str(Config.VECTOR_DB),
)


def _chunk_id(text: str, source: str) -> str:
    return hashlib.sha1(f"{source}:{text}".encode("utf-8")).hexdigest()


def add_chunks(chunks: list[str], source: str) -> None:
    if not chunks:
        return

    documents = [Document(page_content=chunk, metadata={"source": source}) for chunk in chunks]
    ids = [_chunk_id(chunk, source) for chunk in chunks]

    # Ensure idempotent writes across reruns.
    try:
        _vector_db.delete(ids=ids)
    except Exception:  # pragma: no cover - best-effort cleanup
        pass
    _vector_db.add_documents(documents=documents, ids=ids)


def similarity_search(query: str, k: int = Config.RETRIEVAL_TOP_K) -> list[Document]:
    return _vector_db.similarity_search(query, k=k)


def reset_vector_store() -> None:
    # Best-effort cleanup used only from UI reset button.
    directory = Path(Config.VECTOR_DB)
    for path in directory.glob("*"):
        if path.is_file():
            path.unlink(missing_ok=True)
