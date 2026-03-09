from __future__ import annotations

import random

import numpy as np
from PIL import Image, ImageEnhance, ImageFilter


def apply_global_augmentations(img: Image.Image) -> Image.Image:
    if random.random() < 0.35:
        radius = random.uniform(0.3, 1.2)
        img = img.filter(ImageFilter.GaussianBlur(radius=radius))

    if random.random() < 0.35:
        img = ImageEnhance.Contrast(img).enhance(random.uniform(0.92, 1.08))

    if random.random() < 0.25:
        img = ImageEnhance.Brightness(img).enhance(random.uniform(0.96, 1.04))

    if random.random() < 0.25:
        arr = np.array(img).astype(np.float32)
        noise = np.random.normal(0, random.uniform(1.0, 4.0), size=arr.shape)
        arr = np.clip(arr + noise, 0, 255).astype(np.uint8)
        img = Image.fromarray(arr)

    return img
