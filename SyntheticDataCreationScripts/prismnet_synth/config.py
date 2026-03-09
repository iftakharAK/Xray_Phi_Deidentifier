from __future__ import annotations

import random
from typing import Dict, Any

import numpy as np


CONFIG: Dict[str, Any] = {
    "dataset_root": r"archive",
    "train_val_list": r"train_val_list.txt",
    "test_list": r"test_list.txt",
    "output_root": r"prismnet_synthetic_output",
    "val_ratio_from_trainval": 0.15,
    "small_debug_source_count": 100,
    "variants_per_source_train": 6,
    "variants_per_source_val": 2,
    "variants_per_source_test": 2,
    "variants_per_source_small_debug": 2,
    "min_phi_instances": 2,
    "max_phi_instances": 6,
    "min_nonphi_instances": 1,
    "max_nonphi_instances": 3,
    "budgets": [0.25, 0.50, 0.75, 1.00],
    "policies": ["hospital_A", "hospital_B", "hospital_C"],
    "seed": 42,
    "image_exts": [".png", ".jpg", ".jpeg"],
    "resize_to": None,
    "font_size_min_frac": 0.018,
    "font_size_max_frac": 0.035,
    "max_placement_tries": 50,
    "save_category_masks": True,
}


def seed_everything(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
