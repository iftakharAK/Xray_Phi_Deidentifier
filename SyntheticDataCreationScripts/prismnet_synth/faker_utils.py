from __future__ import annotations

import random
from typing import List

from faker import Faker

FAKER_LOCALES = ["en_US", "en_GB", "en_CA", "en_IN"]


def build_fakers(seed: int) -> List[Faker]:
    fakers = [Faker(loc) for loc in FAKER_LOCALES]
    for fk in fakers:
        fk.seed_instance(seed)
    return fakers


def choose_faker(fakers: List[Faker]) -> Faker:
    return random.choice(fakers)
