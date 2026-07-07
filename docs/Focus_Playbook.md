# Focus Playbook — the real strategy (v2, primary)
*The book: 10 filtered single-leg names. Big caps are instruments now — watched, not traded. Spec: **10–15% OTM call · Δ 0.30–0.55 · 1% NAV/trade · ≤3 concurrent · enter on COILED inside the window with stance ≥55 · TP 4× pre-print · else exit print+1 · no stops · kill ⇒ flatten.** All dates EST — verify each at T−10. Not investment advice.*

## How the spec got here (three artifacts killed, on the record)
$0.60 absolute → 30–40% OTM junk board-wide (operator caught it) → premium ≤1.5% of spot → rejected HIMX at 4.5% → 7% sanity ceiling → rejected NVTS at 9% (IV 95 is just expensive). **Surviving invariant: moneyness + delta.** Premium-as-%-of-spot was always a memory of the 2021 price class.

## The ten (score = MULT × IV-fit × conf × liquidity × survival)
| rk | tk | px | card | Δ | prem | window | print | node rule |
|---|---|---|---|---|---|---|---|---|
| 1 | NVTS | 13.90 | ~15.5C | 0.44 | $1.25 | 07-29→08-06 | 08-10 EST | N3-gated |
| 2 | HIMX | 13.45 | ~15C | 0.35 | $0.61 | 07-27→08-04 | 08-06 EST | straddles N3 ·½size |
| 3 | SOUN | 6.84 | ~7.5C | 0.45 | $0.62 | 07-23→08-04 | 08-06 EST | straddles N3 ·½size |
| 4 | IONQ | 44.84 | ~50C | 0.44 | $4.05 | 07-23→08-04 | 08-06 EST | straddles N3 ·½size |
| 5 | SERV | 6.09 | ~7C | 0.43 | $0.57 | 07-23→08-04 | 08-06 EST | straddles N3 ·½size |
| 6 | RR | 1.91 | ~2C | 0.55 | $0.29 | 07-30→08-11 | 08-13 EST | N3-gated |
| 7 | SMCI | 25.54 | ~28.5C | 0.38 | $1.45 | 07-24→08-03 | 08-05 EST | straddles N3 ·½size |
| 8 | AI | 8.99 | ~10C | 0.45 | $0.87 | 08-19→08-31 | 09-02 EST | N3-gated |
| 9 | AIP | 31.84 | ~35.5C | 0.39 | $2.02 | 07-24→08-03 | 08-05 EST | straddles N3 ·½size |
| 10 | SYM | 41.63 | ~46.5C | 0.36 | $2.09 | 07-22→08-03 | 08-05 EST | straddles N3 ·½size |
| 11–12 | ONDS · CEVA | | | | | | | alternates if a top name fails the T−10 date check |

**Flags:** RR at $1.91 is penny-adjacent — confirm the chain has real open interest before it counts; SMCI is a post-collapse name — same check. Six of ten print Aug 5–6: **the cluster cap applies — ≤3 concurrent means you CANNOT hold all of them; rank order decides.**

## Tree receipts (2,000 dedicated worlds on this exact roster)
| variant | mean | med | p5 | win | neg-worlds | trades/w |
|---|---|---|---|---|---|---|
| L1 hold→print+1 | +8.5 | +5.8 | −3.0 | 70% | 30% | 4.3 |
| **L2 +TP 4× (the card)** | **+7.0** | **+5.8** | **−3.0** | **79%** | **21%** | **5.1** |
| L4 +puts post-kill | +10.5 | +9.8 | −0.4 | 94% | 6% | 8.0 |
L4's put overlay is the risk killer but its entries are priced at calm IV — flattered; use puts only where the put chain is actually liquid (SYM/SMCI candidates), never on the penny names.

## The one-line truth
**A4-off collapses this book to +1.5 mean / 54% win.** At IV 95–120 the premium already prices the gap — there is no event-variance cushion here. This strategy IS the bet that smart money front-runs these prints. If coils don't form inside the windows, the correct position is none.

## Watch-only panel (read-throughs, not trades)
TSM Jul 16 → grades the whole tape · MSFT/GOOGL/AMZN Jul 28–30 → N3 · AMD Aug 4 → opens the rotation the focus book lives in · MRVL/NVDA Aug 20–26 → N5 · AVGO Sep 3 → N6. Their prints move OUR names; their options don't fit our spec.