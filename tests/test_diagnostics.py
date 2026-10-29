import pandas as pd

from neo_missingness.diagnostics import missingness_summary


def test_missingness_summary_counts_and_percentages():
    df = pd.DataFrame({"diameter": [1.0, None, None], "e": [0.1, 0.2, 0.3]})
    result = missingness_summary(df)

    assert result.loc["diameter", "missing_count"] == 2
    assert result.loc["diameter", "missing_percent"] == 66.667
    assert result.loc["e", "missing_count"] == 0


def test_missingness_summary_empty_dataframe():
    result = missingness_summary(pd.DataFrame())
    assert list(result.columns) == [
        "missing_count",
        "missing_percent",
        "non_missing_count",
    ]
