# IrfTek Trading System — Setup & Operating Manual

One program that runs the loop your edge needs: **calendar → price state → two-layer gate → graded option setups**, with a mobile HTML terminal on top. Built from your own backtest's conclusion: the anticipation edge is real (entry), and the leaks were exits, instrument duration, and overhead — so the tooling automates the gates and leaves sizing human.

```
irftek.py brief  ─►  fetch quotes/history ─► scan states ─► gate verdicts ─► graded setups (GO names)
irftek.py feed   ─►  terminal_data.js  ─►  catalyst_terminal.html (auto-set state chips, live chains)
```

---

## Quick start — Termux (Android), under 5 minutes

```bash
pkg install git python          # once
mkdir -p ~/irftek && cd ~/irftek
# copy these files here (Claude downloads / your sync folder):
#   irftek.py  catalyst_terminal.html  requirements.txt  setup.sh
#   (optional) watchlist_config.py  irftek_watchlist.csv
bash setup.sh                   # installs deps + runs the 14-check selftest
bash run.sh all                 # feed everything + launch the app in the browser
bash run.sh shortcut            # optional: home-screen button (Termux:Widget)
```

**Windows:** install Python 3.10+ → `pip install -r requirements.txt` → `python irftek.py selftest` → `python irftek.py brief`. Same files, same commands.

First success = `SELFTEST: 19 passed, 0 failed`, then a brief table sorted GO-first.

---

## Standalone app mode (no Termux needed after install)
`irftek_app.html` is now fully self-contained: open it anywhere (phone browser, laptop, sent to a friend) and tap **⟳ refresh** — it fetches delayed prices + 1-year history through public relay endpoints, runs the breakout scanner **in the browser**, auto-sets states, and derives each name's bear/base/bull scenarios from its own live volatility. Open any name and tap **load live option chain** to price setups off the real (delayed) CBOE chain. The Termux feed (`run.sh`) remains as an optional backup data source (auto-merged if `terminal_data.js` exists) and for exchange-direct quotes.

## Daily runbook

**Morning (one command):**
```bash
python3 irftek.py brief                 # core tier (23 names)
python3 irftek.py brief --tier event    # inside catalyst windows (Aug prints etc.)
```
Read the GATE column top-down: **GO** = thesis window open + COILED/BREAKOUT → the setups print below, R3⚠-flagged. **WINDOW-SOON** = coiled, window opens ≤2 wks — prepare, don't enter. **WATCH+** = in window, still basing. Everything else = stand down. Scanner warnings (`!` lines: low-volume breaks, distribution zones) print inline.

**Before entering anything:** `python3 irftek.py setups TICKER` — full graded table with live chain premiums where they exist (`chain` tag) vs model (`model` tag). EST catalyst dates within 10 days print a **confirm T−7** warning — check IBKR's calendar before trusting a weekly.

**Event day (the R5 ritual):** the news is the exit. Sell 50% into the first strength; the program will show the name flip to EXTENDED next scan — that flip is *take-profit confirmation*, never an add.

**Terminal on the phone:**
```bash
python3 irftek.py feed          # 7 card names, ~30s
python3 irftek.py feed --tier all   # full 67, ~5 min
```
Then open `catalyst_terminal.html` (same folder) in the browser. Header flips to **LIVE**; card prices, chain IV, and **state chips auto-set from the scanner**. Everything cyan stays editable.

**Weekly:** `brief --tier component` (teardown/design-win news), `brief --tier bench` (glance), journal entries per R8, and re-run `selftest` after ANY edit to the file.

---

## Command reference

| Command | What it does |
|---|---|
| `brief [--tier core\|event\|component\|bench\|all] [--mock]` | Fetch → scan → gate → setups on GO names. `--mock` = offline pipeline demo |
| `scan --tier X` | States + gate only (no options math) |
| `setups TICKER` | One name: state, gate verdict, full graded contract table |
| `feed [--tier terminal\|...\|all]` | Write `terminal_data.js` (quotes + chains + states) for the HTML |
| `selftest` | 14 offline checks: BS parity, chain parser, state machine, engine, gate |
| `--wbear/--wbase/--wbull N` | Scenario probability weights (default 30/45/25) on `brief`/`setups` |

