from __future__ import annotations

import re

from src.memory.graph_memory import GraphChunk, graph_memory
from src.rag.chunker import chunk_text
from src.rag.vector_store import add_chunks


def _clean_text(text: str) -> str:
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


async def cleaning_agent(state: dict) -> dict:
    raw_data = state.get("raw_data", [])

    all_clean_docs: list[str] = []
    graph_chunks: list[GraphChunk] = []

    for item in raw_data:
        source = item.get("source", "unknown")
        text = _clean_text(item.get("text", ""))
        if not text:
            continue

        all_clean_docs.append(f"Source: {source}\n{text}")

        chunks = chunk_text(text)
        if not chunks:
            continue

        add_chunks(chunks, source=source)
        graph_chunks.extend(GraphChunk(source=source, text=chunk) for chunk in chunks)

    graph_memory.add_chunks(graph_chunks)

    clean_text = "\n\n".join(all_clean_docs)
    return {"clean_text": clean_text}
