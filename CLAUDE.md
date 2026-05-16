# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Environment

Python scripts here depend on `invisible_playwright`, which is installed in a venv at `/home/victor/inv-env` (Python 3.14). The system `python3` is *not* this venv — invoke scripts with the venv interpreter:

```bash
/home/victor/inv-env/bin/python3 google_search.py -q "your query"
/home/victor/inv-env/bin/python3 open_page.py
```

There is no `requirements.txt`, no test suite, no linter config, and no build step.

At the start of any new prompt create a backup of `google_search.py` named `google_search.py.bak`
```bash
cp google_search.py google_search.py.bak
```

## What `invisible_playwright` provides

`InvisiblePlaywright` is a sync context manager that yields a stealth-patched Firefox `browser` object. Usage pattern shared by both scripts:

```python
from invisible_playwright import InvisiblePlaywright

with InvisiblePlaywright() as browser:
    page = browser.new_page()
    page.goto(url, wait_until="domcontentloaded")
```

Optional kwargs: `seed=<int>` (deterministic fingerprint), `humanize=True` (Bezier-trajectory cursor motion on `.click()`). The package source lives under `/home/victor/inv-env/lib/python3.14/site-packages/invisible_playwright/` — read it directly when behavior is unclear, since it's a thin wrapper around Playwright's sync API.

## Scripts

- `google_search.py` — paginated Google SERP scraper. Navigates directly to `/search?q=...&start=N` per page rather than typing into the search box (the `.bak` file is the older, search-box-driven version kept for reference). Dismisses the EU "Accept all" consent button on page 1 only. Dedupes URLs across pages and stops when a page returns zero new results.
- `open_page.py` — opens antcpt.com/score_detector (a bot-score check) and sleeps 10s. Used as a manual smoke test of the stealth profile.

When extending Google-scraping behavior, note the selector contract: results are matched as `div#search a:has(h3)` with `href` starting with `http`. If Google's DOM changes, both the `wait_for_function` predicate and the locator need updating together.
