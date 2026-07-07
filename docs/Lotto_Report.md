# Lotto Battery — single-leg ≤ $0.60, timing does the work
*Same 3,000 stub worlds as Sim_Report (seed 7, paired) · single calls (puts in L4) with model premium ≤ $0.60 · entries: COILED + stance ≥ 55 + 3–8 days to print · 1% NAV per trade, max 3 concurrent · cheap-option costs modeled (min 25%-capped 4¢ slippage + 2%) · `tree_sim.py --lotto` · self-consistency test, not market truth · not investment advice*

## The four variants, identical worlds
| variant | rule | result | trades/w | trade-win | avg winner | neg-worlds |
|---|---|---|---|---|---|---|
| L1 | hold → print+1 (pure R5) | mean +77.5 · med +39.5 · p5 -4.3 · p95 +274.5 · win 87% | 9.0 | 44% | +1564% | 13% |
| L2 | + take-profit 4× pre-print | mean +44.6 · med +40.5 · p5 +6.9 · p95 +96.5 · win 99% | 13.5 | 66% | +458% | 1% |
| L3 | + 40% stop-loss | mean +80.8 · med +42.7 · p5 -3.9 · p95 +280.7 · win 88% | 9.6 | 42% | +1555% | 12% |
| L4 | tree-directional: + puts after a kill | mean +54.1 · med +50.0 · p5 +16.2 · p95 +105.0 · win 100% | 16.8 | 66% | +436% | 0% |
| — | baseline: spread system + tree | mean +21.0 · med +18.8 · p5 -1.3 · p95 +50.2 · win 93% | 10.3 | 63% | +75% | 7% |

## Findings
**1 · Your thesis, quantified — selling right IS the risk control.** L1 vs L2: same median (~+40), but the take-profit flips the tail — p5 goes **−4.3 → +6.9**, losing-world share **13% → 1%**. The cost: mean drops +77 → +45 because the TP sells the moonshots (avg winner +1,564% → +458%). That is the exact trade you're choosing between: consistency (L2) or lottery mass (L1). Both beat the spread baseline in-model at 1% sizing.
**2 · Stops are theater on lottos.** L3 ≈ L1 on every stat. A ≤$0.60 option rarely crosses a 40% stop before resolving to death or glory — the stop harvests noise, not risk. Discipline lives in the exit-into-strength, not the stop.
**3 · The edge decomposes: ramp + gap.** A4-off (no anticipation drift) collapses spread P/L to ~+3, but lottos keep **+13–16 mean (L1 median just +2.0)** — cheap options are long *event-gap variance* itself. So the lotto book leans on TWO assumptions: A4 (ramp) and the gap-size distribution (A6-adjacent). If real gaps run smaller than 2.2–4×ATR on beats, this halves.
**4 · Sizing is the whole 'risk isn't high' claim.** At 1%/trade, worst-case per trade = −1% NAV and mean DD ≈ −2%; at 2% the L2 book compounds to +113 mean (p5 +13) in-model. The claim holds **as a sizing statement**, not an instrument statement: the instrument is 100%-loss-prone (trade-win 44% on L1); the sleeve makes it survivable.

## Honest optimism flags
L4's put entries are priced at seed IV — a real crash spikes put premia before you buy, so L4's 100% world-win is flattered; direction valid, magnitude not. COILED stubs fire at 72% quality in bull moods — real scanners are noisier. Fills on nickel-wide books will be worse than the modeled 4¢+2%. And the world remains the system's own model: this grades the *rules* (entry window, TP, sleeve), not the market.

## Operating translation (if adopted)
R4 lotto sleeve: ≤1% NAV/trade, ≤3 concurrent · entry only COILED + stance ≥55 + T−8…T−3 · **TP at 4× pre-print, else R5 exit at print+1** · no stop-loss (accept the −100%s; the sleeve caps them) · puts post-kill only with the IV caveat priced in. For a truly *low-trade* book, cap total entries (e.g., 6/window) — economics stay L1/L2-shaped, count drops.