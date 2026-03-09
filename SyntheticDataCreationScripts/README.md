# PRISM-Net Synthetic Chest X-ray Data Generator

This project reorganizes the original single-file pipeline into a modular package that is easier to maintain, test, and extend.

##  structure

- `main.py`  
  Entry point that seeds randomness, builds splits, initializes resources, and launches generation.

- `prismnet_synth/config.py`  
  Central configuration and reproducibility utilities.

- `prismnet_synth/constants.py`  
  PHI categories, budget mappings, policy mappings, and text vocabularies.

- `prismnet_synth/faker_utils.py`  
  Faker initialization and locale selection.

- `prismnet_synth/text_generation.py`  
  Synthetic PHI / non-PHI content generation.

- `prismnet_synth/fonts.py`  
  Font discovery and fallback loading.

- `prismnet_synth/splits.py`  
  Dataset discovery and train/val/test split construction.

- `prismnet_synth/placement.py`  
  Chest X-ray overlay zones and collision-aware placement.

- `prismnet_synth/styles.py`  
  Rendering style sampling such as font size, intensity, opacity, and angle.

- `prismnet_synth/rendering.py`  
  Text patch rendering and mask-aware compositing.

- `prismnet_synth/augmentations.py`  
  Post-render image degradations and augmentations.

- `prismnet_synth/targets.py`  
  Budget-conditioned, policy-conditioned, and combined target mask builders.

- `prismnet_synth/sample_generator.py`  
  Per-image sample generation and saving of masks / metadata.

- `prismnet_synth/split_generator.py`  
  Full split generation and flat annotation export.

## Run

```bash
python main.py
```
