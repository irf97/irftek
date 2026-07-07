#!/usr/bin/env python3
"""tree_sim — stub-world Monte Carlo for the IrfTek system.
Samples the Event Tree to spawn alternate 44-day worlds, drives per-name prices with
the locked grammar (front-run ramps, print gaps, 45% digestion, FOMC dents), then lets
the SYSTEM'S OWN RULES trade each world. Reports net %P/L distributions, tree-ablation
delta, kill-world protection, and buy&hold benchmark.
EPISTEMIC STATUS: self-consistency test. The world generator IS the system's model —
this measures whether the RULES extract expectancy from the assumed world (gating,
sizing, exits, tree de-risking), not whether the assumptions match reality.
Not investment advice."""
import math, random, json, argparse, statistics as st
import datetime as dt

# ---------- calendar ----------
START = dt.date(2026, 7, 7)
DAYS = []
_d = START
while len(DAYS) < 44:
    if _d.weekday() < 5: DAYS.append(_d)
    _d += dt.timedelta(days=1)
IDX = {d: i for i, d in enumerate(DAYS)}
FOMC_I = IDX[dt.date(2026, 7, 29)]

# ---------- spine (live anchors from the Jul-7 feed) ----------
NAMES = {
 #        px      IV  cat        cls
 "NVTS": (15.38,  95, "2026-08-10", "comp"),
 "MRVL": (250.59, 55, "2026-08-20", "attach"),
 "CRWV": (142.10, 85, "2026-08-12", "attach"),
 "AVGO": (398.50, 42, "2026-09-03", "anchor"),
 "AMD":  (555.12, 48, "2026-08-04", "attach"),
 "NVDA": (208.40, 42, "2026-08-26", "anchor"),
 "OKTA": (75.20,  45, "2026-08-26", "attach"),
 "HIMX": (10.48,  65, "2026-08-06", "comp"),
 "VICR": (253.74, 60, "2026-07-28", "comp"),
 "VRT":  (288.90, 55, "2026-07-22", "comp"),
 "GEV":  (1044.1, 42, "2026-07-22", "comp"),
 "MU":   (986.00, 75, "2026-09-21", "attach"),  # print OUTSIDE window -> must never trade
}
NAMES_EXT = {
 "ARM":  (306.835, 45, "2026-08-05", "attach"), "TSM": (431.7991, 35, "2026-07-16", "anchor"),
 "NET":  (257.49, 45, "2026-07-31", "attach"), "ETN": (390.06, 32, "2026-07-31", "comp"),
 "ANET": (164.15, 45, "2026-08-04", "attach"), "KLAC":(212.945, 42, "2026-07-30", "comp"),
}
NAMES.update(NAMES_EXT)
ATR = {t: max(2.0, min(8.0, iv / 16)) / 100 for t, (_, iv, _, _) in NAMES.items()}
LAG = {"anchor": 15, "attach": 12, "comp": 8}

# ---------- the tree (mirrors docs/Event_Tree.md) ----------
TREE = [
 ("N1", IDX[dt.date(2026,7,16)], [(.60,"bull",{}), (.40,"bearm",{"delay":5})]),
 ("N2", IDX[dt.date(2026,7,27)], [(.55,"bull",{}), (.35,"chop",{}), (.10,"bear",{"halve":1})]),
 ("N3", IDX[dt.date(2026,7,30)], [(.50,"bull",{}), (.30,"bearm",{"dent":1,"m":.85}),
                                   (.13,"kill",{"m":.70}), (.07,"kill",{"m":.70})]),
 ("N4", IDX[dt.date(2026,8,12)], [(.55,"bull",{}), (.30,"chop",{}), (.15,"bear",{"froth":1})]),
 ("N5", IDX[dt.date(2026,8,26)], [(.60,"bull",{}), (.30,"chop",{}), (.10,"kill",{"m":.70})]),
 ("N6", IDX[dt.date(2026,9,3)],  [(.60,"bull",{}), (.25,"chop",{}), (.15,"bear",{})]),
]
MOODV = {"bull": 1.0, "chop": 0.0, "bearm": -0.5, "bear": -1.0, "kill": -1.0}
W = {"N1": 2, "N2": 1, "N3": 3, "N4": 2, "N5": 3, "N6": 2}

# ---------- Black–Scholes ----------
def _phi(x): return 0.5 * (1 + math.erf(x / math.sqrt(2)))
def bs_call(S, K, Ty, iv, r=0.04):
    if Ty <= 1e-6: return max(0.0, S - K)
    sq = iv * math.sqrt(Ty)
    d1 = (math.log(S / K) + (r + iv * iv / 2) * Ty) / sq
    return S * _phi(d1) - K * math.exp(-r * Ty) * _phi(d1 - sq)
