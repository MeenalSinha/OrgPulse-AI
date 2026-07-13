"""Shared fixture loader for mock-mode connectors."""
import json
from pathlib import Path
from functools import lru_cache

FIXTURES_DIR = Path(__file__).resolve().parent.parent / "data" / "fixtures"


@lru_cache(maxsize=None)
def load(name: str):
    with open(FIXTURES_DIR / f"{name}.json") as f:
        return json.load(f)
