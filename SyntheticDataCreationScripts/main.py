from __future__ import annotations

import json
from pathlib import Path

from prismnet_synth.config import CONFIG, seed_everything
from prismnet_synth.faker_utils import build_fakers
from prismnet_synth.fonts import discover_fonts
from prismnet_synth.sample_generator import SyntheticSampleGenerator
from prismnet_synth.split_generator import generate_split_dataset
from prismnet_synth.splits import build_splits, discover_all_images


def main() -> None:
    seed_everything(CONFIG["seed"])

    dataset_root = CONFIG["dataset_root"]
    output_root = Path(CONFIG["output_root"])
    output_root.mkdir(parents=True, exist_ok=True)

    all_images = discover_all_images(dataset_root, CONFIG["image_exts"])
    print(f"[INFO] Found {len(all_images)} source images.")
    if len(all_images) == 0:
        raise RuntimeError("No images found. Check dataset_root and folder structure.")

    splits = build_splits(
        all_image_paths=all_images,
        train_val_list=CONFIG["train_val_list"],
        test_list=CONFIG["test_list"],
        val_ratio_from_trainval=CONFIG["val_ratio_from_trainval"],
        small_debug_source_count=CONFIG["small_debug_source_count"],
    )

    print(f"[INFO] Train sources: {len(splits['train'])}")
    print(f"[INFO] Val sources: {len(splits['val'])}")
    print(f"[INFO] Test sources: {len(splits['test'])}")
    print(f"[INFO] Small debug train sources: {len(splits['small_debug_train'])}")

    manifest_dir = output_root / "manifests"
    manifest_dir.mkdir(parents=True, exist_ok=True)
    for split_name, paths in splits.items():
        with open(manifest_dir / f"{split_name}_sources.txt", "w", encoding="utf-8") as handle:
            for path in paths:
                handle.write(str(path) + "\n")

    font_files = discover_fonts()
    fakers = build_fakers(CONFIG["seed"])
    generator = SyntheticSampleGenerator(CONFIG, font_files, fakers)

    split_to_variant_count = {
        "train": CONFIG["variants_per_source_train"],
        "val": CONFIG["variants_per_source_val"],
        "test": CONFIG["variants_per_source_test"],
        "small_debug_train": CONFIG["variants_per_source_small_debug"],
    }

    for split_name, source_paths in splits.items():
        generate_split_dataset(
            split_name=split_name,
            source_paths=source_paths,
            variants_per_source=split_to_variant_count[split_name],
            out_root=output_root,
            generator=generator,
        )

    with open(output_root / "generation_config.json", "w", encoding="utf-8") as handle:
        json.dump(CONFIG, handle, indent=2)

    print("\n[DONE] Synthetic data generation completed.")
    print(f"[DONE] Output saved to: {output_root.resolve()}")


if __name__ == "__main__":
    main()