def bs_put(S, K, Ty, iv, r=0.04):
    if Ty <= 1e-6: return max(0.0, K - S)
    return bs_call(S, K, Ty, iv) - S + K * math.exp(-r * Ty)
def spread_val(S, K1, K2, days_rem, iv):
    Ty = max(days_rem, 0) / 365
    return bs_call(S, K1, Ty, iv) - bs_call(S, K2, Ty, iv)

# ---------- world generation ----------
def sample_tree(rng):
    res, effects = {}, {"m": 1.0, "delay": 0, "dent": 0, "halve": 0, "froth": 0, "kill_at": None}
    for nid, di, brs in TREE:
        u, acc = rng.random(), 0.0
        for bi, (p, mood, eff) in enumerate(brs):
            acc += p
            if u <= acc:
                res[nid] = (bi, mood, di)
                if mood == "kill" and effects["kill_at"] is None: effects["kill_at"] = di
                if "m" in eff: effects["m"] = min(effects["m"], eff["m"])
                for k in ("delay", "dent", "halve", "froth"): effects[k] = effects[k] or eff.get(k, 0)
                break
    return res, effects

def mood_at(res, i):
    m, last = 0.05, None
    for nid, dend, _ in TREE:
        if i > dend and nid in res: last = res[nid][1]
        if i <= dend:
            break
    return MOODV.get(last, 0.05) * 0.6 if last else 0.05

