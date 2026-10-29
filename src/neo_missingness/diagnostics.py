"""Small, reusable missingness diagnostics."""

from __future__ import annotations

import pandas as pd


def missingness_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Return missing counts and percentages for each column."""
    if df.empty:
        return pd.DataFrame(
            columns=["missing_count", "missing_percent", "non_missing_count"]
        )

    missing_count = df.isna().sum()
    return pd.DataFrame(
        {
            "missing_count": missing_count,
            "missing_percent": (missing_count / len(df) * 100).round(3),
            "non_missing_count": df.notna().sum(),
        }
    ).sort_values("missing_percent", ascending=False)