## Maintenance (all edits are one-liners in `irftek.py`)

- **Confirm/adjust a catalyst date:** edit the `CAT` dict entry (`"MRVL":("2026-08-20", "...", "CONF")`). Flip `EST`→`CONF` when verified; every gate verdict updates downstream.
- **Add/remove tickers:** `TIERS` dict (or keep using `watchlist_config.py` — it overrides when present). Add a `CAT` entry or the name gates as NO-DATE by design.
- **Tune a name's model:** `IV_SEED` (used only when no live chain IV) and `SCN_SEED` (bear/base/bull %).
- **After any edit:** `python3 irftek.py selftest` — 5 seconds, catches regressions. This rule has already caught real bugs twice this build.

## Troubleshooting

| Symptom | Cause → fix |
|---|---|
| `states unavailable` in brief | network issue or Yahoo throttling → retry; scanner itself is pure stdlib now |
| Nasdaq quote/chain empty, `(yahoo)` tag | api.nasdaq.com rate-limited you → fallback already engaged; chains may be absent, engine prices via model |
| A microcap shows only `model` setups | No liquid chain exists — that IS the verdict: shares-only or skip (Component map rule) |
| `403 Host not in allowlist` | You're in a sandboxed environment (e.g. Claude) — run on Termux/PC; `--mock` proves logic offline |
| Weekly option on an EST date | Don't. Confirm T−7 (the brief warns you). A wrong date on a weekly is an unforced zero |

## File map

**Active:** `run.sh` / `run.bat` (one-tap launcher: feed → serve → open; `stop`/`shortcut` verbs) · `irftek.py` (everything) · `irftek_app.html` (THE app v3 — Brief/Mesh/Calendar/Rules, target mode, slice metric, path sparklines, open after `feed --tier all`, Add-to-Home-Screen for an icon) · `catalyst_terminal.html` (7-card quick view) · `requirements.txt` · `setup.sh` · `watchlist_config.py` (optional override) · `irftek_watchlist.csv` (IBKR import — Client Portal → Watchlist → import → syncs to mobile).
**Superseded, kept for reference:** `breakout_scanner.py`, `nasdaq_feed.py`, `test_scanner.py` (the 18-test battery that hardened the scanner logic now embedded), `quant_system.py`, `options_scorer.py`, `quant_cockpit.html`.
**Reference docs:** `IrfTek_Strategy_v2.md` (the rules) · `IrfTek_Master_Workbook.xlsx` (evidence: backtest, attribution, anticipation proof) · the maps (`Sixty_Day_X_Map`, `Extrinsic_90Day_Rotation`, `The_Ownership_Stack`, `Component_Layer_Map`, `Apple_NVIDIA_Laptop_BOM`).

## The rules the program deliberately does NOT automate

The card to keep human, from your own backtest: **R4** lotto sleeve ≤5% total, never refilled mid-window · **R6** commissions ≤1%/mo, >150 trades/mo = churn alarm · **R5** sell into the news, time-stops not price-stops · **R7** barbell (core 60 / catalyst 30 / lotto 5 / hedge 5–10) · **R8** journal every entry (thesis, timing, instrument) · **R9** two dead catalyst cycles → shares-only until the journal shows lead time again. The program names trades; **you size them.** Nothing here is investment advice.

## Trust boundaries (what's proven vs seeded)

Proven by tests: BS math (parity-locked), state machine (18-test battery + embedded checks), chain parser, gate logic, engine behaviors (spread-beats-naked at rich IV, MU-class SKIPs). Seeded, needs your live confirmation: EST catalyst dates, IV seeds (paste live IV via terminal), scenario magnitudes, small-cap prices. The out-of-sample test of the *edge itself* is the Aug–Sep catalyst cluster — the journal decides.
