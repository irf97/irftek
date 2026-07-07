# Sim Report — stub-world Monte Carlo of the full system
*3,000 tree-sampled 44-day worlds (Jul 7 → Sep 4) · 12-name spine, live Jul-7 anchors · agent = the system's own rules (gate → engine grade → R4 sizing → R5 exits → tree de-risking) · spreads priced with real Black-Scholes, IV crush post-event, 3% round-trip costs · seeded, reproducible (`tree_sim.py --trials 3000 --seed 7`) · **self-consistency test: the world generator IS the system's model** · not investment advice*

## Headline distributions (net % on NAV over the window)
| agent | result                                                       | mean DD |
|---|---|---|
| **system + tree** | mean +21.0 · med +18.8 · p5 -1.3 · p95 +50.2 · win 93% | -2.8% |
| system, tree OFF | mean +21.8 · med +21.5 · p5 -3.9 · p95 +51.0 · win 88% | -3.6% |
| buy & hold basket | mean +2.6 · med +8.1 · p5 -38.1 · p95 +28.6 · win 71% | — |

~10 trades per world · per-trade win ≈ 63% with ~+75% avg winner on debit — the asymmetry of defined-risk spreads, not a crystal ball, carries the portfolio win rate.

## By scenario class — where the tree earns its keep
| class | share | tree | flat | b&h |
|---|---|---|---|---|
| CLEAN-BULL | 15.0% | **+29.8** (win 99%) | +31.7 | +13.2 |
| DETOUR-hawkish | 23.0% | **+24.5** (win 98%) | +27.2 | +11.6 |
| FROTH | 10.6% | **+14.9** (win 94%) | +15.9 | +10.5 |
| KILL-N3 | 20.1% | **+3.0** (win 72%) | +0.3 | -35.0 |
| KILL-N5 | 8.4% | **+19.6** (win 97%) | +19.8 | -1.8 |
| MIXED | 22.9% | **+30.7** (win 100%) | +32.2 | +17.4 |

**Reading:** in benign worlds the tree costs ~1pt of mean (its insurance premium). In **KILL-N3 worlds (20% of all futures)** it returns **+3.0 vs +0.3 flat vs −35.0 buy-&-hold**, and it compresses the left tail (p5 −1.3 vs −3.9) and drawdown (−2.8 vs −3.6). The tree is not an alpha layer — it is a cheap ruin-avoidance layer, exactly as designed.

## The ablation that matters — A4 off (anticipation drift removed)
| agent | result |
|---|---|
| system + tree | mean +3.3 · med +1.4 · p5 -9.0 · p95 +21.3 · win 59% |
| system, tree OFF | mean +3.0 · med +1.2 · p5 -10.4 · p95 +22.0 · win 56% |
| buy & hold | mean -5.9 · med -0.9 · p5 -40.7 · p95 +15.4 · win 46% |

Kill the smart-money front-run and the edge collapses to ≈ +3% with a 59% win rate — statistically alive, economically marginal after costs. **The system's P/L is conditional on A4 being true in the real world.** The sim cannot prove A4; only your live coil-by-T−10 observations can. This is the register, quantified.

## Per-name attribution (3,000 worlds)
| name | trades | avg trade P/L | trade win |
|---|---|---|---|
| AMD | 3191 | +66.6% | 59% |
| GEV | 3165 | +80.4% | 63% |
| VRT | 3127 | +79.0% | 66% |
| VICR | 3116 | +68.9% | 63% |
| HIMX | 3111 | +52.1% | 57% |
| NVTS | 2856 | +61.5% | 63% |
| CRWV | 2800 | +74.9% | 66% |
| MRVL | 2484 | +87.5% | 66% |
| AVGO | 2424 | +97.1% | 67% |
| OKTA | 2382 | +88.3% | 64% |
| NVDA | 2350 | +94.9% | 63% |

MU: **zero trades across all worlds** — the no-date/out-of-window gate held (its print sits outside the window). Anchors (AVGO/NVDA/MRVL/OKTA) show the best per-trade economics (fewer, later, bigger); components trade more, win less per shot — matching the torque-vs-sizing doctrine.

## Honest limits
World = the system's own assumptions (grammar, tree priors, beat rates conditioned on mood) → this validates **rule quality and internal coherence**, not market truth. Fills are BS-mid with 3% costs — thin chains (NVTS-class) will be worse. Seed-stability checked (means within 0.2pt across seeds). Upgrade path: replay against realized paths after Sep 4 (R8 journal) — the only test that grades the assumptions themselves.