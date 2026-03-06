from __future__ import annotations

import math
import re
from collections import defaultdict

from src.config import Config
from src.rag.vector_store import similarity_search

_TOKEN_RE = re.compile(r"\b[a-zA-Z0-9_]{3,}\b")


def _tokenize(text: str) -> set[str]:
    return set(token.lower() for token in _TOKEN_RE.findall(text))


def _lexical_score(query_tokens: set[str], text: str) -> float:
    tokens = _tokenize(text)
    if not tokens:
        return 0.0
    overlap = len(tokens & query_tokens)
    return overlap / math.sqrt(len(tokens))


def retrieve(query: str, graph_context: str = "", local_text: str = "", k: int = Config.RETRIEVAL_TOP_K) -> str:
    query_tokens = _tokenize(query)
    rank_scores: defaultdict[str, float] = defaultdict(float)

    docs = similarity_search(query, k=k)
    for rank, doc in enumerate(docs):
        text = doc.page_content.strip()
        if not text:
            continue

        # Reciprocal rank favors top vector hits.
        rank_scores[text] += 1.0 / (rank + 1)
        rank_scores[text] += 0.35 * _lexical_score(query_tokens, text)

    if graph_context.strip():
        for block in graph_context.split("\n\n"):
            block = block.strip()
            if block:
                rank_scores[block] += 0.25 + 0.5 * _lexical_score(query_tokens, block)

    if local_text.strip():
        # Cheap fallback when vector retrieval is sparse.
        snippets = [piece.strip() for piece in local_text.split(". ") if piece.strip()]
        for snippet in snippets[:30]:
            lexical = _lexical_score(query_tokens, snippet)
            if lexical > 0:
                rank_scores[snippet] += 0.4 * lexical

    ranked = sorted(rank_scores.items(), key=lambda item: item[1], reverse=True)
    selected = [text for text, _ in ranked[:k]]
    return "\n\n".join(selected)