def gen_world(rng, no_ramp=False):
    """Returns per-name daily closes + state stubs + print outcomes."""
    res, eff = sample_tree(rng)
    world = {"res": res, "eff": eff, "px": {}, "state": {}, "gapz": {}}
    for t, (S0, iv, cat, cls) in NAMES.items():
        atr = ATR[t]
        ci = IDX.get(dt.date.fromisoformat(cat), None)
        lag = LAG[cls] + (eff["delay"] if eff["delay"] else 0)
        # print outcome conditioned on governing mood at print
        if ci is not None:
            gm = mood_at(res, ci)
            pb = 0.62 if gm > 0.3 else (0.35 if gm < -0.3 else 0.50)
            u = rng.random()
            beat = u < pb; miss = u > 1 - (0.13 if gm > 0.3 else 0.35 if gm < -0.3 else 0.22)
            gap = (rng.uniform(2.2, 4.0) if beat else rng.uniform(-4.0, -2.2) if miss else rng.uniform(-0.8, 0.8)) * atr
        else:
            gap, beat, miss = 0.0, False, False
        world["gapz"][t] = gap
        S, closes, states = S0, [], []
        pos_gap_i = None
        for i in range(44):
            mood = mood_at(res, i)
            if eff["kill_at"] is not None and i >= eff["kill_at"]: mood = -1.0
            drift = {1.0: .15, 0.0: .02, -0.5: -.25, -1.0: -.45}.get(round(mood*2)/2 if mood in (1,0,-0.5,-1) else 0, mood * .3) * atr
            ramp = 0.0
            if (not no_ramp) and ci is not None and 0 < (ci - i) <= max(3, lag * 5 // 7) and mood > -0.5:
                ramp = 0.35 * atr                                  # front-run accumulation
            noise = rng.gauss(0, atr)
            dr = drift + ramp + noise
            if ci is not None and i == ci: dr += gap                # the print gap
            if pos_gap_i is not None:                               # 45% digestion of a positive gap
                k = i - pos_gap_i
                if 1 <= k <= 6: dr -= gap * [0, .20, .15, .08, .04, .02, .01][k]
            if i in (FOMC_I, FOMC_I + 1) and (eff["dent"] or eff["kill_at"] == IDX[dt.date(2026,7,30)]):
                dr -= (0.5 if i == FOMC_I else 0.3) * atr           # hawkish dent
            S = max(0.2 * NAMES[t][0], S * (1 + dr))
            closes.append(S)
            if ci is not None and i == ci and gap > 1.5 * atr: pos_gap_i = i
            # scanner stub
            if ci is not None and 0 < (ci - i) <= lag and mood > -0.4:
                stt = "COILED" if rng.random() < (0.72 if mood > 0.3 else 0.38) else "BASING"
            elif pos_gap_i is not None and i - pos_gap_i <= 3: stt = "EXTENDED"
            elif mood < -0.4: stt = "NO SETUP"
            else: stt = "BASING" if rng.random() < 0.3 else "NO SETUP"
            states.append(stt)
        world["px"][t], world["state"][t] = closes, states
    return world

# ---------- the agent (the system's rules) ----------
def run_agent(world, tree_on, rng):
    nav, navs = 100.0, []
    pos = {}   # t -> dict(debit, qty_frac, K1, K2, exp_i, entry_i)
    trades = []
    eff, res = world["eff"], world["res"]
    for i in range(44):
        # tree-layer stance (resolved nodes only)
        if tree_on:
            sc, wsum = 0.0, 0.0
            for nid, dend, brs in TREE:
                wsum += W[nid]
                sc += W[nid] * (MOODV[res[nid][1]] if (nid in res and i > dend) else sum(p*MOODV[m] for p, m, _ in brs))
            stance = 50 + 50 * sc / wsum
            killed = eff["kill_at"] is not None and i > eff["kill_at"]
        else:
            stance, killed = 100, False
        # exits
        for t in list(pos):
            p = pos[t]; S = world["px"][t][i]
            rem = p["exp_i"] - i
            iv_now = NAMES[t][1] / 100 * (0.6 if i > IDX.get(dt.date.fromisoformat(NAMES[t][2]), 99) else 1.0)
            val = spread_val(S, p["K1"], p["K2"], rem * 365 / 252, iv_now)
            ci = IDX.get(dt.date.fromisoformat(NAMES[t][2]), None)
            exit_now = (ci is not None and i == ci + 1)                    # R5 sell-into-news
            exit_now |= world["state"][t][i] == "EXTENDED" and ci is not None and i > ci
            exit_now |= val <= 0.40 * p["debit"]                           # defined-risk stop
            exit_now |= rem <= 0
            exit_now |= tree_on and killed                                  # regime kill: flatten
            if exit_now:
                pl = (val - p["debit"]) / p["debit"] - 0.03   # round-trip commission+slippage
                nav += nav * p["risk"] * pl
                trades.append((t, pl)); del pos[t]
        # entries
        if not (tree_on and (killed or stance < 45)):
            for t, (S0, iv, cat, cls) in NAMES.items():
                if t in pos or len(pos) >= 6: continue
                ci = IDX.get(dt.date.fromisoformat(cat), None)
                if ci is None: continue                                     # NO-DATE / outside → never trade
                dtc = ci - i
                if not (1 <= dtc <= 10): continue
                if world["state"][t][i] != "COILED": continue               # the gate
                S = world["px"][t][i]
                K1, K2 = S * 1.05, S * 1.18
                dte = dtc + 21
                debit = spread_val(S, K1, K2, dte * 365 / 252, iv / 100)
                width = K2 - K1
                if debit <= 0 or debit > 0.5 * width: continue              # engine price gate
                bull_S = S * (1 + 2.5 * ATR[t] * math.sqrt(dtc))
                ret = (spread_val(bull_S, K1, K2, 21 * 365 / 252, iv / 100 * .6) - debit) / debit
                if ret < 0.5: continue                                      # grade gate (A/B only)
                risk = 0.03 if cls != "comp" else 0.02
                if tree_on and eff["dent"] and FOMC_I <= i <= FOMC_I + 4: risk *= 0.7
                if tree_on and eff["halve"]: risk *= 0.5
                pos[t] = {"debit": debit, "K1": K1, "K2": K2, "exp_i": ci + 21, "entry_i": i, "risk": risk}
        navs.append(nav)
    # mark residual positions at window end
    for t, p in pos.items():
        S = world["px"][t][43]
        val = spread_val(S, p["K1"], p["K2"], (p["exp_i"] - 43) * 365 / 252, NAMES[t][1] / 100 * .8)
        pl = (val - p["debit"]) / p["debit"] - 0.03
        nav += nav * p["risk"] * pl; trades.append((t, pl))
    navs[-1] = nav
    peak, dd = navs[0], 0.0
    for x in navs:
        peak = max(peak, x); dd = min(dd, x / peak - 1)
    return nav - 100, navs, trades, dd * 100

def find_strike(S, dte, iv, budget, side="C"):
    """closest strike whose model premium fits the budget (per share)."""
    step = 0.025
    for k in range(1, 40):
        K = S * (1 + step * k) if side == "C" else S * (1 - step * k)
        prem = bs_call(S, K, dte/365, iv) if side == "C" else bs_put(S, K, dte/365, iv)
        if prem <= budget and prem >= 0.05:
            return K, prem
    return None, None

def run_lotto(world, variant, risk, rng, budget=0.60):
    """L1 hold→print+1 · L2 +4x pre-print TP · L3 +40% stop · L4 tree-directional (puts post-kill)."""
    nav, navs, trades = 100.0, [], []
    pos = {}
    eff, res = world["eff"], world["res"]
    for i in range(44):
        killed = eff["kill_at"] is not None and i > eff["kill_at"]
        # stance (resolved-only, same math as app)
        sc, wsum = 0.0, 0.0
        for nid, dend, brs in TREE:
            wsum += W[nid]
            sc += W[nid] * (MOODV[res[nid][1]] if (nid in res and i > dend) else sum(p*MOODV[m] for p, m, _ in brs))
        stance = 50 + 50 * sc / wsum
        # exits
        for t in list(pos):
            p = pos[t]; S = world["px"][t][i]
            rem = max(p["exp_i"] - i, 0)
            ci = IDX.get(dt.date.fromisoformat(NAMES[t][2]), None)
            iv_now = NAMES[t][1] / 100 * (0.6 if (ci is not None and i > ci and p["side"] == "C") else 1.0)
            val = (bs_call if p["side"] == "C" else bs_put)(S, p["K"], rem*365/252/365, iv_now)
            cost = min(0.25, 0.04 / p["prem"]) + 0.02
            hit_tp  = variant in ("L2","L4") and ci is not None and i < ci and val >= 4 * p["prem"]
            hit_stp = variant == "L3" and val <= 0.4 * p["prem"]
            at_r5   = (ci is not None and i == ci + 1 and p["side"] == "C")
            put_out = p["side"] == "P" and (i - p["entry_i"] >= 8 or val >= 3 * p["prem"])
            if hit_tp or hit_stp or at_r5 or put_out or rem <= 0 or i == 43:
                pl = (val - p["prem"]) / p["prem"] - cost
                pl = max(pl, -1.0)
                nav += nav * p["risk"] * pl
                trades.append((t, pl, p["side"])); del pos[t]
        # entries — LOW trade: max 3 concurrent, tight window
        if len(pos) < 3:
            if not killed and stance >= 55:
                for t, (S0, iv, cat, cls) in NAMES.items():
                    if t in pos or len(pos) >= 3: continue
                    ci = IDX.get(dt.date.fromisoformat(cat), None)
                    if ci is None: continue
                    dtc = ci - i
                    if not (3 <= dtc <= 8): continue
                    if world["state"][t][i] != "COILED": continue
                    S = world["px"][t][i]
                    dte = dtc + 10
                    K, prem = find_strike(S, dte, iv/100, budget, "C")
                    if K is None: continue
                    pos[t] = {"side":"C","K":K,"prem":prem,"exp_i":ci+10,"entry_i":i,"risk":risk}
            elif variant == "L4" and killed:
                for t, (S0, iv, cat, cls) in NAMES.items():
                    if t in pos or len(pos) >= 3: continue
                    S = world["px"][t][i]
                    K, prem = find_strike(S, 15, iv/100, budget, "P")
                    if K is None or rng.random() > 0.5: continue
                    pos[t] = {"side":"P","K":K,"prem":prem,"exp_i":min(43,i+15),"entry_i":i,"risk":risk}
        navs.append(nav)
    peak, dd = navs[0], 0.0
    for x in navs:
        peak = max(peak, x); dd = min(dd, x/peak - 1)
    return nav - 100, navs, trades, dd*100

def buy_hold(world):
    r = sum(world["px"][t][43] / NAMES[t][0] - 1 for t in NAMES) / len(NAMES)
    return 100 * r

def classify(res, eff):
    if eff["kill_at"] is not None:
        return "KILL-" + ("N3" if res["N3"][1] == "kill" else "N5")
    if eff["froth"]: return "FROTH"
    if res["N3"][1] == "bearm": return "DETOUR-hawkish"
    if all(res[n][1] == "bull" for n in ("N1", "N3", "N5")): return "CLEAN-BULL"
    return "MIXED"

# ---------- runner ----------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--trials", type=int, default=3000)
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--no-ramp", action="store_true", help="A4-off: kill the anticipation drift")
    ap.add_argument("--lotto", action="store_true", help="run the cheap-premium single-leg battery (L1-L4) alongside")
    ap.add_argument("--risk", type=float, default=0.01, help="lotto NAV fraction per trade")
    ap.add_argument("--names", type=str, default="", help="comma list to restrict the tradeable universe")
    a = ap.parse_args()
    rng = random.Random(a.seed)
    if a.names:
        keep=set(x.strip() for x in a.names.split(","))
        for t in list(NAMES):
            if t not in keep: del NAMES[t]
    rows, eq_tree, eq_flat, eq_l2 = [], [0.0]*44, [0.0]*44, [0.0]*44
    for k in range(a.trials):
        w = gen_world(rng, a.no_ramp)
        arng = random.Random(a.seed * 100003 + k)
        pl_t, navs_t, tr_t, dd_t = run_agent(w, True, arng)
        arng2 = random.Random(a.seed * 100003 + k)  # same agent noise
        pl_f, navs_f, tr_f, dd_f = run_agent(w, False, arng2)
        bh = buy_hold(w)
        row={"cls": classify(w["res"], w["eff"]), "tree": pl_t, "flat": pl_f, "bh": bh,
                     "trades": tr_t, "ntr": len(tr_t), "dd_t": dd_t, "dd_f": dd_f}
        if a.lotto:
            for vr in ("L1","L2","L3","L4"):
                lrng = random.Random(a.seed*7919 + k*13 + hash(vr)%97)
                plv, navv, trv, ddv = run_lotto(w, vr, a.risk, lrng)
                row[vr]=plv; row[vr+"_tr"]=trv; row[vr+"_dd"]=ddv
                if vr=="L2":
                    for j in range(44): eq_l2[j]+=navv[j]
        rows.append(row)
        for i in range(44):
            eq_tree[i] += navs_t[i]; eq_flat[i] += navs_f[i]
    n = a.trials
    eq_tree = [x / n for x in eq_tree]; eq_flat = [x / n for x in eq_flat]
    def agg(key, sel=lambda r: True):
        v = [r[key] for r in rows if sel(r)]
        if not v: return None
        v.sort()
        return dict(n=len(v), mean=st.mean(v), med=st.median(v), p5=v[int(.05*len(v))], p95=v[int(.95*len(v))-1],
                    win=sum(1 for x in v if x > 0) / len(v))
    out = {"trials": n, "seed": a.seed, "ramp": not a.no_ramp, "eq_l2":[x/n for x in eq_l2] if a.lotto else None,
           "dd": {"tree": st.mean([r["dd_t"] for r in rows]), "flat": st.mean([r["dd_f"] for r in rows])},
           "overall": {"tree": agg("tree"), "flat": agg("flat"), "bh": agg("bh")},
           "by_class": {}, "per_name": {}, "eq_tree": eq_tree, "eq_flat": eq_flat}
    for cl in sorted({r["cls"] for r in rows}):
        out["by_class"][cl] = {"share": sum(1 for r in rows if r["cls"] == cl) / n,
                               "tree": agg("tree", lambda r: r["cls"] == cl),
                               "flat": agg("flat", lambda r: r["cls"] == cl),
                               "bh": agg("bh", lambda r: r["cls"] == cl)}
    pn = {}
    for r in rows:
        for t, pl in r["trades"]: pn.setdefault(t, []).append(pl)
    for t, v in pn.items():
        out["per_name"][t] = {"trades": len(v), "avg_pl": st.mean(v), "win": sum(1 for x in v if x > 0) / len(v)}
    if a.lotto:
        out["lotto"]={}
        for vr in ("L1","L2","L3","L4"):
            out["lotto"][vr]=agg(vr)
            alltr=[pl for r in rows for (_,pl,_) in r[vr+"_tr"]]
            wins=[x for x in alltr if x>0]
            out["lotto"][vr+"_trade"]={"n":len(alltr),"per_world":len(alltr)/n,
              "win":len(wins)/max(1,len(alltr)),"avg_win":st.mean(wins) if wins else 0,
              "avg_loss":st.mean([x for x in alltr if x<=0]) if len(wins)<len(alltr) else 0,
              "dd":st.mean([r[vr+"_dd"] for r in rows])}
        out["lotto"]["neg_worlds"]={vr: sum(1 for r in rows if r[vr]<0)/n for vr in ("L1","L2","L3","L4")}
    # invariants
    assert "MU" not in pn, "MU traded — no-date/out-of-window gate broken"
    avg_tr = st.mean([r["ntr"] for r in rows])
    out["avg_trades_per_world"] = avg_tr
    keys=["trials","ramp","overall","dd","by_class","per_name","avg_trades_per_world"]+(["lotto"] if a.lotto else [])
    print(json.dumps({k: out[k] for k in keys},
                     indent=1, default=lambda x: round(x, 2) if isinstance(x, float) else x))
    json.dump(out, open("/tmp/sim_out.json", "w"), default=float)

if __name__ == "__main__":
    main()
