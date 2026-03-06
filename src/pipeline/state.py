from __future__ import annotations

from typing import Any, TypedDict


class AgentState(TypedDict, total=False):
    topic: str
    raw_data: list[dict[str, str]]
    clean_text: str
    keywords: list[str]
    linkedin_post: str
    retrieved_context: str
    review: str
    review_payload: dict[str, Any]
    score: int
    rewrite_round: int
