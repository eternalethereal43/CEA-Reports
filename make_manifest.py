#!/usr/bin/env python3
"""Write CEA Reports/manifest.json so the dashboard knows what is in the folder.

GitHub Pages serves no directory listing, so the dashboard reads this file.
Run it after adding reports:

    python tools/make_manifest.py

The GitHub Action in .github/workflows/build-manifest.yml runs it for you on
every push that touches the reports folder.
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT, "CEA Reports")
REPORT = re.compile(r"^(\d{2})-(\d{2})-(\d{4})\.(xlsx|xlsm|xls)$", re.I)


def main() -> int:
    if not os.path.isdir(DATA_DIR):
        print(f"No folder at {DATA_DIR}", file=sys.stderr)
        return 1

    files, skipped = [], []
    for name in sorted(os.listdir(DATA_DIR)):
        if name.startswith((".", "~$")) or name == "manifest.json":
            continue
        m = REPORT.match(name)
        if m:
            d, mo, y = m.group(1), m.group(2), m.group(3)
            files.append({"name": name, "date": f"{y}-{mo}-{d}"})
        elif os.path.isfile(os.path.join(DATA_DIR, name)):
            skipped.append(name)

    files.sort(key=lambda f: f["date"])
    out = {
        "folder": "CEA Reports",
        "count": len(files),
        "files": [f["name"] for f in files],
        "dates": [f["date"] for f in files],
    }
    with open(os.path.join(DATA_DIR, "manifest.json"), "w") as fh:
        json.dump(out, fh, indent=1)
        fh.write("\n")

    print(f"manifest.json written with {len(files)} report(s)")
    if files:
        print(f"  {files[0]['date']} to {files[-1]['date']}")
    for name in skipped:
        print(f"  skipped (not named DD-MM-YYYY): {name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
