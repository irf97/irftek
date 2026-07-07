# Top-10 Playbook — biggest upside per unit of risk
*Ranked across all 88 scored names by URS = (bull₆₀ × capture) / bear₆₀ × window × liquidity × staleness — every input from the locked layers · validated with dedicated tree tests (2,000 paired worlds per sleeve) · entries always through the live gate; this file is the pre-registration, the app is the trigger · not investment advice*

## Architecture: two sleeves, instrument controls risk
**CORE (spreads, 3% NAV/trade, 2% for comp-class):** the URS top-10 — calm-IV, capture-strong, deep books. **SATELLITES (lotto L2, 1% NAV/trade, ≤3 concurrent):** the torque names the ranking correctly rejects as spread underliers — NVTS · HIMX · VICR — where the ≤$0.60 single-leg caps risk at the sleeve, TP 4× pre-print, exit print+1, no stops.

## The ranking (top of 88)
| rk | tk | URS | bull₆₀ | bear₆₀ | cap | cat | role |
|---|---|---|---|---|---|---|---|
| 1 | ARM | 0.65 | +12.1% | −14.9% | 0.80 | Aug 05 | core |
| 2 | AVGO | 0.63 | +11.0% | −13.9% | 0.80 | Sep 03 | core |
| 3 | TSM | 0.61 | +7.8% | −11.6% | 0.90 | **Jul 16** | core — ACTIVE NOW |
| 4 | NET | 0.58 | +13.2% | −14.9% | 0.65 | Jul 31 | core |
| 5 | ETN | 0.57 | +8.1% | −10.6% | 0.75 | Jul 31 | core |
| 6 | ANET | 0.55 | +10.9% | −14.9% | 0.75 | Aug 04 | core |
| 7 | NVDA | 0.54 | +9.0% | −14.9% | 0.90 | Aug 26 | core |
| 8 | MRVL | 0.52 | +13.4% | −18.2% | 0.70 | Aug 20 CONF | core |
| 9 | KLAC | 0.52 | +9.0% | −13.9% | 0.80 | Jul 30 | core |
| 10 | OKTA | 0.51 | +11.6% | −14.9% | 0.65 | Aug 26 | core |
| — | VRT 0.50 · GEV 0.50 · PWR 0.50 | | | | | | bench-warmers |
| sat | NVTS 0.28 · HIMX 0.31 · VICR 0.33 | | | | | | lotto sleeve |

## Core cards (uniform frame: enter COILED, T−10…T−1, spread ≈ +5%/+18% OTM, exp = cat+3wks, grade A/B only, exit R5 print+1 or EXTENDED flip, stance ≥45 to open, kill ⇒ flatten)
**TSM · Jul 16 · N1 itself** — the window is open NOW (Jul 8–15). The foundry toll prints first; its result IS the N1 resolution. Smallest-IV entry of the set.
**KLAC · Jul 30** — capex truth on cluster day. Pure A1 read; pairs with the FOMC morning — size ×0.7 if N3 resolves hawkish.
**NET / ETN · Jul 31** — cluster+1: coordination attach and grid backbone reporting into whatever N3 decided. Same ×0.7 hawkish rule.
**ANET · Aug 04** — rotation-window opener beside AMD; A5's first confirmation vehicle in the core.
**ARM · Aug 05** — #1 URS; royalty on the edge cycle. Pre-read: QCOM Jul 30 — a QCOM beat upgrades the card, a miss demotes it to half-size.
**MRVL · Aug 20 CONF** — N5's opening bell; the known-value structure (280/315-style) lives here.
**NVDA + OKTA · Aug 26** — same-day pair: treat as ONE exposure (combined ≤4% risk). NVDA is the referendum; OKTA is its shadow at better prices.
**AVGO · Sep 03** — conditional card: T−10 lands ON the MRVL print. Rule: open only if MRVL's reaction is constructive (N5 not resolved bear). The $16B bar does the rest.

## Satellite cards (lotto L2)
**VICR · Jul 28 CONF** — first satellite live: window Jul 17–23, ≤$0.60 call ~10–15% OTM, TP 4×, exit Jul 29 open into the FOMC. **HIMX · Aug 06** — glasses print, window Jul 27–Aug 3. **NVTS · Aug 10** — window Jul 29–Aug 5; the torque-#1/sizing-#17 name, played at 1% where that contradiction is safe.

## Sim receipts (dedicated runs, same seed/worlds)
| sleeve | mean | med | p5 | win | DD | trades/w |
|---|---|---|---|---|---|---|
| CORE-10 spread+tree | +21.2 | +19.5 | −3.6 | 89% | −3.4% | 9.5 |
| CORE-10 tree OFF | +21.0 | +20.6 | −7.3 | 85% | −3.6% | — |
| CORE-10 buy&hold | +2.7 | +7.5 | −28.9 | 72% | — | — |
| SATELLITES lotto L2 | +6.7 | +5.5 | −2.3 | 84% | −2.0% | 3.5 |
Combined book ≈ **+28 in-model**, tails roughly additive. Underlying risk is genuinely lower than the old spine (b&h p5 −28.9 vs −38.1) — the ranking works at the asset level.

## The rule the sim forced: cluster-concentration cap
Four core names print inside 48h (KLAC Jul 30 · NET+ETN Jul 31 · with MSFT/GOOGL/AMZN around them). Correlated event risk is why core-10's p5 (−3.6) isn't better than the spine's. **Cap: ≤2 open core positions with catalysts inside any 3-session window; excess candidates wait or halve.**

## Caveats, standing
URS's bull/bear inputs are the model's own 60-day paths — selection is only as good as the grammar. In-model results inherit every optimism flag from Sim_Report/Lotto_Report. TSM/ARM/ETN/KLAC/ANET/NET are Jan-knowledge names verified only by today's live prices — first prints re-grade them. The gate, not this file, opens trades.