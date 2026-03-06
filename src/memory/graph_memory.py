from __future__ import annotations

import hashlib
import math
import re
from dataclasses import dataclass

import networkx as nx


_TOKEN_RE = re.compile(r"\b[a-zA-Z0-9_]{3,}\b")


def _tokenize(text: str) -> set[str]:
    return set(token.lower() for token in _TOKEN_RE.findall(text))


def _node_id(source: str, index: int, text: str) -> str:
    return hashlib.sha1(f"{source}:{index}:{text}".encode("utf-8")).hexdigest()


@dataclass
class GraphChunk:
    source: str
    text: str


class GraphMemory:
    def __init__(self) -> None:
        self.graph = nx.Graph()

    def add_chunks(self, chunks: list[GraphChunk]) -> None:
        prev_id: str | None = None
        for idx, chunk in enumerate(chunks):
            node_id = _node_id(chunk.source, idx, chunk.text)
            tokens = _tokenize(chunk.text)
            self.graph.add_node(
                node_id,
                text=chunk.text,
                source=chunk.source,
                tokens=tokens,
            )

            # Temporal adjacency keeps graph sparse and fast.
            if prev_id is not None:
                self.graph.add_edge(prev_id, node_id, weight=1.0)
            prev_id = node_id

    def get_context(self, query: str, top_k: int = 3) -> str:
        if self.graph.number_of_nodes() == 0:
            return ""

        query_tokens = _tokenize(query)
        if not query_tokens:
            return ""

        scored: list[tuple[float, str]] = []
        for node_id, attrs in self.graph.nodes(data=True):
            tokens = attrs.get("tokens") or set()
            overlap = len(tokens & query_tokens)
            if overlap == 0:
                continue

            score = overlap / math.sqrt(max(1, len(tokens)))
            scored.append((score, node_id))

        scored.sort(key=lambda item: item[0], reverse=True)
        selected_nodes = [node_id for _, node_id in scored[:top_k]]
        selected_texts = [self.graph.nodes[node_id]["text"] for node_id in selected_nodes]
        return "\n\n".join(selected_texts)

    def clear(self) -> None:
        self.graph.clear()


graph_memory = GraphMemory()
