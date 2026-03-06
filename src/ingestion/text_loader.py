from __future__ import annotations

from pathlib import Path
from typing import Union

FileLike = Union[str, Path, bytes]


def load_text(source: FileLike) -> str:
    if isinstance(source, (str, Path)):
        with open(source, "r", encoding="utf-8", errors="ignore") as file:
            return file.read().strip()

    return source.decode("utf-8", errors="ignore").strip()
