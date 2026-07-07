# Autonomy — how the tool runs without anyone

**v5.0 "zelfstandig".** Every derived layer is computed client-side, on every load, from three sources the tool owns:

| source | what | who updates it |
|---|---|---|
| **live feed** | 105 quotes · chains · scanner states (`terminal_data.js`) | GitHub Actions cron, weeknights 21:15 UTC — no human, no AI |
| **knowledge base** | per-name catalyst date/CONF, MULT, capture, IV override, thesis | you, inside each name's detail view |
| **settings** | horizon, filter bands, risk caps, macro dates, assumption switches | you, in the ⚙ tab |

**Derived at load (nothing pre-baked):** rolling model paths (`pathFor`: horizon trading-days from *today*, front-run ramps by class lag, print gaps, digestion, macro dents, day codes) · the focus book (`focusList`: the moneyness+delta filter over the whole universe, live-priced cards with strike/Δ/premium/window/node-gate) · stance (editable tree × resolutions) · calendar · gates. Change any input and everything downstream reprices immediately — that's the point.

**Assumption register as machinery:** killing an assumption in ⚙ multiplies every torque multiplier by its factor (e.g. A9 hike-kill ×0.7) — the register is no longer prose, it's a circuit breaker.

**Your config is a file, not a chat.** The ⚙ DATA card exports `{cfg,kb,ak,tree,res}` as one JSON blob; paste to import on any device. localStorage persists it per-browser on the live site.

**Three duties remain, and they are human duties, not AI ones:**
1. **Verify catalyst dates at T−10** — edit them in the name view (the VICR ritual, now a date field).
2. **Review MULT/capture monthly** — steppers in the name view; the numbers are your judgment, the tool only propagates it.
3. **Resolve tree nodes nightly** — tap the branch that fired; edit dates/weights/probabilities as the world drifts.

**What stays frozen on purpose:** `Sixty_Day_Paths.csv` and the R8 journal are the *pre-registration* — the locked Jul-7 bet. The app is the living tool; the CSV is the thing that gets graded. Do not confuse them: falsification requires one artifact that never rolls.
