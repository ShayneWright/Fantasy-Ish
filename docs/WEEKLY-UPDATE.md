# Weekly operating runbook

## 1. What this system does

Maintain a source-backed, dated HTML decision report for Don Pablo's and retain the record of what was recommended before games. Explain each roster decision against the actual opponent while preserving week-by-week results. Game environment comes from sportsbook markets. Player role and injury evidence comes from verifiable football sources.

The website is static, but a new committed report deploys automatically after Pages is enabled. A research agent must gather data and author that report. The deployment Action does not run research. Do not set a cron that merely rebuilds old data and call that a live update.

## 2. Initial setup and execution access

1. Enable GitHub Pages using the README steps.
2. Give the scheduled agent access to this repository, a working Python environment and web research. A coding-only agent without internet cannot complete the football refresh.
3. Provide an authorized way to read the current roster, opponent, scoring and actual results. Screenshots supplied by the user are valid evidence; repository access alone does not grant ESPN access. If no fresh roster is available, disclose the date of the last known roster and treat lineup advice as conditional.
4. Use a branch/PR by default. If the user explicitly authorizes unattended publishing to main, record that policy in the scheduler configuration. Follow branch protection and required reviews.
5. Never store passwords, session cookies or API keys in the repository. If a paid odds API is later selected, configure its credentials in the execution environment and document its rate limits and coverage. No paid API is required to build the present site.
6. Supply the scheduled prompt from SCHEDULED-PROMPT.md. Test one manual run before enabling recurrence. Verify that the scheduler actually checks out, researches, writes and submits changes, not just sends a notification.

## 3. Suggested cadence

Use **America/New_York** for football schedules and daylight-saving handling. Do not infer the week from a calendar week number. Verify the actual NFL schedule first, including international and unusual Wednesday/Saturday games.

| Run | Suggested local time | Main work |
|---|---|---|
| Results review | Tuesday 10:00 ET | Reconcile final scores, usage, injuries; audit legal optimum; start next report |
| Early-game decision | Thursday 16:00 ET | Refresh odds and availability; identify tonight's locks and preserve FLEX flexibility |
| Practice review | Saturday 16:00 ET | Final designations, likely workloads, late-game contingency plans |
| Main pregame review | Sunday 08:00 ET | Refresh all markets and news; check early international games |
| Early inactives | Sunday 11:35 ET, if 13:00 games | Check released inactives and final replacements |
| Late inactives | About 85 minutes before affected kickoff | Verify late-window injury decisions with eligible fallback players |
| Monday check | About 85 minutes before kickoff, if relevant | Verify remaining players and contingency availability |

These are suggested times, not installed schedules. The game-dependent checkpoints take priority over the table. A once-weekly update cannot replace last-minute inactive checks. A scheduler using UTC needs seasonal conversion; prefer a timezone-aware schedule instead of fixed UTC. GitHub scheduled jobs can be delayed and should not be relied on for last-second lineup actions.

## 4. Start every run with evidence and context

Read AGENTS.md, SCORING.md, manifest.json and the latest registered HTML. Inspect the latest pregame report and completed-week results separately.

Confirm:

- Current date/time/timezone, season and NFL week.
- Latest roster, positions, transactions, bench/IR and current starters.
- Opponent's starters, bench alternatives, injuries and already-locked players.
- League scoring and lineup locks. An opponent carrying an out/zero-projection starter may replace him; model that scenario instead of assuming free points.
- What this run can verify and what is unavailable. Retain provenance for screenshot facts; do not describe them as independently verified live feed data.

Keep all observed data at its original observation timestamp. Track retrieval time separately from event date, source publication date and report creation time.

## 5. Source hierarchy and cross-checks

Use official team/NFL roster, depth-chart, injury report, practice participation and inactive announcements first. Use official gamebooks and NFL/ESPN box scores for actual stats. Beat reporting may support workload expectations if attributed; label inference clearly.

Use named sportsbook pages or a reputable odds aggregator that identifies the book and timestamp for markets. Cross-check critical lines with another book where available. Cite each relevant source with a direct URL, publication/observation time and the specific claim it supports. Do not source ten unrelated claims to a generic team homepage.

For contradictory facts, prefer the latest relevant official update and explain the conflict. If neither source resolves it, mark uncertain. Verify standings through the completed games appropriate to the report's cutoff; record wins/losses/ties, division position, last three results, points for/against and sample size. Do not confuse fantasy opponent ranks with NFL standings.

## 6. Main player table — all rostered players

Player name must be the first column. Include team and position, then:

