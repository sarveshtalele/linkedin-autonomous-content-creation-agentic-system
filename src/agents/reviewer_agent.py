from __future__ import annotations

from src.llm import run_llm_json


def _clamp_score(value: int) -> int:
    return max(0, min(100, value))


async def reviewer_agent(state: dict) -> dict:
    post = state.get("linkedin_post", "")

    prompt = f"""
You are a strict LinkedIn content reviewer.
Evaluate the post below and return JSON only.

Required JSON schema:
{{
  "credibility": 0-100,
  "clarity": 0-100,
  "engagement": 0-100,
  "seo": 0-100,
  "accuracy": 0-100,
  "final_score": 0-100,
  "feedback": "short paragraph with specific fixes"
}}

Post:
{post}
"""

    fallback = {
        "credibility": 75,
        "clarity": 75,
        "engagement": 75,
        "seo": 75,
        "accuracy": 75,
        "final_score": 75,
        "feedback": "Improve specificity, shorten long sentences, and include one concrete proof point.",
    }

    review = await run_llm_json(prompt, fallback=fallback)
    score = _clamp_score(int(review.get("final_score", 75)))
    feedback = str(review.get("feedback", fallback["feedback"]))

    return {"review": feedback, "score": score, "review_payload": review}
