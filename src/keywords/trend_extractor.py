from __future__ import annotations

import re
from collections import Counter

STOPWORDS = {
    "about",
    "after",
    "again",
    "being",
    "could",
    "first",
    "found",
    "from",
    "have",
    "into",
    "just",
    "more",
    "most",
    "other",
    "over",
    "should",
    "their",
    "there",
    "these",
    "those",
    "using",
    "with",
    "your",
}


def extract_keywords(text: str, top_k: int = 12) -> list[str]:
    words = re.findall(r"\b[A-Za-z][A-Za-z0-9-]{3,}\b", text.lower())
    filtered = [word for word in words if word not in STOPWORDS]
    counts = Counter(filtered)
    return [word for word, _ in counts.most_common(top_k)]
