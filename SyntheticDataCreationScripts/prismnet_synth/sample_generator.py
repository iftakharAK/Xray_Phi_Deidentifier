from __future__ import annotations

import random
from pathlib import Path
from typing import Dict, List

import numpy as np
from PIL import Image

from prismnet_synth.augmentations import apply_global_augmentations
from prismnet_synth.constants import PHI_CATEGORIES
from prismnet_synth.placement import get_candidate_zones, sample_position_for_text
from prismnet_synth.rendering import paste_text_with_mask, render_text_patch
from prismnet_synth.styles import random_text_style
from prismnet_synth.targets import (
    build_budget_mask,
    build_budget_policy_mask,
    build_policy_mask,
)
from prismnet_synth.text_generation import generate_nonphi_text, generate_phi_pool


class SyntheticSampleGenerator:
    def __init__(self, config: Dict, font_files: List[str], fakers: List) -> None:
        self.config = config
        self.font_files = font_files
        self.fakers = fakers

    def generate_one_sample(
        self,
        source_path: Path,
        out_split_dir: Path,
        sample_id: str,
        split_name: str,
    ) -> Dict:
        img = Image.open(source_path).convert("L")

        if self.config["resize_to"] is not None:
            img = img.resize(self.config["resize_to"], Image.BILINEAR)

        width, height = img.size
        zones = get_candidate_zones(width, height)
        syn_img = img.copy()

        all_phi_mask = np.zeros((height, width), dtype=np.uint8)
        non_phi_mask = np.zeros((height, width), dtype=np.uint8)
        category_masks = {cat: np.zeros((height, width), dtype=np.uint8) for cat in PHI_CATEGORIES}

        instances = []
        occupied_boxes = []
        phi_pool = generate_phi_pool(self.fakers)

        n_phi = random.randint(self.config["min_phi_instances"], self.config["max_phi_instances"])
        n_nonphi = random.randint(self.config["min_nonphi_instances"], self.config["max_nonphi_instances"])
        chosen_phi_categories = random.sample(PHI_CATEGORIES, k=min(n_phi, len(PHI_CATEGORIES)))

        for category in chosen_phi_categories:
            text = phi_pool[category]
            style = random_text_style(
                image_height=height,
                min_frac=self.config["font_size_min_frac"],
                max_frac=self.config["font_size_max_frac"],
            )
            patch = render_text_patch(text, style, self.font_files)
            patch_w, patch_h = patch.size

            zone_name = random.choice(list(zones.keys()))
            placement = sample_position_for_text(
                zones[zone_name],
                (patch_w, patch_h),
                occupied_boxes,
                max_tries=self.config["max_placement_tries"],
            )
            if placement is None:
                continue

            x1, y1, x2, y2 = placement
            paste_text_with_mask(
                base_img=syn_img,
                text_patch=patch,
                x=x1,
                y=y1,
                intensity=style["intensity"],
                global_mask=all_phi_mask,
                category_mask=category_masks[category],
            )

            occupied_boxes.append((x1, y1, x2, y2))
            instances.append({
                "instance_id": len(instances),
                "text": text,
                "category": category,
                "is_phi": True,
                "bbox": [int(x1), int(y1), int(x2), int(y2)],
                "bbox_xywh": [int(x1), int(y1), int(x2 - x1), int(y2 - y1)],
                "font_size": int(style["font_size"]),
                "intensity": int(style["intensity"]),
                "opacity": float(style["opacity"]),
                "angle": float(style["angle"]),
                "zone": zone_name,
            })

        for _ in range(n_nonphi):
            text = generate_nonphi_text()
            style = random_text_style(
                image_height=height,
                min_frac=self.config["font_size_min_frac"],
                max_frac=self.config["font_size_max_frac"],
            )
            style["intensity"] = max(150, style["intensity"] - random.randint(0, 20))

            patch = render_text_patch(text, style, self.font_files)
            patch_w, patch_h = patch.size

            zone_name = random.choice(list(zones.keys()))
            placement = sample_position_for_text(
                zones[zone_name],
                (patch_w, patch_h),
                occupied_boxes,
                max_tries=self.config["max_placement_tries"],
            )
            if placement is None:
                continue

            x1, y1, x2, y2 = placement
            dummy_nonphi_category_mask = np.zeros((height, width), dtype=np.uint8)

            paste_text_with_mask(
                base_img=syn_img,
                text_patch=patch,
                x=x1,
                y=y1,
                intensity=style["intensity"],
                global_mask=non_phi_mask,
                category_mask=dummy_nonphi_category_mask,
            )

            occupied_boxes.append((x1, y1, x2, y2))
            instances.append({
                "instance_id": len(instances),
                "text": text,
                "category": "non_phi_marker",
                "is_phi": False,
                "bbox": [int(x1), int(y1), int(x2), int(y2)],
                "bbox_xywh": [int(x1), int(y1), int(x2 - x1), int(y2 - y1)],
                "font_size": int(style["font_size"]),
                "intensity": int(style["intensity"]),
                "opacity": float(style["opacity"]),
                "angle": float(style["angle"]),
                "zone": zone_name,
            })

        syn_img = apply_global_augmentations(syn_img)

        image_dir = out_split_dir / "images"
        image_dir.mkdir(parents=True, exist_ok=True)
        image_path = image_dir / f"{sample_id}.png"
        syn_img.save(image_path)

        mask_root = out_split_dir / "masks"
        all_phi_dir = mask_root / "all_phi"
        non_phi_dir = mask_root / "non_phi_text"
        all_phi_dir.mkdir(parents=True, exist_ok=True)
        non_phi_dir.mkdir(parents=True, exist_ok=True)

        all_phi_path = all_phi_dir / f"{sample_id}.png"
        non_phi_path = non_phi_dir / f"{sample_id}.png"
        Image.fromarray((all_phi_mask * 255).astype(np.uint8)).save(all_phi_path)
        Image.fromarray((non_phi_mask * 255).astype(np.uint8)).save(non_phi_path)

        category_mask_paths = {}
        if self.config["save_category_masks"]:
            for category, category_mask in category_masks.items():
                if category_mask.sum() > 0:
                    category_dir = mask_root / "categories" / category
                    category_dir.mkdir(parents=True, exist_ok=True)
                    category_path = category_dir / f"{sample_id}.png"
                    Image.fromarray((category_mask * 255).astype(np.uint8)).save(category_path)
                    category_mask_paths[category] = str(category_path)

        budget_mask_paths = {}
        budget_root = out_split_dir / "targets" / "budgets"
        for budget in self.config["budgets"]:
            budget_mask = build_budget_mask(category_masks, budget)
            budget_dir = budget_root / f"budget_{str(budget).replace('.', '_')}"
            budget_dir.mkdir(parents=True, exist_ok=True)
            budget_path = budget_dir / f"{sample_id}.png"
            Image.fromarray((budget_mask * 255).astype(np.uint8)).save(budget_path)
            budget_mask_paths[str(budget)] = str(budget_path)

        policy_mask_paths = {}
        policy_root = out_split_dir / "targets" / "policies"
        for policy in self.config["policies"]:
            policy_mask = build_policy_mask(category_masks, policy)
            policy_dir = policy_root / policy
            policy_dir.mkdir(parents=True, exist_ok=True)
            policy_path = policy_dir / f"{sample_id}.png"
            Image.fromarray((policy_mask * 255).astype(np.uint8)).save(policy_path)
            policy_mask_paths[policy] = str(policy_path)

        combined_mask_paths = {}
        combined_root = out_split_dir / "targets" / "budget_policy_combined"
        for budget in self.config["budgets"]:
            budget_key = str(budget)
            combined_mask_paths[budget_key] = {}
            for policy in self.config["policies"]:
                combined_mask = build_budget_policy_mask(category_masks, budget, policy)
                combo_dir = combined_root / f"budget_{str(budget).replace('.', '_')}" / policy
                combo_dir.mkdir(parents=True, exist_ok=True)
                combo_path = combo_dir / f"{sample_id}.png"
                Image.fromarray((combined_mask * 255).astype(np.uint8)).save(combo_path)
                combined_mask_paths[budget_key][policy] = str(combo_path)

        phi_instance_count = sum(1 for item in instances if item["is_phi"])
        non_phi_instance_count = sum(1 for item in instances if not item["is_phi"])

        return {
            "sample_id": sample_id,
            "split": split_name,
            "source_image_name": source_path.name,
            "source_image_path": str(source_path),
            "synthetic_image_path": str(image_path),
            "width": width,
            "height": height,
            "phi_instance_count": phi_instance_count,
            "non_phi_instance_count": non_phi_instance_count,
            "instances": instances,
            "mask_paths": {
                "all_phi": str(all_phi_path),
                "non_phi_text": str(non_phi_path),
                "categories": category_mask_paths,
                "budgets": budget_mask_paths,
                "policies": policy_mask_paths,
                "budget_policy_combined": combined_mask_paths,
            },
            "budgets": self.config["budgets"],
            "policies": self.config["policies"],
        }
