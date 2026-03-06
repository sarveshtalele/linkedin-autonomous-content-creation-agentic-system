from __future__ import annotations

from pathlib import Path
from typing import Union

import fitz

FileLike = Union[str, Path, bytes]


def load_pdf(source: FileLike) -> str:
    if isinstance(source, (str, Path)):
        doc = fitz.open(str(source))
    else:
        doc = fitz.open(stream=source, filetype="pdf")

    texts: list[str] = []
    with doc:
        for page in doc:
            texts.append(page.get_text())

    return "\n".join(texts).strip()
