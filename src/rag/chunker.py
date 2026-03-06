from __future__ import annotations

from src.config import Config


def chunk_text(text: str, size: int = Config.CHUNK_SIZE, overlap: int = Config.CHUNK_OVERLAP) -> list[str]:
    normalized = " ".join(text.split())
    if not normalized:
        return []

    chunks: list[str] = []
    start = 0
    text_len = len(normalized)

    while start < text_len:
        end = min(start + size, text_len)

        # Prefer ending on a word boundary to improve retrieval coherence.
        if end < text_len:
            boundary = normalized.rfind(" ", start, end)
            if boundary > start + (size // 2):
                end = boundary

        chunk = normalized[start:end].strip()
        if chunk:
            chunks.append(chunk)

        if end >= text_len:
            break

        start = max(0, end - overlap)

    return chunks
