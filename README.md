# Ringer Wise Guys Betting Dashboard

A dashboard tracking the Ringer Wise Guys overall record, per-host splits, and breakdowns by bet type and sport.

> Not affiliated with or endorsed by The Ringer. Built by a fan!

**Live:** https://wiseguysbets.pages.dev/

## How it works

Best bets and futures are tracked in a spreadsheet, maintained outside of this repo. Data flows in the following direction: `wiseguys_tracker.xlsx → build_data.py → data.json → index.html`. The tracker holds every best bet (host, type, odds, result); `build_data.py` reads from the sheet and writes to `data.json` (graded bets only, net units computed from odds + result); `index.html` is a self-contained vanilla dashboard that fetches `data.json` and renders in-browser.

## Updating the data

1. Add/grade bets in the tracker.
2. `python3 build_data.py`
3. Commit the tracker + `data.json` and push.

## Running locally

`python3 -m http.server 8000`, then open `localhost:8000` (opening the file directly won't work because the browser blocks local fetches).

## Data method

Right now the dashboard only tracks each hosts' bets from the "plays of the day" segment. Futures data has been added in the latest release. Live odds tracking coming soon.

Open to feedback on features and functionality!
