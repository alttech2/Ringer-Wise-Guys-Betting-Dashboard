# Ringer Wise Guys Betting Dashboard

A dashboard tracking the betting picks from *The Ringer's* **Wise Guys** podcast, including the crew's best-bet record, per-host splits, breakdowns by bet type and sport, plus a full futures board.

> Not affiliated with or endorsed by The Ringer. Built by a fan!

**Live:** https://wiseguysbets.pages.dev/

## What's on it

The dashboard has two views, toggled from the header:

- **Best Bets** — the crew's overall record, per-host splits ranked by net units, a cumulative-units chart, and breakdowns by bet type and sport. Pending bets are flagged and shown but don't count toward the record.
- **Futures** — a sport-aware board covering the NFL and College Football. Filter by sport, then by division (NFL) or conference (College Football), across these categories:
  - **Win Totals** — a consensus board showing each host's over/under lean per team, tagged *Family Play* (everyone agrees) or *Split*.
  - **Division Winners** (NFL) / **Playoff Props** (College Football) — staked plays to win the division, make/miss the playoff, etc.
  - **Player Props** and **Longshots** — staked props and higher-odds swings (awards, order-of-finish, parlays, Heisman).

  A summary strip up top tracks open predictions, staked plays, longshot count, and max units at stake. Live odds are a placeholder for now (see below).

## How it works

Best bets and futures are tracked in a spreadsheet (`wiseguys_tracker.xlsx`) that's **maintained outside this repo**. Data flows in one direction:

```
wiseguys_tracker.xlsx  →  build_data.py  →  data.json  →  index.html
```

- The **tracker** holds every best bet (host, type, odds, result) on one tab and every futures pick on another (sport, team, division/conference, category, line, selection, stake, odds, result).
- **`build_data.py`** reads the sheet and writes **`data.json`** — computing net units from odds + result for graded best bets, and grouping futures per sport into the boards the dashboard renders. It lives in the repo for transparency, but it's **run locally, not by the site**—the only thing the live site loads is `data.json`.
- **`index.html`** is a self-contained vanilla HTML/CSS/JS dashboard (no build step, no dependencies) that fetches `data.json` and renders everything in-browser.

The "Last updated" stamp in the footer is written by `build_data.py` at build time (stored as UTC, displayed in ET).

## Updating the data

1. Add or grade picks in the tracker.
2. `python3 build_data.py`
3. Commit `data.json` (and `index.html` if the UI changed) and push.

Hosting is on Cloudflare Pages, which auto-deploys on push. The tracker itself stays local and out of the repo.

## Running locally

```
python3 -m http.server 8000
```

Then open `localhost:8000`. Opening `index.html` directly won't work — the browser blocks the local `data.json` fetch over `file://`.

## Methodology

- **Best bets:** only the designated "plays of the day" go-around picks count, not early bonus picks or casual leans. Each best bet is 1 unit; a parlay counts as a single bet for that host.
- **Futures:** win-total picks are logged as no-stake **leans** (predictions), while division winners, playoff props, player props, and longshots are **staked plays** (1 unit each). Everything is pulled from the crew's division and conference preview episodes.
- Pending results are flagged explicitly rather than left blank.

Live odds tracking is coming soon (the column is wired up and shows "soon" until an odds feed is connected).

Open to feedback on features and functionality!
