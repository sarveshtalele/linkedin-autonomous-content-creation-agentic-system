from __future__ import annotations

from src.keywords.trend_extractor import extract_keywords


async def keyword_agent(state: dict) -> dict:
    text = state.get("clean_text", "")
    keywords = extract_keywords(text)
    return {"keywords": keywords}
