from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List

import pandas as pd
from tqdm import tqdm

from prismnet_synth.sample_generator import SyntheticSampleGenerator


def generate_split_dataset(
    split_name: str,
    source_paths: List[Path],
    variants_per_source: int,
    out_root: Path,
    generator: SyntheticSampleGenerator,
) -> None:
    out_split_dir = out_root / split_name
    out_split_dir.mkdir(parents=True, exist_ok=True)

    metadata_file = out_split_dir / "metadata.jsonl"
    flat_csv_file = out_split_dir / "annotations_flat.csv"

    if metadata_file.exists():
        metadata_file.unlink()
    if flat_csv_file.exists():
        flat_csv_file.unlink()

    total_samples = len(source_paths) * variants_per_source
    progress_bar = tqdm(total=total_samples, desc=f"Generating {split_name}")
    flat_rows = []

    with open(metadata_file, "w", encoding="utf-8") as metadata_handle:
        for src_path in source_paths:
            stem = src_path.stem

            for variant_idx in range(variants_per_source):
                sample_id = f"{stem}_syn_{variant_idx:02d}"
                meta = generator.generate_one_sample(
                    source_path=src_path,
                    out_split_dir=out_split_dir,
                    sample_id=sample_id,
                    split_name=split_name,
                )

                metadata_handle.write(json.dumps(meta) + "\n")

                for instance in meta["instances"]:
                    flat_rows.append({
                        "sample_id": meta["sample_id"],
                        "split": meta["split"],
                        "source_image_name": meta["source_image_name"],
                        "synthetic_image_path": meta["synthetic_image_path"],
                        "instance_id": instance["instance_id"],
                        "text": instance["text"],
                        "category": instance["category"],
                        "is_phi": instance["is_phi"],
                        "x1": instance["bbox"][0],
                        "y1": instance["bbox"][1],
                        "x2": instance["bbox"][2],
                        "y2": instance["bbox"][3],
                        "x": instance["bbox_xywh"][0],
                        "y": instance["bbox_xywh"][1],
                        "w": instance["bbox_xywh"][2],
                        "h": instance["bbox_xywh"][3],
                        "font_size": instance["font_size"],
                        "intensity": instance["intensity"],
                        "opacity": instance["opacity"],
                        "angle": instance["angle"],
                        "zone": instance["zone"],
                        "all_phi_mask_path": meta["mask_paths"]["all_phi"],
                        "non_phi_mask_path": meta["mask_paths"]["non_phi_text"],
                    })

                progress_bar.update(1)

    progress_bar.close()

    if flat_rows:
        df = pd.DataFrame(flat_rows)
        df.to_csv(flat_csv_file, index=False)