| Column | Required evidence and interpretation |
|---|---|
| Decision | Start/bench/conditional; confidence supported by evidence; concrete fallback and decision deadline |
| Game | Opponent, home/away/neutral site, kickoff with timezone, venue/roof |
| Vegas | Named book, spread, total, team/opponent implied totals, observation time and movement |
| Props | Passing attempts/completions/yards, rushing/receiving yards, catches and TD market where available; threshold, price and source |
| Actual role | Official depth position plus snaps, routes, carries, targets, target/route share, goal-line/red-zone work and return role |
| Availability | Practice sequence, injury designation, expected limitations, confirmed inactives when released |
| Supporting personnel | Starting QB and line availability; relevant teammates' absences; opposing corners/LBs/pass rush injuries |
| Opposition | Current record/division rank, recent results, run/pass strength, recent position-specific yards/catches/TDs allowed |
| History | Last 3–5 games, opponent history with dates and sample size, useful venue/split evidence |
| Conditions | Wind/rain, roof status, travel, rest and short-week factors |
| Law of 10 | Actual hit rate over known comparable games, route to 10 and dependence on TDs/returns |
| Sources / caveats | Field-level provenance, timestamps, missing fields and fact-versus-inference labels |

Do not omit bench players or auto-start a player because he is listed first on a depth chart. Routes, targets, carries and scoring-area opportunities are more useful than a TE1 label alone. Account for the different value of receptions, completions and returns in this league.

## 7. Sportsbook mathematics and limits

Let T be the total and S the signed point spread for the player's team (favorite negative):

- Player's team implied total = (T - S) / 2.
- Opponent implied total = (T + S) / 2.
- Example: team -3, total 47 gives 25–22.

Store lines from the same book and observation time for a given calculation. Keep half-points and don't round to a plausible football final score. Both implied totals must sum to T, and their difference must equal -S.

Line movement requires opening/earlier and current observations from the **same book and same market**. Cross-book disagreement is not line movement. If no opening observation exists, say unavailable.

Props are market thresholds with prices, not automatically statistical means. An anytime-TD price measures at least one TD, not expected TD count. Converting American odds to a raw implied probability uses 100/(positive odds + 100), or abs(negative odds)/(abs(negative odds) + 100); raw probabilities include margin. Only remove vig when the complete relevant opposing market is available, and disclose the method.

Do not convert the game total into a player fantasy projection without a documented workload model. Keep ESPN projections, market-derived information, own estimates and actual points separate. No precise 10+ probability or win probability without a calibrated model and validation. Markets incorporate risk management as well as forecasting; they are strong evidence, not guarantees.

## 8. Build the actual matchup recommendation

1. Establish a valid nine-player lineup under SCORING.md.
2. Compare the marginal choices: QB alternative, second RB, second WR and the two FLEX spots. Provide point estimates only with stated methodology, or a qualitative lean if data is inadequate.
3. Explain each close call using role, injury certainty, expected team scoring and matchup. Limit weight on historical head-to-head performance when coaches, scheme or personnel changed.
4. Keep later-playing flexible options available by putting earlier WR/RB/TE starters into their specific slots where possible. Check platform lock rules.
5. Set a decision tree for questionable players: what official update changes the recommendation, when it is expected, and which eligible unlocked substitute remains.
6. Recalculate against the opponent after plausible replacements. Show the scenario range rather than treating their injured player's zero as final.
7. Keep conservative and upside alternatives appropriate to the matchup, without chasing a tiny projection difference or last week's touchdowns.

## 9. Week-by-week performance and bench audit

For every current roster player show all known weekly actuals, starter/bench/IR status where known, average over known weeks, latest change, known-week 10+ hit rate and sample size. Keep departed players in old snapshots. Missing weeks are null and excluded from averages; 0 is a verified zero. Clearly distinguish injury/inactive zeros from active games.

Use full gamebooks for the reason behind a breakout: route and snap change, target volume, rushing volume, goal-line share, long plays, return yards, opponent injuries and game script. Separate repeatable opportunity from TD variance. A three-TD game alone does not prove a new lead-back role.

Calculate:

1. Actual starter total (cross-check the final ESPN matchup total).
2. Maximum score obtainable from that week's roster with QB1/RB2/WR2/TE1/FLEX2/D-ST1, no duplicates. QB cannot enter FLEX.
3. Missed opportunity = legal optimum minus actual total, not the sum of all bench scores.
4. Exact swaps and score deltas; distinguish one swap from a set that requires position reshuffling.
5. Whether the optimal lineup would have changed the result.
6. Pregame process review using the recommendation and source snapshot recorded before kickoff. Do not re-label hindsight as an obvious decision.

Seed checks from the supplied results:

| Week | Actual | Legal optimum | Difference |
|---|---:|---:|---:|
| 3 | 83.44 | 118.02 | 34.58 |
| 4 | 105.86 | 127.96 | 22.10 |

