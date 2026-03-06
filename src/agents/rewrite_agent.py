from __future__ import annotations

from src.llm import run_llm


async def rewrite_agent(state: dict) -> dict:
    post = state.get("linkedin_post", "")
    feedback = state.get("review", "")
    keywords = state.get("keywords", [])
    rewrite_round = int(state.get("rewrite_round", 0)) + 1

    prompt = f"""
Rewrite this LinkedIn post based on reviewer feedback.

Feedback:
{feedback}

Keywords to preserve naturally:
{', '.join(keywords[:10])}

Original post:
{post}

Constraints:
- Keep hook + bullets + CTA.
- Improve credibility and clarity first.
- Max 220 words.
"""

    improved = await run_llm(prompt, cache=False)
    return {"linkedin_post": improved, "rewrite_round": rewrite_round}
