#!/usr/bin/env python3
"""Run Bayesian causal discovery with a stable CLI wrapper."""

from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path
from typing import Iterable

import pandas as pd

from engine import CausalDiscoveryEngine


def parse_edge_list(raw: str | None) -> list[tuple[str, str]]:
    """Parse comma-separated edge pairs in src:tgt format."""
    if not raw:
        return []
    edges: list[tuple[str, str]] = []
    for item in raw.split(","):
        pair = item.strip()
        if not pair:
            continue
        if ":" not in pair:
            raise ValueError(f"Invalid edge '{pair}'. Use src:tgt format.")
        src, tgt = pair.split(":", 1)
        src, tgt = src.strip(), tgt.strip()
        if not src or not tgt:
            raise ValueError(f"Invalid edge '{pair}'. Use src:tgt format.")
        edges.append((src, tgt))
    return edges


def parse_csv_list(raw: str | None) -> list[str]:
    if not raw:
        return []
    return [x.strip() for x in raw.split(",") if x.strip()]


def ensure_columns(df: pd.DataFrame, cols: Iterable[str], label: str) -> None:
    missing = [col for col in cols if col not in df.columns]
    if missing:
        missing_str = ", ".join(missing)
        raise ValueError(f"{label} column(s) not found in data: {missing_str}")


def load_dataframe(args: argparse.Namespace) -> pd.DataFrame:
    if args.csv and args.sqlite:
        raise ValueError("Use only one source: --csv or --sqlite")
    if not args.csv and not args.sqlite:
        raise ValueError("Provide a data source with --csv or --sqlite")

    if args.csv:
        path = Path(args.csv).expanduser().resolve()
        if not path.exists():
            raise FileNotFoundError(f"CSV not found: {path}")
        return pd.read_csv(path)

    db_path = Path(args.sqlite).expanduser().resolve()
    if not db_path.exists():
        raise FileNotFoundError(f"SQLite database not found: {db_path}")
    if not args.table:
        raise ValueError("When using --sqlite, provide --table")

    with sqlite3.connect(str(db_path)) as conn:
        return pd.read_sql_query(f"SELECT * FROM {args.table}", conn)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", help="Path to input CSV file")
    parser.add_argument("--sqlite", help="Path to SQLite database file")
    parser.add_argument("--table", help="SQLite table name")
    parser.add_argument("--target", required=True, help="Target/effect variable")
    parser.add_argument("--exog", help="Comma-separated exogenous columns")
    parser.add_argument(
        "--blacklist",
        help="Comma-separated forbidden edges in src:tgt format",
    )
    parser.add_argument(
        "--whitelist",
        help="Comma-separated required edges in src:tgt format",
    )
    parser.add_argument("--bins", type=int, default=3, help="Number of bins (default: 3)")
    parser.add_argument(
        "--bootstrap",
        type=int,
        default=30,
        help="Bootstrap iterations (default: 30)",
    )
    parser.add_argument(
        "--restarts",
        type=int,
        default=3,
        help="HillClimb restarts (default: 3)",
    )
    parser.add_argument(
        "--output",
        default="./causal_discovery_output",
        help="Output directory",
    )
    parser.add_argument(
        "--drop-cols",
        help="Comma-separated columns to drop before modeling",
    )

    args = parser.parse_args()

    df = load_dataframe(args)
    if df.empty:
        raise ValueError("Input dataset is empty")

    drop_cols = parse_csv_list(args.drop_cols)
    if drop_cols:
        ensure_columns(df, drop_cols, "Drop")
        df = df.drop(columns=drop_cols)

    exog = parse_csv_list(args.exog)
    blacklist = parse_edge_list(args.blacklist)
    whitelist = parse_edge_list(args.whitelist)

    ensure_columns(df, [args.target], "Target")
    ensure_columns(df, exog, "Exogenous")

    flat_edges = [col for edge in (blacklist + whitelist) for col in edge]
    ensure_columns(df, flat_edges, "Edge")

    config = {
        "target_variable": args.target,
        "exogenous_variables": exog,
        "blacklist": blacklist,
        "whitelist": whitelist,
        "n_bins": args.bins,
        "hc_restarts": args.restarts,
        "n_bootstrap": args.bootstrap,
        "output_dir": args.output,
    }

    print(f"Loaded data with {df.shape[0]} rows and {df.shape[1]} columns")
    print(f"Target variable: {args.target}")
    if exog:
        print(f"Exogenous variables: {', '.join(exog)}")

    engine = CausalDiscoveryEngine(config)
    result = engine.run(df)
    summary = result["confidence_summary"]
    print(
        "Confidence tiers: "
        f"GREEN={summary['green']} "
        f"YELLOW={summary['yellow']} "
        f"RED={summary['red']}"
    )


if __name__ == "__main__":
    main()
