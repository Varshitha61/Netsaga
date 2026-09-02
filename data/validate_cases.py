"""
validate_cases.py — Dataset integrity checker for cases.csv

Usage:
    python data/validate_cases.py
"""

import sys
import os
import pandas as pd

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
CSV_PATH = os.path.join(os.path.dirname(__file__), "cases.csv")
REQUIRED_COLUMNS = [
    "case_id",
    "symptom",
    "topology_note",
    "show_command_outputs",
    "expected_fault",
    "osi_layer",
    "concept_tag",
    "severity",
    "source",
]
MIN_ROWS = 30

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_csv(path: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(path)
    except FileNotFoundError:
        print(f"[ERROR] File not found: {path}")
        sys.exit(1)
    except pd.errors.ParserError as exc:
        print(f"[ERROR] CSV parse error: {exc}")
        sys.exit(1)
    return df


def check_row_count(df: pd.DataFrame) -> None:
    count = len(df)
    status = "✅ PASS" if count >= MIN_ROWS else "❌ FAIL"
    print(f"{status}  Row count: {count} (minimum {MIN_ROWS})")
    assert count >= MIN_ROWS, f"Expected at least {MIN_ROWS} rows, got {count}"


def check_required_columns(df: pd.DataFrame) -> None:
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        print(f"❌ FAIL  Missing columns: {missing}")
        assert False, f"Missing columns: {missing}"
    print(f"✅ PASS  All required columns present: {REQUIRED_COLUMNS}")


def check_no_empty_fields(df: pd.DataFrame) -> None:
    issues = []
    for col in REQUIRED_COLUMNS:
        empty_rows = df[df[col].isnull() | (df[col].astype(str).str.strip() == "")]
        if not empty_rows.empty:
            issues.append(f"  Column '{col}' empty in rows: {empty_rows.index.tolist()}")
    if issues:
        print("❌ FAIL  Empty field(s) detected:")
        for issue in issues:
            print(issue)
        assert False, "Empty fields found"
    print("✅ PASS  No empty fields detected")


def print_distribution(df: pd.DataFrame) -> None:
    print("\n" + "=" * 55)
    print("📊  Cases per concept_tag")
    print("=" * 55)
    tag_counts = df["concept_tag"].value_counts()
    for tag, count in tag_counts.items():
        bar = "█" * count
        print(f"  {tag:<35} {count:>3}  {bar}")

    print("\n" + "=" * 55)
    print("📊  Cases per OSI layer")
    print("=" * 55)
    layer_counts = df["osi_layer"].value_counts()
    for layer, count in layer_counts.items():
        bar = "█" * count
        print(f"  {layer:<35} {count:>3}  {bar}")

    print("\n" + "=" * 55)
    print("📊  Cases per severity")
    print("=" * 55)
    sev_counts = df["severity"].value_counts()
    for sev, count in sev_counts.items():
        bar = "█" * count
        print(f"  {sev:<35} {count:>3}  {bar}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    print(f"\n🔍  Validating: {CSV_PATH}\n")
    df = load_csv(CSV_PATH)

    errors = 0
    for check_fn in (check_required_columns, check_row_count, check_no_empty_fields):
        try:
            check_fn(df)
        except AssertionError as exc:
            print(f"   └─ {exc}")
            errors += 1

    print_distribution(df)

    print("\n" + "=" * 55)
    if errors == 0:
        print("✅  All validation checks passed.")
    else:
        print(f"❌  {errors} check(s) failed. See above for details.")
        sys.exit(1)


if __name__ == "__main__":
    main()
