# League contract and score reconciliation

Source: the user's scoring-setting screenshots in this analysis thread. Preserve this contract until the user supplies changed settings. The user sometimes calls the format PPR, but the screenshot specifies **0.5 per reception**. Label it **custom half-PPR**.

## Roster

Nine starters: 1 QB, 2 RB, 2 WR, 1 TE, 2 FLEX (RB/WR/TE only), 1 D/ST. Six bench spots and one IR. No kicker and no superflex. Screenshot position limits: QB4, RB8, WR8, TE3, D/ST3. Confirm eligibility and lock rules with the current league before recommending a transaction.

## Offense

| Event | Points |
|---|---:|
| Passing yard | 0.02 |
| Completion | 0.2 |
| Passing TD | 4 |
| Interception thrown | -2 |
| Passing two-point conversion | 2 |
| Rushing yard | 0.08 |
| Receiving yard | 0.08 |
| Reception | 0.5 |
| Rushing or receiving TD | 6 |
| Rushing or receiving two-point conversion | 2 |
| 40+ yard rushing/receiving TD bonus | 1 |
| 50+ yard rushing/receiving TD bonus | 2 |
| 100–199 rushing yards in a game | 1 |
| 200+ rushing yards in a game | 2 |
| 100–199 receiving yards in a game | 1 |
| 200+ receiving yards in a game | 2 |
| Kickoff-return yard | 0.04 |
| Punt-return yard | 0.04 |
| Kickoff/punt return TD | 6 |
| Fumble recovered for TD | 6 |
| Fumble lost | -2 |
| Individual interception/fumble return TD | 6 |

Return yards matter: 100 credited return yards = 4 points before any receiving or rushing output. Verify that the player actually returns kicks/punts; do not credit touchbacks or team return yards to an individual. Check current NFL kickoff rules with official NFL sources each season and after changes. Rule changes alone do not establish a player's return workload.

Long-TD bonuses appear additive in the supplied history (Kittle's Week 4 total is consistent with a 50+ TD receiving both long-TD bonuses). Verify event lengths and the ESPN scoring detail when recalculating; do not infer an event solely to force the total to match. The 100–199 and 200+ yard bands are distinct.

## D/ST

| Event | Points |
|---|---:|
| Sack | 1 |
| Interception | 3 |
| Fumble recovered | 3 |
| Interception/fumble return TD | 3 |
| Kickoff/punt return TD | 6 |
| Blocked punt/FG returned for TD | 6 |
| Blocked punt/PAT/FG | 2 |
| Safety | 2 |
| Two-point return | 2 |
| One-point safety | 1 |

| Points allowed | Points | Total yards allowed | Points |
|---|---:|---|---:|
| 0 | 5 | Under 100 | 5 |
| 1–6 | 4 | 100–199 | 3 |
| 7–13 | 3 | 200–299 | 2 |
| 14–17 | 1 | 300–349 | Unconfirmed |
| 18–27 | Unconfirmed | 350–399 | -1 |
| 28–34 | -1 | 400–449 | -3 |
| 35–45 | -3 | 450–499 | -5 |
| 46+ | -5 | 500–549 | -6 |
| — | — | 550+ | -7 |

The unlisted middle bands were not visible in the supplied settings. Do not silently assume they are zero when independently recalculating D/ST. ESPN's credited points allowed may differ from the final scoreboard because of scoring attribution; use the fantasy scoring detail.

## Reconciliation protocol

1. Store **ESPN actual points**, **independently calculated points**, and **difference** as separate values.
2. Obtain complete passing completions/yards/TD/INT, rushing and receiving stats, TD lengths, return yards, conversions and fumbles lost. Short scoreboard lines omit categories.
3. Apply the exact league settings, rounding only the final display to two decimals.
4. Where facts are incomplete, label calculated points unavailable and preserve ESPN actuals. Never invent a missing stat.
5. Investigate differences with source details, then document any stat correction in a new report. Keep the old snapshot intact.
6. Do not compare ordinary full-PPR projections with these actuals without explicitly converting the scoring. Show any requested full-PPR benchmark in a separate column with its complete assumptions.

## Law of 10

Report the number of starters who reached 10, each player's known-week 10+ hit rate and their practical route to 10. Nine players at 10 = 90, but a 90-point total need not win. Do not restrict a high-upside QB to a 10-point target or pretend a D/ST has a guaranteed floor. Sample size and role changes must accompany hit rates.
