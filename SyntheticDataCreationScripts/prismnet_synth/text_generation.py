from __future__ import annotations

import random
from typing import Dict, List

import pandas as pd
from faker import Faker

from prismnet_synth.constants import (
    DEPARTMENTS,
    HOSPITAL_MIDDLES,
    HOSPITAL_PREFIXES,
    HOSPITAL_SUFFIXES,
    NON_PHI_MARKERS,
)
from prismnet_synth.faker_utils import choose_faker


def generate_hospital_name() -> str:
    pattern = random.choice([
        "{p} {m} {s}",
        "{p} {s}",
        "{p} {m} Center",
        "{p} {m} Institute",
        "{p} {m} Hospital",
        "{p} {m} and {m2} Center",
    ])
    name = pattern.format(
        p=random.choice(HOSPITAL_PREFIXES),
        m=random.choice(HOSPITAL_MIDDLES),
        m2=random.choice(HOSPITAL_MIDDLES),
        s=random.choice(HOSPITAL_SUFFIXES),
    )
    return " ".join(name.split())


def generate_patient_name(fake: Faker) -> str:
    first = fake.first_name()
    last = fake.last_name()
    middle = fake.first_name()

    patterns = [
        lambda: fake.name(),
        lambda: f"{last}, {first}",
        lambda: f"{first} {last}",
        lambda: f"{first} {middle} {last}",
        lambda: f"{first[0]}. {last}",
        lambda: f"{first} {middle[0]}. {last}",
    ]
    name = random.choice(patterns)()
    if random.random() < 0.30:
        name = name.upper()
    return name


def generate_patient_id() -> str:
    patterns = [
        lambda: f"MRN:{random.randint(100000, 999999)}",
        lambda: f"PAT ID:{random.randint(1000000, 9999999)}",
        lambda: f"ID {random.randint(10000, 99999)}-{random.randint(10, 99)}",
        lambda: f"ACC:{random.randint(1000, 9999)}-{random.randint(10000, 99999)}",
        lambda: f"XR-{random.randint(1000, 9999)}-{random.randint(10, 99)}",
        lambda: f"EXAM#{random.randint(100000, 999999)}",
    ]
    return random.choice(patterns)()


def generate_date_string(fake: Faker) -> str:
    dt = fake.date_between(start_date="-10y", end_date="today")
    formats = [
        "%m/%d/%Y",
        "%Y-%m-%d",
        "%d-%b-%Y",
        "%b %d %Y",
        "%d/%m/%Y",
        "%m-%d-%Y",
    ]
    return pd.Timestamp(dt).strftime(random.choice(formats))


def generate_time_string() -> str:
    hh = random.randint(0, 23)
    mm = random.randint(0, 59)
    ss = random.randint(0, 59)
    patterns = [
        f"{hh:02d}:{mm:02d}",
        f"{hh:02d}{mm:02d}",
        f"{hh:02d}:{mm:02d}:{ss:02d}",
        f"{hh:02d}.{mm:02d}",
    ]
    return random.choice(patterns)


def generate_physician_name(fake: Faker) -> str:
    last = fake.last_name()
    patterns = [
        lambda: f"Dr. {last}",
        lambda: f"Ref MD: {last}",
        lambda: f"Physician: Dr. {last}",
        lambda: f"Attending: Dr. {last}",
        lambda: f"Reported by Dr. {last}",
    ]
    return random.choice(patterns)()


def generate_age_sex() -> str:
    age = random.randint(1, 95)
    sex = random.choice(["M", "F"])
    patterns = [
        f"{age}Y {sex}",
        f"Age:{age} Sex:{sex}",
        f"{sex}/{age}",
        f"{age} {sex}",
    ]
    return random.choice(patterns)


def generate_nonphi_text() -> str:
    if random.random() < 0.7:
        return random.choice(NON_PHI_MARKERS)
    return random.choice([
        "CHEST",
        "PORTABLE CHEST",
        "PA CHEST",
        "AP UPRIGHT",
        "INSPIRATION",
        random.choice(DEPARTMENTS),
        f"Dept: {random.choice(DEPARTMENTS)}",
    ])


def generate_phi_pool(fakers: List[Faker]) -> Dict[str, str]:
    fake = choose_faker(fakers)
    return {
        "patient_name": generate_patient_name(fake),
        "patient_id": generate_patient_id(),
        "dob": f"DOB: {generate_date_string(fake)}",
        "exam_date": f"DATE: {generate_date_string(fake)}",
        "exam_time": f"TIME: {generate_time_string()}",
        "hospital_name": generate_hospital_name(),
        "physician_name": generate_physician_name(fake),
        "age_sex": generate_age_sex(),
    }
