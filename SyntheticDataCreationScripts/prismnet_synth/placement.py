from __future__ import annotations

import random
from typing import Dict, List, Optional, Tuple


Box = Tuple[int, int, int, int]


def get_candidate_zones(width: int, height: int) -> Dict[str, Box]:
    return {
        "top_left": (0, 0, int(0.28 * width), int(0.18 * height)),
        "top_right": (int(0.72 * width), 0, width, int(0.18 * height)),
        "bottom_left": (0, int(0.82 * height), int(0.32 * width), height),
        "bottom_right": (int(0.68 * width), int(0.82 * height), width, height),
        "left_margin": (0, int(0.20 * height), int(0.18 * width), int(0.80 * height)),
        "right_margin": (int(0.82 * width), int(0.20 * height), width, int(0.80 * height)),
        "top_center": (int(0.35 * width), 0, int(0.65 * width), int(0.12 * height)),
    }


def boxes_intersect(box_a: Box, box_b: Box, pad: int = 4) -> bool:
    ax1, ay1, ax2, ay2 = box_a
    bx1, by1, bx2, by2 = box_b
    return not (ax2 + pad < bx1 or bx2 + pad < ax1 or ay2 + pad < by1 or by2 + pad < ay1)


def sample_position_for_text(
    zone_box: Box,
    text_box_size: Tuple[int, int],
    occupied_boxes: List[Box],
    max_tries: int = 50,
) -> Optional[Box]:
    zx1, zy1, zx2, zy2 = zone_box
    text_width, text_height = text_box_size
    if (zx2 - zx1) <= text_width or (zy2 - zy1) <= text_height:
        return None

    for _ in range(max_tries):
        x = random.randint(zx1, max(zx1, zx2 - text_width))
        y = random.randint(zy1, max(zy1, zy2 - text_height))
        candidate = (x, y, x + text_width, y + text_height)
        if not any(boxes_intersect(candidate, occupied) for occupied in occupied_boxes):
            return candidate
    return None
