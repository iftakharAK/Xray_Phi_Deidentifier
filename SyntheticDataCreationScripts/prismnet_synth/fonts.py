from __future__ import annotations

import random
from pathlib import Path
from typing import List

from PIL import ImageFont


def discover_fonts() -> List[str]:
    possible_dirs = [
        r"C:\Windows\Fonts",
        "/usr/share/fonts",
        "/usr/local/share/fonts",
        str(Path.home() / ".fonts"),
    ]
    font_files = []
    for directory in possible_dirs:
        path = Path(directory)
        if path.exists():
            for ext in ["*.ttf", "*.otf", "*.ttc"]:
                font_files.extend([str(p) for p in path.rglob(ext)])

    good_keywords = ["arial", "helvetica", "cour", "dejavu", "liberation", "noto", "sans"]
    selected = []
    for font_file in font_files:
        lowered = font_file.lower()
        if any(keyword in lowered for keyword in good_keywords):
            selected.append(font_file)

    return selected[:200] if selected else []


def load_font(font_files: List[str], font_size: int):
    if font_files:
        font_path = random.choice(font_files)
        try:
            return ImageFont.truetype(font_path, font_size)
        except Exception:
            pass
    return ImageFont.load_default()