Week 3 improvement: Burden for Concepcion +13.18; Meyers for Henry +13.72; Brian Robinson for Hampton +7.68.

Week 4 optimal lineup: Goff, Taylor, Hampton, Olave, Shakir, Kittle at TE, Brian Robinson and Concepcion at FLEX, Steelers D/ST. This requires moving Kittle into TE so Warren's place can become a FLEX opportunity. The optimizer must account for this, not merely compare bench players against like-labelled starting slots.

Retain the previous confirmed scores if there is a possible stat correction; append a correction report with the source and old/new values.

## 10. Author and register a new report

Reports are self-contained HTML. Start from a copy of the last relevant report in an ignored scratch directory. Never modify the original archive file.

Embedded data lives in script#report-data. Existing keys: sources, games, teams, players, asof, note, audit. Each player's scores/started arrays use week-minus-one indexing. Append new weeks without shifting older indices. Each source is [label, https URL]. Game spread is signed for the away team in the imported data. Keep that convention consistent with the UI calculations.

Update **both data and prose/application code**. The imported report has hard-coded week titles, historical table headings/ranges, current/lean lineup defaults, opponent totals, dates, source labels, audit text and deadline cards. Search for stale week numbers, dates, player IDs and old opponent totals. Extend all history loops and headers; verify the new week actually appears. Remove or update unsupported claims, not just the title.

Add per-field observation times and status labels in the UI when refreshing a subset. An overall new report date must not imply all carried-forward facts were reverified. Mark unknown props, snaps or injuries explicitly. A failed research run should leave the latest report pointer unchanged and return a failure summary.

After research and manual consistency review:

```sh
python3 scripts/register_report.py \
  --file scratch/new-report.html \
  --season 2026 --week 6 \
  --as-of 2026-10-18T11:40:00-04:00 \
  --label "October 18, 2026, 11:40 ET; early inactive lists checked" \
  --status pregame \
  --notes "Refreshed roster, markets and early inactives; late-game inactives pending."
python3 scripts/validate.py
python3 scripts/build.py
```

The command above is an example, not a claim about that future week's schedule or evidence. Replace every value with the verified run context. The script copies the new file into reports/season/week-NN, appends manifest.json and updates latest. It rejects an existing snapshot ID/path. If later validation fails, do not commit the incomplete candidate; fix only the newly added candidate and its manifest entry, leaving pre-existing history intact.

For a results report, continue to show the completed week's true decision context and add the audit. For a new pregame week, preserve all completed actuals and update the upcoming matchup. Register separate snapshots for distinct phases.

## 11. Validation before commit

- Run validate.py: it checks unique players/reports, source-reference keys, known-score histories, legal starter totals and exhaustive legal optimum totals.
- Run build.py: output must include index.html, archive.html, manifest.json and each report path. Archive links and nested-page navigation must work under /Fantasy-Ish/.
- Check the latest report's names, all roster rows, injuries, source URLs, bookmaker labels, implied-total formulas and timestamps.
- Verify every numerical claim against its source. Arithmetic validation cannot establish that web data is current.
- Confirm historical source files are unchanged. Review the diff; only append reports/manifest entries unless making a separately justified tooling fix.
- Open a local browser at desktop and mobile widths if available. Check filters, sorts, history range, comparison selections, lineup duplicate rejection, opponent alternatives and navigation. If no browser is available, state that visual QA was not performed.
- Validate schema and exact arithmetic after any scoring or lineup algorithm change. Never weaken a failing check just to publish.

## 12. Commit, deploy, confirm

Commit the new report, manifest and intentional documentation/tool changes with a message such as "Add 2026 Week 6 Sunday pregame report". Use a branch/PR unless the scheduler has explicit direct-publish authorization. Do not force push or silently merge around repository rules.

After an authorized merge/push to main, check Actions: build must pass and deploy must succeed. Open the published address, verify the new report's as-of label and the previous archive entries. A successful git push is not proof the website deployed.

For failures: source unavailable → keep missing/stale markers; build failure → fix before publishing; Pages not configured → enable it using README; protected main → leave a PR; deployment failure → retain last working site and report the job error. Re-run deployment after the cause is fixed, without changing evidence timestamps.

Rollback by selecting an earlier manifest latest ID in a new commit and rebuilding. Keep newer reports in the archive and note why the homepage was rolled back.

## 13. Scheduled-run final response

Return: season/week and evidence cutoff; top lineup decisions and deadlines; newly confirmed news; fields still missing/stale; actual versus optimum if a results run; source/report path; commit or PR link; validation and deployment status; next required check. Be explicit if the run only prepared a PR or could not publish. Never claim a schedule, access grant or live refresh that was not installed and verified.
