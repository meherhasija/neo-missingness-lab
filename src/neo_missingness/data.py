"""Data-loading helpers.

The downloader will be added after API parameters and snapshot metadata
are validated against the current official JPL documentation.
"""

from pathlib import Path

import pandas as pd


def load_csv(path: str | Path) -> pd.DataFrame:
    """Load a CSV snapshot from a local path."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")
    return pd.read_csv(path)
