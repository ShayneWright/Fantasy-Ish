"""Validate archived data and exact legal lineup audits; standard library only."""
import itertools
import json
import math
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = re.compile(r'<script id="report-data" type="application/json">(.*?)</script>', re.S)

def extract(path):
    match = DATA.search(path.read_text(encoding="utf-8"))
    assert match, f"{path}: embedded report-data missing"
    return json.loads(match.group(1))

def legal(players):
    pos = [p["pos"] for p in players]
    return (len(pos) == 9 and pos.count("QB") == 1 and pos.count("D/ST") == 1
            and pos.count("RB") >= 2 and pos.count("WR") >= 2 and pos.count("TE") >= 1
            and all(p in {"QB", "RB", "WR", "TE", "D/ST"} for p in pos))

def validate_report(path):
    data = extract(path)
    players = data["players"]
    assert len({p["id"] for p in players}) == len(players), "Duplicate player IDs"
    assert len({len(p["scores"]) for p in players}) == 1, "Unequal history lengths"
    for p in players:
        assert len(p["scores"]) == len(p["started"]), p["id"]
        assert all(x is None or isinstance(x, bool) for x in p["started"]), p["id"]
        assert all(x is None or (isinstance(x, (int, float)) and math.isfinite(x)) for x in p["scores"]), p["id"]
        for key in ("propRefs", "injRefs", "histRefs"):
            assert all(ref in data["sources"] for ref in p.get(key, [])), f"Unknown source: {p['id']}"
    for key, source in data["sources"].items():
        assert len(source) == 2 and source[1].startswith("https://"), key
    for game in data["games"]:
        assert game["total"] > 0 and abs(game["spread"]) < game["total"]
    for audit in data["audit"]:
        week = audit["week"] - 1
        eligible = [p for p in players if p["scores"][week] is not None]
        starters = [p for p in eligible if p["started"][week] is True]
        assert legal(starters), f"Invalid starters Week {week + 1}"
        actual = sum(p["scores"][week] for p in starters)
        optimum = max(sum(p["scores"][week] for p in lineup)
                      for lineup in itertools.combinations(eligible, 9) if legal(lineup))
        selected = [p for p in eligible if p["id"] in audit["best"]["ids"]]
        assert len(set(audit["best"]["ids"])) == 9 and legal(selected), "Invalid optimum lineup"
        assert abs(actual - audit["actual"]) < .005, f"Actual mismatch Week {week + 1}"
        assert abs(optimum - audit["best"]["total"]) < .005, f"Optimum mismatch Week {week + 1}"
        assert abs(sum(p["scores"][week] for p in selected) - optimum) < .005
    return data

def validate():
    manifest = json.loads((ROOT / "manifest.json").read_text())
    reports = manifest["reports"]
    assert manifest["schema_version"] == 1
    assert len({r["id"] for r in reports}) == len(reports), "Duplicate report ID"
    assert len({r["path"] for r in reports}) == len(reports), "Duplicate report path"
    assert manifest["latest"] in {r["id"] for r in reports}
    for report in reports:
        assert 1 <= report["week"] <= 22 and 2026 <= report["season"] <= 2100
        datetime.fromisoformat(report["as_of"])
        path = ROOT / report["path"]
        assert path.resolve().is_relative_to((ROOT / "reports").resolve())
        assert path.suffix == ".html"
        validate_report(path)
    print(f"Validated {len(reports)} report(s), source references, histories and legal lineup audits.")
    return manifest

if __name__ == "__main__":
    validate()
