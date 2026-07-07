# IrfTek Strategy v2 — The Anticipation Engine, Governed

*Session synthesis → operating rules. v1 = what the account actually did (Jun 2025 – May 2026). v2 = same engine, governed. Not investment advice.*

---

## 0. Evidence base (what this session proved)

| Finding | Evidence | Status |
|---|---|---|
| Entry edge is real | NVTS initiated 22 trading days before NVIDIA 800V news; INTC before the Sep-18 surprise | PROVEN (1 regime) |
| Edge is domain-specific | AI-power/infra +€1.13M · fintech/crypto/momentum −€1.09M | PROVEN |
| Exit edge is absent | Nov −€457k; €1.04M peak → €66 | PROVEN GAP |
| Overhead is fatal | €98.8k commissions ≈ 4× net profit; Oct = 619 trades, −€61.8k in one month | PROVEN GAP |
| Instrument mismatch is structural | ~1-month anticipation lead expressed in weekly far-OTM options | STRUCTURAL FLAW |
| Concentration is the edge signature | Top 3 names = 62% of gross profit; 58 of 89 names lost | REFRAME |

**Identity correction:** you are a **thesis-anticipation trader**, not an options trader. Options were one expression of the edge — usually the wrong one.

**Your own equation, applied (Eq 9):** Net = EdgeP&L − [no-edge churn + overhead] → +1,128,514 − [1,092,349 + 98,767] ≈ **+25k**. The engine produced a million; governance leaked a million. v2 exists to fix the bracket, not the engine.

---

## 1. The rule set

### R1 — Universe (circle of competence)
- **IN:** AI-power · AI-infra/cloud · memory/HBM · custom silicon/inference · governance/authority layer (research sleeve, small)
- **HARD BAN:** fintech momentum, crypto-mining, EV/China, meme names, thesis-less earnings gambles. This list cost −€1.09M. No exceptions mid-mania.

### R2 — Entry (two-layer gate)
- Pre-register the thesis **before** entry, 3 lines: *the tech · why now · catalyst + window*. Unwritten thesis = no position.
- Scanner state must be **COILED — ready** or **BREAKOUT (trigger)**. **EXTENDED = never initiate.**
- One layer alone (thesis without coil, coil without thesis) = watchlist, not position.

### R3 — Instrument ladder (duration ≥ lead time)
Your proven lead ≈ 1 month. A weekly option cannot hold a 22-day edge — being right *and* early expired worthless.
- Catalyst window ≤ 6 wk → options, **DTE ≥ 3× time-to-window-end** (floor: 60–90 DTE). Weeklies banned for anticipation trades.
- Thesis 3–12 mo → LEAPS or shares.
- Thesis 1–3 yr (mesh-layer plays) → **shares only**.

### R4 — Sizing (anti-mania)
- ≤ 10% of equity premium-at-risk per thesis · ≤ 30% aggregate options premium.
- Adds allowed only pre-catalyst and while state ≠ EXTENDED.
- Lottery sleeve (the far-OTM vice): **≤ 5%, capped, acknowledged.**

### R5 — Exits (the missing half — trade as session: settle → learn → dissolve)
- **The news is the exit.** Anticipation pays exactly once — when the asymmetry closes. The crowd you predicted is your liquidity: sell **50% into the first strength day**, 25% into the second; trail the rest (close below 20d EMA or state-flip).
- **Time stop:** window + 2 weeks with no catalyst → dissolve. Early ≠ immortal.
- **Circuit breaker (account level):** −20% from equity peak → halve gross exposure. −30% → core shares only. Applied to 2025, this preserves ~€700k of the peak.
- Every closed trade gets a 2-line journal entry (thesis right? timing right? instrument right?). Settle → learn → dissolve. No permanent residents.

### R6 — Overhead budget (Eq 9 as accounting)
- Commissions ≤ **1% of equity per month**. Budget hit = no new openings that month.
- **> 150 trades/month = churn alarm** (October was 619). Stop, review, resume next month.

### R7 — Portfolio shape (barbell)
- **Core 60%** — shares/LEAPS in top-conviction thesis names.
- **Catalyst sleeve 30%** — NVTS-pattern option trades under R2–R5.
- **Lottery ≤ 5%** — capped.
- **Hedge/cash 5–10%** — formalize the Apr–May discovery: aggregate premium > 20% → hold a tail hedge.

### R8 — Cadence & measurement
- Daily: `breakout_scanner.py --once` → act only on two-layer hits.
- Weekly: thesis journal update.
- Monthly: rerun the attribution (edge-zone vs no-edge P&L).
- Quarterly: regime check — where is the bottleneck now, how crowded is the edge?

### R9 — Falsification (kill criteria for the strategy itself)
- Two consecutive catalyst cycles with edge-zone P&L ≤ 0 → downgrade to shares-only until the journal shows lead time again.
- Journal reveals lead times were hindsight → the edge claim dies; retire the catalyst sleeve.
- Scanner < 40% useful signals after 20 firings → reweight or retire the tool.

---

## 2. Where to point it (June 2026)

Your 2025 alpha (AI-power) is 2026 beta — consensus, crowded, re-rated. The engine's next targets, less crowded first:

1. **Governance/authority layer** — CYBR, OKTA (+ MCP watch). Uncrowded; your Living Mesh call; thesis-early positioning before the market prices agent authority.
2. **Custom silicon / inference** — MRVL, AVGO, CBRS. The "NVIDIA validates a supplier" setup most likely to rhyme with NVTS.
3. **Memory/HBM** — MU. Structural supercycle, but already moving — wait for the coil, don't chase the run (R2).

---

## 3. Delta table — v1 → v2

| Dimension | v1 (what you did) | v2 (rule) |
|---|---|---|
| Entries | Intuition, unrecorded | Pre-registered thesis + scanner gate |
| Instrument | Weekly far-OTM calls | DTE ≥ 3× lead · LEAPS/shares by horizon |
| Exits | None — held through reversal | Sell-into-news · trail · time stop · circuit breaker |
| Sizing | Unbounded (Oct mania) | 10% / 30% / 5% caps |
| Universe | 89 names, anything moving | 5 domains + hard ban list |
| Overhead | €98.8k, unbudgeted | ≤1%/mo · churn alarm at 150 trades |
| Measurement | None | Journal + monthly attribution + kill criteria |

---

## One line

Same engine, governed: **anticipate inside the circle, buy time not lottery tickets, sell into the crowd you predicted, budget the overhead, and let every trade dissolve.**

---

*Handoff: strategy v2 supersedes implicit v1. Artifacts: IrfTek_Master_Workbook.xlsx (12 tabs, evidence + method), breakout_scanner.py (daily radar, selftest-verified, run locally — sandbox blocks market data). Next session: run scanner live on Termux, pre-register first v2 theses (governance layer + inference silicon), set the commission budget line in IBKR.*
