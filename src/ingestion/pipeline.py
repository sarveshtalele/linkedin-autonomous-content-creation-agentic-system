from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

from src.config import Config

from .image_loader import load_image
from .pdf_loader import load_pdf
from .text_loader import load_text
from .web_loader import load_web


SUPPORTED_IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".bmp"}


def _read_upload(file_obj: Any) -> tuple[str, bytes]:
    name = getattr(file_obj, "name", "uploaded_file")
    if hasattr(file_obj, "seek"):
        file_obj.seek(0)
    content = file_obj.read() if hasattr(file_obj, "read") else bytes(file_obj)
    if hasattr(file_obj, "seek"):
        file_obj.seek(0)
    return name, content


def _load_single_file(file_input: Any) -> dict[str, str]:
    if isinstance(file_input, (str, Path)):
        source_name = str(file_input)
        ext = Path(source_name).suffix.lower()
        payload: str | bytes = source_name
    else:
        source_name, content = _read_upload(file_input)
        ext = Path(source_name).suffix.lower()
        payload = content

    if ext == ".pdf":
        text = load_pdf(payload)
    elif ext in SUPPORTED_IMAGE_EXTENSIONS:
        text = load_image(payload)
    else:
        text = load_text(payload)

    return {"source": source_name, "text": text}


def _load_single_url(url: str) -> dict[str, str]:
    text = load_web(url)
    return {"source": url, "text": text}


def ingest(files: list[Any] | None, urls: list[str] | None) -> list[dict[str, str]]:
    files = files or []
    urls = [u.strip() for u in (urls or []) if u and u.strip()]

    dataset: list[dict[str, str]] = []
    futures = []

    with ThreadPoolExecutor(max_workers=Config.MAX_INGEST_WORKERS) as executor:
        for file_input in files:
            futures.append(executor.submit(_load_single_file, file_input))

        for url in urls:
            futures.append(executor.submit(_load_single_url, url))

        for future in as_completed(futures):
            try:
                item = future.result()
                if item.get("text"):
                    dataset.append(item)
            except Exception as exc:  # pragma: no cover - non-fatal ingestion branch
                dataset.append({"source": "ingestion_error", "text": f"Ingestion failed: {exc}"})

    return dataset
