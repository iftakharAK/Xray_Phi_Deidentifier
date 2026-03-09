from __future__ import annotations

from typing import Dict

import numpy as np

from prismnet_synth.constants import BUDGET_CATEGORY_MAP, POLICY_CATEGORY_MAP


def build_budget_mask(category_masks: Dict[str, np.ndarray], budget: float) -> np.ndarray:
    categories = BUDGET_CATEGORY_MAP[budget]
    sample_mask = next(iter(category_masks.values()))
    out = np.zeros_like(sample_mask, dtype=np.uint8)
    for category in categories:
        if category in category_masks:
            out = np.maximum(out, category_masks[category])
    return out


def build_policy_mask(category_masks: Dict[str, np.ndarray], policy_name: str) -> np.ndarray:
    categories = POLICY_CATEGORY_MAP[policy_name]
    sample_mask = next(iter(category_masks.values()))
    out = np.zeros_like(sample_mask, dtype=np.uint8)
    for category in categories:
        if category in category_masks:
            out = np.maximum(out, category_masks[category])
    return out


def build_budget_policy_mask(
    category_masks: Dict[str, np.ndarray],
    budget: float,
    policy_name: str,
) -> np.ndarray:
    budget_categories = set(BUDGET_CATEGORY_MAP[budget])
    policy_categories = set(POLICY_CATEGORY_MAP[policy_name])
    active_categories = budget_categories.intersection(policy_categories)

    sample_mask = next(iter(category_masks.values()))
    out = np.zeros_like(sample_mask, dtype=np.uint8)

    for category in active_categories:
        if category in category_masks:
            out = np.maximum(out, category_masks[category])

    return out
