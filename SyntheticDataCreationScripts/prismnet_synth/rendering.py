from __future__ import annotations

from typing import Dict, List

import numpy as np
from PIL import Image, ImageDraw

from prismnet_synth.fonts import load_font


def render_text_patch(text: str, style: Dict, font_files: List[str]) -> Image.Image:
    font = load_font(font_files, style["font_size"])

    temp_img = Image.new("L", (2000, 400), 0)
    temp_draw = ImageDraw.Draw(temp_img)
    bbox = temp_draw.textbbox((0, 0), text, font=font)

    text_width = max(1, bbox[2] - bbox[0] + 4)
    text_height = max(1, bbox[3] - bbox[1] + 4)

    patch = Image.new("L", (text_width, text_height), 0)
    patch_draw = ImageDraw.Draw(patch)
    patch_draw.text((2, 2), text, fill=int(255 * style["opacity"]), font=font)

    if style["angle"] != 0:
        patch = patch.rotate(style["angle"], expand=True, fillcolor=0)

    return patch


def paste_text_with_mask(
    base_img: Image.Image,
    text_patch: Image.Image,
    x: int,
    y: int,
    intensity: int,
    global_mask: np.ndarray,
    category_mask: np.ndarray,
) -> None:
    patch_np = np.array(text_patch).astype(np.float32) / 255.0
    if patch_np.max() <= 0:
        return

    base_np = np.array(base_img).astype(np.float32)

    patch_h, patch_w = patch_np.shape
    image_h, image_w = base_np.shape

    x2 = min(image_w, x + patch_w)
    y2 = min(image_h, y + patch_h)
    x1 = max(0, x)
    y1 = max(0, y)

    px1 = max(0, -x)
    py1 = max(0, -y)
    px2 = px1 + (x2 - x1)
    py2 = py1 + (y2 - y1)

    if x2 <= x1 or y2 <= y1:
        return

    alpha = patch_np[py1:py2, px1:px2]
    region = base_np[y1:y2, x1:x2]

    text_val = np.full_like(region, fill_value=intensity, dtype=np.float32)
    out = region * (1 - alpha) + text_val * alpha
    base_np[y1:y2, x1:x2] = np.clip(out, 0, 255)

    binary_alpha = (alpha > 0.05).astype(np.uint8)
    global_mask[y1:y2, x1:x2] = np.maximum(global_mask[y1:y2, x1:x2], binary_alpha)
    category_mask[y1:y2, x1:x2] = np.maximum(category_mask[y1:y2, x1:x2], binary_alpha)

    base_img.paste(Image.fromarray(base_np.astype(np.uint8)))
