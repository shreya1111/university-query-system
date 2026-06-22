"""
Department Router — loads mapping from departments.csv.
To extend: add rows to departments.csv; no code change needed.
"""
import os
import pandas as pd
from functools import lru_cache

_DATA_PATH = "data/training/departments.csv"
_FALLBACK   = "Help Desk"


@lru_cache(maxsize=1)
def _load_map() -> dict[str, str]:
    if not os.path.exists(_DATA_PATH):
        return {}
    df = pd.read_csv(_DATA_PATH)
    return dict(zip(df["intent"].str.strip(), df["department"].str.strip()))


def route_department(intent: str) -> str:
    """Return the responsible department for a given intent label."""
    return _load_map().get(intent.strip(), _FALLBACK)
