from __future__ import annotations

from src.config import Config
from src.llm import run_llm
from src.memory.graph_memory import graph_memory
from src.rag.hybrid_retriever import retrieve


async def writer_agent(state: dict) -> dict:
    topic = state.get("topic", "")
    keywords = state.get("keywords", [])
    clean_text = state.get("clean_text", "")

    graph_context = graph_memory.get_context(topic, top_k=Config.RETRIEVAL_GRAPH_K)
    retrieved_context = retrieve(topic, graph_context=graph_context, local_text=clean_text)

    prompt = f"""
You are a growth-focused tech founder writing on LinkedIn.
Write one high-performing LinkedIn post.

Topic:
{topic}

Keywords to naturally include:
{', '.join(keywords[:10])}

Research context:
{retrieved_context[:3500]}

Constraints:
- Only refer the content provided in the research context. (Don't use any outside knowledge.)
- First line must be a strong hook.
- Use short paragraphs and 3-5 bullet insights.
- Keep the tone credible and specific (no hype).
- Include one practical takeaway.
- End with one call-to-action question.
- Max length: 220 words.
"""

    post = await run_llm(prompt, cache=True)
    return {"linkedin_post": post, "retrieved_context": retrieved_context}
