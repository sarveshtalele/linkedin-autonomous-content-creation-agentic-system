from __future__ import annotations

import asyncio
import hashlib
import json
from typing import Any

from langchain_ollama import OllamaLLM

from src.config import Config

_llm = OllamaLLM(model=Config.MODEL, temperature=0.3)
_prompt_cache: dict[str, str] = {}
_cache_lock = asyncio.Lock()


def _prompt_hash(prompt: str) -> str:
    return hashlib.sha1(prompt.encode("utf-8")).hexdigest()


async def run_llm(prompt: str, *, cache: bool = False) -> str:
    key = _prompt_hash(prompt)
    if cache:
        async with _cache_lock:
            cached = _prompt_cache.get(key)
        if cached is not None:
            return cached

    # `OllamaLLM.invoke` is sync in many setups; offload to worker thread.
    result = await asyncio.to_thread(_llm.invoke, prompt)
    text = str(result).strip()

    if cache:
        async with _cache_lock:
            _prompt_cache[key] = text

    return text


async def run_llm_json(prompt: str, fallback: dict[str, Any]) -> dict[str, Any]:
    raw = await run_llm(prompt, cache=False)

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        start = raw.find("{")
        end = raw.rfind("}")
        if start != -1 and end != -1 and end > start:
            try:
                return json.loads(raw[start : end + 1])
            except json.JSONDecodeError:
                pass

    return fallback
