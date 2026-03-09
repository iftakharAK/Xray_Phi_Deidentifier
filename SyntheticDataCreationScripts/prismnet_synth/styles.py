from __future__ import annotations

import random
from typing import Dict


def random_text_style(image_height: int, min_frac: float, max_frac: float) -> Dict[str, float]:
    font_size = random.randint(
        int(min_frac * image_height),
        int(max_frac * image_height),
    )
    intensity = random.randint(175, 255)
    opacity = random.uniform(0.70, 1.0)
    angle = random.uniform(-4, 4) if random.random() < 0.35 else 0.0

    return {
        "font_size": font_size,
        "intensity": intensity,
        "opacity": opacity,
        "angle": angle,
    }
