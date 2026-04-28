"""Polars-based analysis layer for Steam case price data.

This module is the bridge between the SQLite store (written by storage.py)
and the downstream wavelet analysis. Its only job is to turn rows in the
`case_prices` table into:

    1. A long-format Polars DataFrame for querying (`load_prices`), and
    2. A 1D numpy array of prices for one case, which is what wavelet
       transforms actually consume (`get_signal`).

Uniform-hourly resampling -- the step wavelet transforms REALLY want -- is
stubbed here (`resample_uniform_hourly`) and deferred to a later milestone.

Design commitment: long format in storage, long format in Polars, collapse
to 1D numpy only at the wavelet boundary. See the plan document for the
reasons (storage shape, unstable case set, honest missing-data, cheap
pivot-on-demand).
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import polars as pl
import sqlite3

from storage import DB_PATH


def load_prices(db_path: Path = DB_PATH) -> tuple[pl.DataFrame, np.ndarray]:
    """Load the entire `case_prices` table into a long-format Polars DataFrame.

    Returns a DataFrame with the following schema:
        - name    : pl.Utf8
        - date    : pl.Datetime(time_zone="UTC")
        - price   : pl.Float64
        - volume  : pl.Int64

    The returned DataFrame is sorted by (name, date). Downstream callers may
    assume this ordering.

    Args:
        db_path: Location of the SQLite file. Defaults to storage.DB_PATH.

    Returns:
        A long-format Polars DataFrame. One row per (case_name, timestamp) pair.
        A numpy array that holds the timestamps for future visuals

    Contract notes:
      - SQLite stores `date` as ISO-8601 TEXT (see storage.py schema).
        Polars will load it as Utf8; you need to CAST it to Datetime with
        UTC timezone before returning.
      - The string format written by storage.py looks like
        `YYYY-MM-DD HH:MM:SS+00:00` because storage.py calls
        `.isoformat(sep=" ")` on a UTC-aware datetime. Your parser needs to
        tolerate that.
      - Sort by (name, date) on the way out. Enforce the invariant once.

    Hints:
      - `pl.read_database_uri("SELECT * FROM case_prices", f"sqlite:///{db_path}")`
        is the shortest path. It needs an engine extra (e.g. `connectorx` or
        `adbc-driver-sqlite`); if you don't want to add one, fall back to
        opening a `sqlite3.Connection` and passing it to
        `pl.read_database(query, connection)`.
      - `.with_columns(pl.col("date").str.to_datetime(time_zone="UTC"))`
        handles the cast. Polars' to_datetime is pretty forgiving about the
        input format.
      - `.sort(["name", "date"])` at the end.
    """
    with sqlite3.connect(db_path) as conn:
      query = "SELECT * FROM case_prices"
      df = pl.read_database(query=query, connection=conn)
      df = df.with_columns(pl.col("date").str.to_datetime(time_zone = "UTC"))
      df = df.sort(["name", "date"])
      timestamps = df["date"].to_numpy()
      query = "SELECT DISTINCT date FROM case_prices"
      timestamps = pl.read_database(query=query, connection=conn).to_numpy()
      
    conn.close()

    return df, timestamps

def get_signal(df: pl.DataFrame, case_name: str) -> np.ndarray:
    """Extract one case's price series as a 1D numpy array.

    Given the long DataFrame produced by `load_prices`, return the prices for
    `case_name`, sorted ascending by timestamp, as a 1D numpy array. This is
    the array shape that pywt.wavedec / pywt.cwt / pywt.dwt actually want.

    Args:
        df:        Long-format DataFrame as returned by load_prices().
        case_name: Human-readable case name (e.g. "KiloWatt Case"). Must
                   match exactly -- no URL encoding, no trimming.

    Returns:
        1D numpy array of shape (N,), dtype float64, where N is the number
        of observations for this case.

    Raises:
        ValueError: if `case_name` is not present in the DataFrame.

    Contract notes:
      - No gap-filling, no resampling, no log-transform. This function
        returns the raw observed price series. If you want a uniform hourly
        grid, call `resample_uniform_hourly` instead.
      - The output is 1D. Not (N, 1), not (1, N). Wavelet functions are
        picky about this.

    Hints:
      - `df.filter(pl.col("name") == case_name).sort("date").select("price").to_numpy()`
        gets you a (N, 1) array. Use `.ravel()` or `.flatten()` to get (N,).
      - Check for an empty result BEFORE calling `.to_numpy()`. A silent
        empty array is the worst kind of bug.
    """

    df = df.filter(pl.col("name") == case_name).sort("date").select("price")
    if df.is_empty():
      raise ValueError("Case Name Does Not Exist In DataFrame")
    num_arr = df.to_numpy().flatten()
    return num_arr



def resample_uniform_hourly_log_Momentum(
    df: pl.DataFrame,
    case_name: str
) -> np.ndarray:
    """Resample one case's price series onto a uniform hourly grid.

    Classical wavelet transforms (pywt.dwt, pywt.wavedec, pywt.cwt) assume
    equal time spacing between samples. Real scrapes miss hours -- Steam
    goes down, 429s happen, the machine reboots. Before any wavelet math,
    the signal MUST sit on a regular hourly grid.

    STUB. Not implemented. Intentionally.

    Args:
        df:            Long-format DataFrame from load_prices().
        case_name:     Case to resample.

    Returns:
        1D numpy array on a uniform hourly grid covering [min_date, max_date]
        for this case.

    Decisions deferred to implementation time (do NOT pre-answer these):
      - Gap-fill semantics. Forward-fill creates artificial plateaus that
        wavelets will read as zero-frequency content. Linear interp smooths
        out high-frequency structure. Zero-fill introduces step discontinuities.
        Each distorts the spectrum differently. This is a data-science
        decision, not a code decision.
      - Window bounds. Per-case (min to max for that case) is natural but
        makes cases incomparable. Project-wide (fixed start across all
        cases) makes cases aligned but front-loads cases with gaps of
        NaN/fill at the start.
      - Chose to Log prices because base prices of items vary in orders of magnitude 
        and logging it gives the precentage difference more accurately
      - Chose to detrend momentum  so that for 24 hour width periods continous increases
        are not confuse for a spike
    """

    df = df.filter(pl.col("name") == case_name).sort("date").upsample(time_column="date", every="1h")

    df = df.with_columns([
      pl.col("price").interpolate(),
      pl.col("volume").forward_fill()
    ])

    df = df.with_columns([
      pl.col("price").log(),
      pl.col("volume").log1p()
    ])

    df = df.with_columns([
      (pl.col("price") * pl.col("volume")).alias("Momentum")
    ])

    df = df.with_columns([
      (pl.col("Momentum") - pl.col("Momentum").rolling_mean(window_size=24)).alias("detrended_momentum")
    ])

    return df.select("detrended_momentum").to_numpy().flatten()

   


if __name__ == "__main__":
    # Poor-man's sanity check. Once you've implemented load_prices and
    # get_signal, running `py DataIngestion/analysis.py` should print the
    # DataFrame schema and the first signal without any NotImplementedError.
    df = load_prices()
    print("DataFrame shape:", df.shape)
    print("DataFrame schema:")
    print(df.schema)
    print("\nDataFrame head:")
    print(df.head())

    sample_case = "Recoil Case"
    signal = get_signal(df, sample_case)
    print(f"\nSignal for {sample_case!r}:")
    print("  shape:", signal.shape)
    print("  dtype:", signal.dtype)
    print("  first 5 values:", signal[:5])
    print("  last 5 values: ", signal[-5:])
