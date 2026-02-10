"""Convert Surity_Process_Catalogue_V4.xlsx to JSON seed file.

One-time script. Reads the V4 Excel spreadsheet and outputs a structured
JSON file suitable for the Alembic migration to consume.

Usage:
    python reference/convert_v4_excel_to_json.py

Output:
    reference/process_catalogue_v4_seed.json
"""

import json
import os
import re

import openpyxl

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.normpath(os.path.join(SCRIPT_DIR, ".."))
INPUT_FILE = os.path.join(
    PROJECT_ROOT, "Additional Design Documents", "Surity_Process_Catalogue_V4.xlsx"
)
OUTPUT_FILE = os.path.join(SCRIPT_DIR, "process_catalogue_v4_seed.json")

# Regex to strip leading numeric prefix: "1. Strategy" → "Strategy", "1.1 Client & ..." → "Client & ..."
PREFIX_PATTERN = re.compile(r"^\d+(?:\.\d+)*\.?\s+")

# Normalize abbreviated role names to match the canonical role_catalogue names (migration 014)
ROLE_ALIASES = {
    "Asst. Accountant": "Assistant Accountant",
    "Sr. QA Technologist": "Senior QA Technologist",
    "Sr. Packaging Technologist": "Senior Packaging Technologist",
    "All Staff": "All Staff",  # keep as-is — not a real role, just a RACI placeholder
}


def strip_prefix(value: str | None) -> str | None:
    """Remove leading numeric ref prefix from a cell value."""
    if not value:
        return None
    cleaned = PREFIX_PATTERN.sub("", str(value).strip())
    return cleaned if cleaned else None


def normalize_role(value: str | None) -> str | None:
    """Normalize a RACI role value, expanding abbreviations."""
    if not value:
        return None
    text = str(value).strip()
    # For comma-separated values (C and I columns), normalize each part
    parts = [p.strip() for p in text.split(",")]
    normalized = [ROLE_ALIASES.get(p, p) for p in parts if p]
    return ", ".join(normalized) if normalized else None


def main() -> None:
    if not os.path.exists(INPUT_FILE):
        print(f"ERROR: Input file not found: {INPUT_FILE}")
        return

    wb = openpyxl.load_workbook(INPUT_FILE, data_only=True)
    ws = wb["Process Catalogue"]

    rows_out: list[dict] = []
    counts = {"L0": 0, "L1": 0, "L2": 0, "L3": 0}
    raci_count = 0
    kpi_count = 0

    for row in ws.iter_rows(min_row=2, values_only=True):
        ref_raw, l0_raw, l1_raw, l2_raw, l3_raw, desc, r, a, c, i, kpi = (
            row[0],
            row[1],
            row[2],
            row[3],
            row[4],
            row[5] if len(row) > 5 else None,
            row[6] if len(row) > 6 else None,
            row[7] if len(row) > 7 else None,
            row[8] if len(row) > 8 else None,
            row[9] if len(row) > 9 else None,
            row[10] if len(row) > 10 else None,
        )

        if ref_raw is None:
            continue

        ref = str(ref_raw).strip()

        # Determine level from ref dot count
        dot_count = ref.count(".")
        level = dot_count  # 0=L0, 1=L1, 2=L2, 3=L3

        # Clean names — strip numeric prefixes
        l0_name = strip_prefix(l0_raw)
        l1_name = strip_prefix(l1_raw)
        l2_name = strip_prefix(l2_raw)
        l3_name = strip_prefix(l3_raw)

        # Determine the process name for this row
        if level == 0:
            name = l0_name
        elif level == 1:
            name = l1_name
        elif level == 2:
            name = l2_name
        else:
            name = l3_name

        if not name:
            continue

        entry: dict = {
            "ref": ref,
            "level": level,
            "name": name,
        }

        # Add L0 context for parent resolution
        if l0_name:
            entry["l0"] = l0_name

        # Add description (L3 only)
        if desc:
            entry["description"] = str(desc).strip()

        # Add RACI (L3 only) — normalize abbreviations to canonical role names
        if r or a or c or i:
            entry["responsible"] = normalize_role(r)
            entry["accountable"] = normalize_role(a)
            entry["consulted"] = normalize_role(c)
            entry["informed"] = normalize_role(i)
            raci_count += 1

        # Add KPI (L3 only)
        if kpi:
            entry["kpi"] = str(kpi).strip()
            kpi_count += 1

        level_key = f"L{level}"
        counts[level_key] += 1
        rows_out.append(entry)

    # Write output
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(rows_out, f, indent=2, ensure_ascii=False)

    total = sum(counts.values())
    print(f"Converted {total} processes to {OUTPUT_FILE}")
    print(f"  L0: {counts['L0']}, L1: {counts['L1']}, L2: {counts['L2']}, L3: {counts['L3']}")
    print(f"  RACI entries: {raci_count}")
    print(f"  KPI entries: {kpi_count}")


if __name__ == "__main__":
    main()
