#!/usr/bin/env python3
"""Write manifest.json listing the reports that sit beside index.html.

GitHub Pages serves no directory listing, so the dashboard reads this file.
Run it after adding reports:

    python tools/make_manifest.py

The GitHub Action in .github/workflows/build-manifest.yml runs it for you on
every push that adds or removes a report.
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORT = re.compile(r"^(\d{2})-(\d{2})-(\d{4})\.(xlsx|xlsm|xls)$", re.I)
WORKBOOK = re.compile(r"\.(xlsx|xlsm|xls)$", re.I)


def main() -> int:
    files, skipped = [], []
    for name in sorted(os.listdir(ROOT)):
        if name.startswith((".", "~$")) or not os.path.isfile(os.path.join(ROOT, name)):
            continue
        m = REPORT.match(name)
        if m:
            d, mo, y = m.group(1), m.group(2), m.group(3)
            files.append({"name": name, "date": f"{y}-{mo}-{d}"})
        elif WORKBOOK.search(name):
            skipped.append(name)

    files.sort(key=lambda f: f["date"])
    out = {
        "count": len(files),
        "files": [f["name"] for f in files],
        "dates": [f["date"] for f in files],
    }
    with open(os.path.join(ROOT, "manifest.json"), "w") as fh:
        json.dump(out, fh, indent=1)
        fh.write("\n")

    print(f"manifest.json written with {len(files)} report(s)")
    if files:
        print(f"  {files[0]['date']} to {files[-1]['date']}")
    for name in skipped:
        print(f"  skipped (not named DD-MM-YYYY): {name}")
    if not files:
        print("  nothing matched — reports must be named like 26-08-2026.xlsx", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
