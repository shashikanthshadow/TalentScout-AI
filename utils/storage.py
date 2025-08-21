# utils/storage.py
import pandas as pd
from typing import Dict, Any

def candidate_to_dataframe(candidate: Dict[str, Any]) -> pd.DataFrame:
    """
    Convert the candidate dict into a single-row DataFrame for easy display/export.
    """
    return pd.DataFrame([candidate])

def merge_tech_stack(existing: str, new_input: str) -> str:
    """
    Merge tech stack strings, de-duplicate items by comma, and return a clean string.
    """
    def split_clean(s: str):
        return [x.strip() for x in s.split(",") if x.strip()]

    items = set()
    for part in [existing or "", new_input or ""]:
        for t in split_clean(part):
            items.add(t)
    return ", ".join(sorted(items, key=lambda x: x.lower()))
