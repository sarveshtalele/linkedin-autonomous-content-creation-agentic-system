from __future__ import annotations

import io
from pathlib import Path
from typing import Union

import pytesseract
from PIL import Image

FileLike = Union[str, Path, bytes]


def load_image(source: FileLike) -> str:
    if isinstance(source, (str, Path)):
        image = Image.open(str(source))
    else:
        image = Image.open(io.BytesIO(source))

    return pytesseract.image_to_string(image).strip()
