"""Append a fully researched HTML report. Never overwrite an existing snapshot."""
import argparse
import json
import re
from datetime import datetime
from pathlib import Path
from validate import ROOT, validate_report

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--file", required=True, type=Path)
    parser.add_argument("--season", required=True, type=int)
    parser.add_argument("--week", required=True, type=int)
    parser.add_argument("--as-of", required=True, help="Actual evidence cutoff: ISO 8601 with timezone")
    parser.add_argument("--label", required=True, help="Readable evidence cutoff and coverage caveat")
    parser.add_argument("--notes", required=True, help="What changed and any unresolved data")
    parser.add_argument("--status", default="partial", choices=["partial", "pregame", "results", "correction"])
    args = parser.parse_args()
    dt = datetime.fromisoformat(args.as_of)
    assert dt.tzinfo is not None, "--as-of needs a timezone offset"
    assert 1 <= args.week <= 22 and 2026 <= args.season <= 2100
    validate_report(args.file)
    stamp = re.sub(r"[^0-9A-Za-z]", "", args.as_of)
    path = f"reports/{args.season}/week-{args.week:02d}/{stamp}.html"
    report_id = f"{args.season}-w{args.week:02d}-{stamp}"
    manifest_path = ROOT / "manifest.json"
    manifest = json.loads(manifest_path.read_text())
    assert report_id not in {r["id"] for r in manifest["reports"]}, "Snapshot already registered"
    dest = ROOT / path
    dest.parent.mkdir(parents=True, exist_ok=True)
    with dest.open("xb") as output:
        output.write(args.file.read_bytes())
    manifest["reports"].append(dict(id=report_id, season=args.season, week=args.week,
        as_of=args.as_of, as_of_label=args.label, status=args.status, path=path, notes=args.notes))
    manifest["latest"] = report_id
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"Registered {path}. Run validate.py and build.py before committing.")

if __name__ == "__main__":
    main()
