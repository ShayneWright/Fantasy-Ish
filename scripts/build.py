"""Create a static Pages artifact without modifying archived reports."""
import html
import json
import os
import shutil
from pathlib import Path
from validate import ROOT, validate

OUT = ROOT / "_site"

def decorate(source, report, prefix, archived=False):
    label = html.escape(report["as_of_label"])
    notice = f"""<aside style="background:#fff2ce;color:#302514;padding:16px 24px;font:14px/1.5 system-ui" aria-label="Report freshness">
<strong>{'Archived report' if archived else 'Latest published report'} · Week {report['week']} / {report['season']}</strong><br>
Evidence as of {label}. <span id="snapshot-age"></span>
This is a dated research snapshot, not a live odds feed. Confirm injuries, inactive lists and prices before kickoff.
<br><a href="{prefix}archive.html">Browse all reports</a> · <a href="https://github.com/ShayneWright/Fantasy-Ish">Repository and update instructions</a>
</aside>"""
    # Metadata used only in textContent; JSON encoding prevents script injection.
    stamp = json.dumps(report["as_of"]).replace("<", "\\u003c")
    freshness = f"""<script>
(function(){{const stamp={stamp};const days=Math.floor((Date.now()-Date.parse(stamp))/86400000);
document.getElementById('snapshot-age').textContent=days>=1?'Snapshot is '+days+' day(s) old.':'Check the timestamp before using.';}})();
</script>"""
    source = source.replace("<body>", "<body>" + notice, 1)
    source = source.replace("This is a separate file; the GitHub archive has not been overwritten or deployed.",
                            "This published copy retains the original report; prior snapshots remain in the archive.")
    return source.replace("</body>", freshness + "</body>")

def build():
    manifest = validate()
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    (OUT / ".nojekyll").touch()
    rows = []
    for report in manifest["reports"]:
        source = (ROOT / report["path"]).read_text(encoding="utf-8")
        dest = OUT / report["path"]
        dest.parent.mkdir(parents=True, exist_ok=True)
        prefix = os.path.relpath(OUT, dest.parent).replace(os.sep, "/") + "/"
        dest.write_text(decorate(source, report, prefix, True), encoding="utf-8")
        if report["id"] == manifest["latest"]:
            (OUT / "index.html").write_text(decorate(source, report, ""), encoding="utf-8")
        rows.append(f'<li><a href="{html.escape(report["path"])}">Week {report["week"]} · {report["season"]} · {html.escape(report["as_of_label"])}</a><p>{html.escape(report["notes"])}</p></li>')
    archive = """<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Don Pablo’s — report archive</title><style>body{max-width:950px;margin:40px auto;padding:24px;background:#f4f5ef;color:#17231d;font:17px/1.6 system-ui}a{color:#1d6b4d}li{margin:24px 0}p{font-size:14px}</style>
<h1>Don Pablo’s · Report archive</h1><a href="index.html">Latest published report</a>
<p>Snapshots preserve the evidence and advice available at the time. No Week 1 report has been recovered; Week 1 actuals remain unknown. The imported Week 5 report includes Week 2–4 player comparisons.</p><ul>"""
    (OUT / "archive.html").write_text(archive + "".join(reversed(rows)) + "</ul></html>", encoding="utf-8")
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print("Built _site/index.html and all archived reports.")

if __name__ == "__main__":
    build()
