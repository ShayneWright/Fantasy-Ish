# Fantasy-Ish · Don Pablo’s

A self-contained fantasy-football decision dashboard with a report archive, player-by-player analysis, sportsbook outlook, week-by-week actual performance and legal lineup audits.

**Imported evidence cutoff: October 8, 2026, evening ET.** The initial Week 5 report is preserved exactly as supplied. Repository setup does not refresh its football data. The site shows the age of the snapshot.

## View the site

Expected GitHub Pages address after activation and a successful deployment:

**https://shaynewright.github.io/Fantasy-Ish/**

One-time activation:

1. Open [Settings → Pages](https://github.com/ShayneWright/Fantasy-Ish/settings/pages).
2. Under **Build and deployment → Source**, choose **GitHub Actions**.
3. Open [Actions](https://github.com/ShayneWright/Fantasy-Ish/actions), choose **Validate and publish dashboard**, then **Run workflow** on main. If the initial run failed because Pages was not enabled, re-run it after step 2.
4. Wait for both build and deploy to succeed. Open the deployment URL shown by the job. Verify the report date and Archive link.

Future main-branch commits run validation and publish automatically. Pull requests build without deploying. No custom domain or paid hosting is required for this public repository.

**The deploy workflow publishes committed files; it does not research games or refresh odds.** Schedule a research-capable agent using the instructions below to create new reports. There is no background sports-data feed or research schedule installed in this repository.

## Weekly maintenance

- [Comprehensive weekly update runbook](docs/WEEKLY-UPDATE.md): research, sourcing, roster decisions, results, validation, publication and failure handling.
- [Copyable scheduled-agent prompt](docs/SCHEDULED-PROMPT.md): use in a scheduler with web research and authorized repository write access.
- [League rules and scoring](docs/SCORING.md): custom half-PPR rules and unresolved scoring details.
- [AGENTS.md](AGENTS.md): mandatory context for coding/research agents.

Start with one weekly Tuesday results/research run and a Sunday pre-kickoff refresh. Add Thursday and Saturday checks if useful. Suggested timings and early-game exceptions are in the runbook. A scheduler that only sends reminders cannot execute repository updates.

## Local preview

Python 3.10+ is sufficient; no dependencies or API keys are needed to build.

```sh
python3 scripts/validate.py
python3 scripts/build.py
python3 -m http.server 8000 --directory _site
```

Open http://localhost:8000. Stop the server with Ctrl+C. The original archived HTML also opens directly in a browser, although the generated Pages copy adds archive navigation and freshness warnings.

## Repository layout

| Path | Purpose |
|---|---|
| reports/2026/week-05/2026-10-08-evening.html | Original complete report, including its embedded data and application |
| manifest.json | Append-only report index; latest selects the homepage snapshot |
| scripts/register_report.py | Register a newly researched HTML snapshot without replacing an existing one |
| scripts/validate.py | Validate report structure, references, scoring histories and exact legal lineup audit totals |
| scripts/build.py | Generate _site/index.html, archive.html and decorated report copies |
| .github/workflows/pages.yml | Build on PRs; build and deploy on main pushes or manual runs |
| docs/ | Weekly operating instructions, scheduled prompt and scoring contract |

Do not edit generated _site files. Create new dated reports; keep the original reports unchanged. The manifest does not itself contain the research data: each report embeds JSON in script#report-data.

## History available at import

- Week 1: actual scores unavailable; preserve null values. No original Week 1 HTML has been recovered into this repository.
- Weeks 2–4: actual player scores and starter/bench labels are included in the Week 5 comparison table.
- Week 3: actual **83.44**, legal optimum **118.02**, improvement **34.58**.
- Week 4: actual **105.86**, legal optimum **127.96**, improvement **22.10**.

These are hindsight ceilings, not claims that every winning substitution was predictable. The user’s “law of 10” is a target, not a guarantee or a maximum.

## Important implementation limits

The imported dashboard is a complete single-file report with week-specific prose and UI defaults. A weekly updater must change the narrative, table labels, lineup defaults, opponent totals and history ranges together with the JSON. The registration script packages and checks the file; it does not write those insights.

The build validates arithmetic and structure, not the truth of a source or a recommendation. Browsing the output and checking citations remain part of the runbook. Historical snapshots may contain incomplete fields; do not convert missing information into zero.

GitHub Pages setup reference: https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site
