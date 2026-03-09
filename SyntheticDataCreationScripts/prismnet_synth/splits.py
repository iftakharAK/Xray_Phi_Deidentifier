from __future__ import annotations

import random
from pathlib import Path
from typing import Dict, List


def discover_all_images(dataset_root: str, exts: List[str]) -> List[Path]:
    root = Path(dataset_root)
    all_files = []
    for path in root.rglob("*"):
        if path.is_file() and path.suffix.lower() in exts:
            if "images" in [part.lower() for part in path.parts]:
                all_files.append(path)
    return sorted(all_files)


def read_split_list(file_path: str) -> List[str]:
    path = Path(file_path)
    if not path.exists():
        return []
    with open(path, "r", encoding="utf-8") as handle:
        return [line.strip() for line in handle if line.strip()]


def build_splits(
    all_image_paths: List[Path],
    train_val_list: str,
    test_list: str,
    val_ratio_from_trainval: float,
    small_debug_source_count: int,
) -> Dict[str, List[Path]]:
    image_name_to_path = {path.name: path for path in all_image_paths}

    train_val_names = read_split_list(train_val_list)
    test_names = read_split_list(test_list)

    if train_val_names and test_names:
        train_val_paths = [image_name_to_path[name] for name in train_val_names if name in image_name_to_path]
        test_paths = [image_name_to_path[name] for name in test_names if name in image_name_to_path]

        random.shuffle(train_val_paths)
        val_size = int(len(train_val_paths) * val_ratio_from_trainval)
        val_paths = train_val_paths[:val_size]
        train_paths = train_val_paths[val_size:]
    else:
        paths = all_image_paths[:]
        random.shuffle(paths)
        total = len(paths)
        test_size = int(total * 0.20)
        val_size = int(total * 0.10)
        test_paths = paths[:test_size]
        val_paths = paths[test_size:test_size + val_size]
        train_paths = paths[test_size + val_size:]

    small_debug_paths = train_paths[:min(small_debug_source_count, len(train_paths))]

    return {
        "train": train_paths,
        "val": val_paths,
        "test": test_paths,
        "small_debug_train": small_debug_paths,
    }
