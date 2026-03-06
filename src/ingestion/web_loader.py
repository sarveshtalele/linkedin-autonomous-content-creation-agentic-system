from __future__ import annotations

from bs4 import BeautifulSoup
import requests

from src.config import Config


def load_web(url: str) -> str:
    response = requests.get(url, timeout=Config.WEB_TIMEOUT_SECONDS)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    text = soup.get_text(separator=" ")
    return " ".join(text.split())
