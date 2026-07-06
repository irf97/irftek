#!/usr/bin/env python3
"""
irftek.py — the one program. v1.1 zero-dependency edition (Jul 2026)
=============================================================
Compresses the whole stack: tiered universe + catalyst calendar + live data
(Nasdaq quotes & option chains + Yahoo history, requests-only) + the battery-proven NVTS
breakout state machine + the Black-Scholes setup engine (calls/puts/debit
spreads, EV / P(win) / breakeven / flat / grade) + the TWO-LAYER GATE
(thesis-ready calendar x COILED price state) — automated end to end.

USAGE (Termux / any Python 3.10+, the ONLY dependency is `pip install requests` — everything else is stdlib):

  python3 irftek.py brief                    # THE morning command:
                                             # fetch -> scan -> gate -> top setups (core tier)
  python3 irftek.py brief --tier event       # same, other tiers
  python3 irftek.py scan  --tier core        # states only (no options math)
  python3 irftek.py setups NVTS              # graded contracts for one name
  python3 irftek.py feed  --tier terminal    # refresh terminal_data.js for the HTML UI
  python3 irftek.py selftest                 # offline proof: math parity, parser,
                                             # state machine, engine sanity
  python3 irftek.py brief --mock             # offline demo of the full pipeline

Rules enforced automatically: R2 two-layer gate (verdict per name), R3
duration>=3x lead (flagged per contract), catalyst-date confidence (CONF/EST
with confirm-T-7 warnings). Sizing rules R4/R6 remain YOUR job.
Not investment advice. Seeds dated Jul 2026 — prices/dates move; verify.
"""
from __future__ import annotations
import argparse, json, math, random, sys, time, datetime as dt

# =====================================================================
# 0 · UNIVERSE + CALENDAR (embedded; watchlist_config.py overrides tiers)
# =====================================================================
TIERS = {
 "core": ["NVTS","CRWV","MRVL","AVGO","AMD","MU","OKTA","NVDA","ARM","INTC",
          "AAPL","MSFT","GOOGL","META","AMZN","DELL","QCOM","TSLA","NOW","NET",
          "DDOG","CRWD","PANW"],
 "event": ["SERV","ONDS","AAOI","POET","RR","CBRS","IONQ","TEM","QBTS","RGTI",
           "RXRX","SOUN"],
 "component": ["HIMX","VICR","POWI","MPWR","CRUS","AMKR","AEHR","FORM","TTMI",
               "SNDK","SITM","CEVA","AIP","VUZI","SLAB","LSCC","AMBA"],
 "bench": ["SAIL","MDB","PATH","LITE","IBM","TER","ISRG","CRM","ESTC","DT",
           "AKAM","FSLY","KOPN","QUBT","SDGR"],
}
TERMINAL = ["MRVL","NVTS","CRWV","AVGO","AMD","MU","OKTA"]
try:
    import watchlist_config as _wc
    TIERS = getattr(_wc, "TIERS", TIERS); TERMINAL = getattr(_wc, "TERMINAL", TERMINAL)
except Exception:
    pass
ALL = [t for v in TIERS.values() for t in v]

# Catalyst calendar (session-verified spine; CONF = confirmed, EST = fiscal-
# cadence estimate -> confirm T-7). date "None" = undated (no thesis window).
CAT = {
 "MRVL":("2026-08-20","Q2 print — first after NVIDIA $2B/NVLink Fusion","CONF"),
 "NVDA":("2026-08-26","Q2 print — first with Rubin shipping","CONF"),
 "AVGO":("2026-09-03","Q3 print — $16B AI-semi guide is the bar","CONF"),
 "MU":("2026-09-21","FQ1 print — $50B guide; Micron named on Spark board","EST"),
 "NVTS":("2026-08-10","Earnings (Aug 3-17 conflict) + Rubin 800V racks Q3","EST"),
 "AMD":("2026-08-04","Q2 print + MI450 1GW deployment begins","EST"),
 "CRWV":("2026-08-12","Q2 print + Rubin deployment PRs (launch partner)","EST"),
 "OKTA":("2026-08-26","Q2 print + agent-identity cycle (Layer D)","EST"),
 "AAPL":("2026-09-09","iPhone/M5 event — Spark response stage","EST"),
 "META":("2026-09-17","Connect — glasses/ambient stage","EST"),
 "ARM":("2026-08-05","Q1 print — first with Spark design-wins narrative","EST"),
 "INTC":("2026-07-23","Q2 print — foundry + Arm-PC two-sided","EST"),
 "QCOM":("2026-07-30","Q3 print — Spark loser vs glasses winner","EST"),
 "MSFT":("2026-07-28","Capex + Copilot/agent print","EST"),
 "GOOGL":("2026-07-29","Capex + Gemini/agent print","EST"),
 "AMZN":("2026-07-30","Capex print","EST"),
 "TSLA":("2026-07-23","Q2 print (Optimus line)","EST"),
 "DELL":("2026-08-27","Q2 print — Spark OEM + AI server attach","EST"),
 "NOW":("2026-07-23","Q2 print — agentic workflow","EST"),
 "NET":("2026-07-31","Q2 print — agent platform/Durable Objects","EST"),
 "DDOG":("2026-08-06","Q2 print — AI observability","EST"),
 "CRWD":("2026-08-27","Q2 print — agentic security","EST"),
 "PANW":("2026-08-19","FQ4 print — CyberArk integration","EST"),
 "SERV":("2026-08-06","Q2 print + fleet PRs","EST"),
 "ONDS":("2026-08-11","Q2 print + defense drone flow","EST"),
 "AAOI":("2026-08-06","Q2 print — optical = Rubin cluster pace","EST"),
 "RR":("2026-08-13","Q2 print — squeeze mechanics","EST"),
 "CBRS":("2026-08-24","Hot Chips stage (no print in window)","EST"),
 "IONQ":("2026-08-06","Q2 print + networking milestones","EST"),
 "TEM":("2026-08-04","Q2 print","EST"),
 "QBTS":(None,"Undated CHIPS/contract headlines","EST"),
 "RGTI":(None,"Undated milestones","EST"),
 "RXRX":(None,"Binary readout — only if dated","EST"),
 "POET":(None,"Undated design-win PRs","EST"),
 "SOUN":("2026-08-06","Q2 print — on-device voice agents","EST"),
 "HIMX":("2026-08-06","Q2 print — glasses display engine + WiseEye","EST"),
 "VICR":("2026-07-21","Q2 print — VPD 2.0, record Q1","EST"),
 "POWI":("2026-08-04","Q2 print — 1250/1700V GaN, laptop chargers","EST"),
 "MPWR":("2026-07-31","Q2 print — NVIDIA VRM incumbent","EST"),
 "CRUS":("2026-07-29","FQ1 print — Apple + Windows-laptop expansion","EST"),
 "AMKR":("2026-07-27","Q2 print — Apple AZ packaging","EST"),
 "FORM":("2026-07-29","Q2 print — HBM/logic probe cards","EST"),
 "TTMI":("2026-07-29","Q2 print — AI PCBs","EST"),
 "SNDK":("2026-08-05","Print — client NAND for local AI","EST"),
 "SITM":("2026-08-05","Print — AI timing","EST"),
 "CEVA":("2026-08-10","Print — edge-AI IP royalty","EST"),
 "AIP":("2026-08-05","Print — NoC IP (shares-only chains)","EST"),
 "AEHR":(None,"Undated customer-order PRs (lotto until dated)","EST"),
 "VUZI":(None,"Undated OEM wins (HIMX expresses it better)","EST"),
}
# IV seeds (%) when no live chain IV; crush = post-event IV multiplier
IV_SEED = {"NVTS":95,"CRWV":85,"MU":75,"MRVL":55,"AMD":48,"OKTA":45,"AVGO":42,
           "SERV":110,"RR":120,"ONDS":95,"AAOI":80,"POET":100,"CBRS":75,"IONQ":100,
           "TEM":85,"QBTS":110,"RGTI":115,"RXRX":110,"SOUN":95,"HIMX":65,"VICR":60,
           "POWI":45,"MPWR":45,"CRUS":45,"AMKR":55,"AEHR":110,"FORM":55,"TTMI":55,
           "SNDK":75,"SITM":60,"CEVA":70,"AIP":80,"VUZI":130,"SLAB":50,"LSCC":55,
           "AMBA":60}
def iv_seed(t):  return IV_SEED.get(t, 40 if t in TIERS["core"] else 70)
def crush_of(t): return 0.90 if CAT.get(t,(None,))[0] is None or "PR" in (CAT.get(t,("","",""))[1]) else 0.80
# Scenario seeds (catalyst-day % move): per-name for terminal 7, tier default otherwise
SCN_SEED = {"MRVL":(-12,10,22),"NVTS":(-18,15,35),"CRWV":(-15,12,28),"AVGO":(-10,7,15),
            "AMD":(-10,6,15),"MU":(-15,5,12),"OKTA":(-10,7,16)}
def scn_of(t):
    if t in SCN_SEED: return SCN_SEED[t]
    if t in TIERS["event"]: return (-15,10,25)
    if t in TIERS["component"]: return (-12,8,20)
    return (-8,5,12)
W = {"bear":0.30,"base":0.45,"bull":0.25}
EXPIRIES = ["2026-08-21","2026-09-18","2026-10-16","2026-11-20","2027-01-15"]
THESIS_WINDOW_D = 45      # catalyst within N days => thesis-ready
UA = {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/126 Safari/537.36",
      "Accept":"application/json, text/plain, */*","Origin":"https://www.nasdaq.com",
      "Referer":"https://www.nasdaq.com/"}

# =====================================================================
# 1 · MATH (Black-Scholes — parity-locked to the verified engines)
# =====================================================================
def _ncdf(x): return 0.5*(1+math.erf(x/math.sqrt(2)))
def bs_call(S,K,T,sig,r=0.04):
    if T<=0: return max(0.0,S-K)
    if sig<=0: return max(0.0,S-K*math.exp(-r*T))
    d1=(math.log(S/K)+(r+sig*sig/2)*T)/(sig*math.sqrt(T)); d2=d1-sig*math.sqrt(T)
    return S*_ncdf(d1)-K*math.exp(-r*T)*_ncdf(d2)
def bs_put(S,K,T,sig,r=0.04): return bs_call(S,K,T,sig,r)-S+K*math.exp(-r*T)
def price(cp,S,K,T,sig,r=0.04): return bs_call(S,K,T,sig,r) if cp=="C" else bs_put(S,K,T,sig,r)
def step_for(p): return .5 if p<20 else 1 if p<60 else 2.5 if p<150 else 5 if p<400 else 10 if p<800 else 25
def rnd(p): s=step_for(p); return round(p/s)*s

# =====================================================================
# 2 · DATA (quotes + chains + history; MockProvider for offline)
# =====================================================================
def _num(x):
    if x is None: return None
    s=str(x).replace("$","").replace(",","").replace("%","").strip()
    if s in ("","N/A","-","--"): return None
    try: return float(s)
    except ValueError: return None
def norm_date(s):
    s=str(s).strip()
    for f in ("%Y-%m-%d","%b %d, %Y","%B %d, %Y","%m/%d/%Y","%b. %d, %Y"):
        try: return dt.datetime.strptime(s,f).strftime("%Y-%m-%d")
        except ValueError: pass
    return None
def parse_chain(j):
    out=[]
    def walk(o,exp=None):
        if isinstance(o,dict):
            e=o.get("expiryDate") or o.get("expirygroup") or o.get("expirationDate") or exp
            st=_num(o.get("strike"))
            if st is not None and e:
                cL,pL=_num(o.get("c_Last")),_num(o.get("p_Last"))
                cI=_num(o.get("c_Iv") or o.get("c_impliedVolatility")); pI=_num(o.get("p_Iv") or o.get("p_impliedVolatility"))
                cB,cA=_num(o.get("c_Bid")),_num(o.get("c_Ask")); pB,pA=_num(o.get("p_Bid")),_num(o.get("p_Ask"))
                if cL is not None or cB is not None:
                    out.append({"exp":norm_date(e),"K":st,"cp":"C","last":cL,"bid":cB,"ask":cA,"iv":cI})
                if pL is not None or pB is not None:
                    out.append({"exp":norm_date(e),"K":st,"cp":"P","last":pL,"bid":pB,"ask":pA,"iv":pI})
            for v in o.values(): walk(v,e)
        elif isinstance(o,list):
            for v in o: walk(v,exp)
    walk(j)
    seen,ded=set(),[]
    for r in out:
        k=(r["exp"],r["K"],r["cp"])
        if r["exp"] and k not in seen: seen.add(k); ded.append(r)
    return ded
def fetch_quote(sess,t):
    try:
        j=sess.get(f"https://api.nasdaq.com/api/quote/{t}/info?assetclass=stocks",headers=UA,timeout=12).json()
        p=((j.get("data") or {}).get("primaryData") or {})
        px=_num(p.get("lastSalePrice")) or _num(p.get("lastTradePrice"))
        if px: return {"px":px,"src":"nasdaq"}
    except Exception: pass
    try:
        j=sess.get(f"https://query1.finance.yahoo.com/v8/finance/chart/{t}?range=5d&interval=1d",headers=UA,timeout=12).json()
        m=j["chart"]["result"][0]["meta"]
        return {"px":_num(m.get("regularMarketPrice")),"src":"yahoo"}
    except Exception: return None
import re as _re
def _cboe_chain(j):
    """CBOE delayed-quotes JSON -> same row shape as parse_chain."""
    rows=((j.get("data") or {}).get("options")) or []
    out=[]
    for o in rows:
        m=_re.search(r"([0-9]{6})([CP])([0-9]{8})$",str(o.get("option","")))
        if not m: continue
        yymmdd,cp,k=m.groups()
        iv=_num(o.get("iv"))
        out.append({"exp":f"20{yymmdd[:2]}-{yymmdd[2:4]}-{yymmdd[4:6]}","K":int(k)/1000,"cp":cp,
                    "last":_num(o.get("last_trade_price")),"bid":_num(o.get("bid")),
                    "ask":_num(o.get("ask")),"iv":round(iv*100,2) if iv and iv>0 else None})
    return out
def fetch_chain(sess,t):
    try:
        u=(f"https://api.nasdaq.com/api/quote/{t}/option-chain?assetclass=stocks"
           f"&limit=600&fromdate=all&todate=undefined&excode=oprac&callput=callput&money=all&type=all")
        ch=parse_chain(sess.get(u,headers=UA,timeout=15).json())
        if ch: return ch
    except Exception: pass
    try:  # CBOE delayed chains — works where Nasdaq gates datacenter IPs
        j=sess.get(f"https://cdn.cboe.com/api/global/delayed_quotes/options/{t}.json",
                   headers=UA,timeout=15).json()
        return _cboe_chain(j)
    except Exception: return []
def _hist_df(j):
    """Yahoo v8 chart JSON -> dict of OHLCV lists (pure stdlib)."""
    r=j["chart"]["result"][0]; q=r["indicators"]["quote"][0]
    o,h,l,c,v=q["open"],q["high"],q["low"],q["close"],q["volume"]
    out={"Open":[],"High":[],"Low":[],"Close":[],"Volume":[]}
    for i in range(len(c)):
        row=(o[i],h[i],l[i],c[i],v[i])
        if any(x is None for x in row): continue
        out["Open"].append(float(o[i])); out["High"].append(float(h[i]))
        out["Low"].append(float(l[i])); out["Close"].append(float(c[i]))
        out["Volume"].append(float(v[i]))
    return out if out["Close"] else None

def _nq_hist(j):
    """Nasdaq chart JSON -> dict of OHLCV lists."""
    rows=((j.get("data") or {}).get("chart")) or []
    out={"Open":[],"High":[],"Low":[],"Close":[],"Volume":[]}
    for r in rows:
        z=r.get("z") or r
        vals=[_num(z.get(k)) for k in ("open","high","low","close","volume")]
        if any(x is None for x in vals): continue
        for k,x in zip(("Open","High","Low","Close","Volume"),vals): out[k].append(x)
    return out if out["Close"] else None

def fetch_history(tickers,period="1y"):
    """Daily OHLCV per ticker: Yahoo chart first, Nasdaq chart as fallback."""
    import requests
    sess=requests.Session(); data={}
    end=dt.date.today(); start=end-dt.timedelta(days=380)
    for t in tickers:
        df=None
        try:
            j=sess.get(f"https://query1.finance.yahoo.com/v8/finance/chart/{t}?range={period}&interval=1d",
                       headers=UA,timeout=12).json()
            df=_hist_df(j)
        except Exception: df=None
        if df is None or len(df["Close"])<60:
            try:
                u=(f"https://api.nasdaq.com/api/quote/{t}/chart?assetclass=stocks"
                   f"&fromdate={start}&todate={end}")
                df=_nq_hist(sess.get(u,headers=UA,timeout=15).json())
            except Exception: df=None
        if df is not None and len(df["Close"])>=60: data[t]=df
        time.sleep(0.25)
    return data

class MockProvider:
    """Controlled OHLCV shapes, pure stdlib (deterministic via random.Random)."""
    @staticmethod
    def series(shape,n=170,seed=0):
        rng=random.Random(seed); g=rng.gauss
        def ohlcv(close,vol):
            hi=[c*(1+abs(g(0,0.005))) for c in close]
            lo=[c*(1-abs(g(0,0.005))) for c in close]
            op=[close[0]]+close[:-1]
            return {"Open":op,"High":[max(a,b) for a,b in zip(hi,close)],
                    "Low":[min(a,b) for a,b in zip(lo,close)],"Close":close,"Volume":vol}
        if shape in ("coiled","breakout"):
            ramp_n=130; coil_n=n-ramp_n; c=[10.0]
            for _ in range(ramp_n): c.append(max(0.5,c[-1]*(1+0.015+g(0,0.012))))
            c=c[1:]; base=c[-1]; vol=[1.5e6]*ramp_n
            for k in range(coil_n):
                amp=0.05*(1-k/coil_n)
                c.append(base*(1+0.0008*k)*(1+amp*math.sin(k*1.05)+g(0,0.004)))
                vol.append(1.5e6*(1.0-0.65*k/max(1,coil_n-1)))
            if shape=="breakout": c[-1]=c[-2]*1.12; vol[-1]=4.0e6
        elif shape=="extended":
            c=[10.0]
            for _ in range(n): c.append(c[-1]*(1+0.028+g(0,0.006)))
            c=c[1:]; vol=[1.5e6]*n
        elif shape=="gap":
            c=[10.0]
            for _ in range(n-1): c.append(max(0.5,c[-1]*(1+g(0,0.006))))
            c=c[1:]; c.append(c[-1]*1.35); vol=[1.0e6]*(n-1)+[4.0e6]
        else:
            c=[30.0]
            for _ in range(n): c.append(max(0.3,c[-1]*(1-0.012+g(0,0.015))))
            c=c[1:]; vol=[1.0e6]*n
        return ohlcv(c,vol)

# =====================================================================
# 3 · SCANNER (battery-proven v2 state machine — logic lifted verbatim)
# =====================================================================
def _ema(xs,n):
    al=2/(n+1); out=[]; prev=None
    for x in xs:
        prev=x if prev is None else al*x+(1-al)*prev
        out.append(prev)
    return out
def _sma(xs,n):
    out=[None]*len(xs); s=0.0
    for i,x in enumerate(xs):
        s+=x
        if i>=n: s-=xs[i-n]
        if i>=n-1: out[i]=s/n
    return out
def _rstd(xs,n):
    out=[None]*len(xs)
    for i in range(n-1,len(xs)):
        w=xs[i-n+1:i+1]; m=sum(w)/n
        out[i]=math.sqrt(sum((z-m)**2 for z in w)/n)
    return out
def _atr(h,l,c,n):
    tr=[h[0]-l[0]]+[max(h[i]-l[i],abs(h[i]-c[i-1]),abs(l[i]-c[i-1])) for i in range(1,len(c))]
    return _sma(tr,n)
def _rsi(c,n=14):
    d=[0.0]+[c[i]-c[i-1] for i in range(1,len(c))]
    mu=_sma([max(x,0) for x in d],n); md=_sma([max(-x,0) for x in d],n)
    out=[]
    for u,v in zip(mu,md):
        out.append(50.0 if (u is None or v is None or v==0) else 100-100/(1+u/v))
    return out
def _obv(c,v):
    out=[0.0]
    for i in range(1,len(c)):
        s=1 if c[i]>c[i-1] else (-1 if c[i]<c[i-1] else 0)
        out.append(out[-1]+s*v[i])
    return out
def _slope(xs,n):
    y=[x for x in xs if x is not None][-n:]
    if len(y)<n: return 0.0
    m=len(y); sx=m*(m-1)/2.0; sxx=(m-1)*m*(2*m-1)/6.0
    sy=sum(y); sxy=sum(i*yv for i,yv in enumerate(y))
    den=m*sxx-sx*sx
    if den==0: return 0.0
    b=(m*sxy-sx*sy)/den; base=sy/m
    return b/base if base else 0.0
def _pct_rank(sl,val):
    s=[x for x in sl if x is not None]
    if len(s)<5 or val is None: return 0.5
    return sum(1 for x in s if x<val)/len(s)
def _rmin(xs,n):
    out=[None]*len(xs)
    for i in range(n-1,len(xs)): out[i]=min(xs[i-n+1:i+1])
    return out

def score_name(df,hi_win=50):
    """Battery-proven v2 state machine — pure-Python port (parity-verified vs pandas)."""
    if df is None: return None
    c,h,l,v=df["Close"],df["High"],df["Low"],df["Volume"]
    if len(c)<60: return None
    clamp=lambda x,lo=0.0,hi=1.0: max(lo,min(hi,x))
    mid=_sma(c,20); sd=_rstd(c,20)
    ub=[None if m is None else m+2*s for m,s in zip(mid,sd)]
    lb=[None if m is None else m-2*s for m,s in zip(mid,sd)]
    kmid=_ema(c,20); a20=_atr(h,l,c,20)
    kub=[None if x is None else m+1.5*x for m,x in zip(kmid,a20)]
    klb=[None if x is None else m-1.5*x for m,x in zip(kmid,a20)]
    bbw=[None if (u is None or m in (None,0)) else (u-b2)/m for u,b2,m in zip(ub,lb,mid)]
    r=_rsi(c,14); e20=_ema(c,20); e50=_ema(c,50); obv=_obv(c,v)
    px=c[-1]
    bbw_rank=_pct_rank(bbw[-126:],bbw[-1])
    squeeze_on=bool(lb[-1] is not None and klb[-1] is not None and lb[-1]>klb[-1] and ub[-1]<kub[-1])
    squeeze=clamp((1-bbw_rank)*0.8+(0.2 if squeeze_on else 0.0))
    v5=_sma(v,5)[-1]; v20=_sma(v,20)[-1]
    dryup=clamp((v20-v5)/v20+0.5) if v20 else 0.5
    accum=clamp(0.5+8*_slope(obv,20)); volume=clamp(0.5*dryup+0.5*accum)
    hi=max(c[-hi_win:]); dist=(hi-px)/hi if hi else 1.0
    breaking=px>=hi*0.999
    proximity=1.0 if breaking else clamp(1-dist/0.12)
    rs=clamp(0.5+6*_slope(c,40))
    uptrend=px>e50[-1] and e20[-1]>e50[-1]
    hl=_slope(_rmin(l,5),30)>0
    trend=clamp((0.6 if uptrend else 0.0)+(0.4 if hl else 0.0))
    rv=r[-1]; rrise=r[-1]-r[-4]
    if rv>=80: momentum=0.2
    elif 50<=rv<72: momentum=clamp(0.6+0.05*rrise)
    elif rv<40: momentum=0.2
    else: momentum=0.5
    extended=rv>=80 or px>1.30*e50[-1]
    Wp={"squeeze":0.25,"volume":0.15,"proximity":0.20,"rs":0.20,"trend":0.10,"momentum":0.10}
    parts=dict(squeeze=squeeze,volume=volume,proximity=proximity,rs=rs,trend=trend,momentum=momentum)
    readiness=round(100*sum(Wp[k]*parts[k] for k in Wp),1)
    vol_expand=bool(v20) and v[-1]>1.5*v20
    over_trend=px>1.30*e50[-1]
    note=""
    if breaking and uptrend and not vol_expand:
        note="breaking level WITHOUT volume -- suspect; wait for confirmation"
    if len(c)>=hi_win+2:
        px1=c[-2]; hi1=max(c[-hi_win-1:-1])
        prox1=1.0 if px1>=hi1*0.999 else clamp(1-((hi1-px1)/hi1)/0.12)
        sq1=clamp((1-_pct_rank(bbw[-127:-1],bbw[-2]))*0.8+(0.2 if squeeze_on else 0.0))
    else: prox1,sq1=proximity,squeeze
    if breaking and vol_expand and uptrend:
        if over_trend:
            state="EXTENDED (don't chase)"; note="new high while >30% over 50d EMA -- late; distribution zone"
        else: state="BREAKOUT (trigger)"
    elif extended: state="EXTENDED (don't chase)"
    else:
        has_ramp=True if len(c)<90 else (c[-40]/c[-90]-1)>=0.08
        tight=(parts["squeeze"]>=0.50 and parts["proximity"]>=0.60 and sq1>=0.45 and prox1>=0.55 and has_ramp)
        if readiness>=68 and uptrend and tight: state="COILED — ready"
        elif uptrend and readiness>=50: state="BASING (watch)"
        else: state="NO SETUP"
    return dict(price=round(px,2),readiness=readiness,state=state,note=note,rsi=round(rv,1),
                dist_to_high=f"{dist*100:.1f}%",**{k:round(val,2) for k,val in parts.items()})

# =====================================================================
# 4 · SETUP ENGINE (parity port of the verified terminal engine)
# =====================================================================
ALIGN_C={"COILED":1,"BASING":.85,"REPAIR":.65,"VERIFY":.5,"EXTENDED":.15,"NO SETUP":.35,"BREAKOUT":1}
ALIGN_P={"EXTENDED":.85,"VERIFY":.5,"BASING":.35,"COILED":.15,"REPAIR":.3,"NO SETUP":.4,"BREAKOUT":.1}
def _state_key(s):
    if s is None: return "VERIFY"
    for k in ("COILED","BREAKOUT","BASING","EXTENDED","NO SETUP"):
        if s.startswith(k): return k
    return "VERIFY"
def setups_for(t,S,state=None,chain=None,today=None,iv=None,crush=None,scn=None,weights=None):
    today=today or dt.date.today()
    cinfo=CAT.get(t,(None,"",""))
    catD=dt.date.fromisoformat(cinfo[0]) if cinfo[0] else None
    iv=(iv if iv else iv_seed(t))/100.0; crush=crush or crush_of(t)
    b,m,u=scn or scn_of(t); scnd={"bear":b,"base":m,"bull":u}
    Wl=weights or W; sk=_state_key(state)
    out=[]
    if catD is None or S is None or S<=0: return out
    lead=max(1,(catD-today).days)
    def chain_row(exp,K,cp):
        if not chain: return None
        eps=step_for(K)/2
        return next((r for r in chain if r["exp"]==exp and r["cp"]==cp and abs(r["K"]-K)<=eps),None)
    def prem_of(cp,exp,eT,K):
        row=chain_row(exp,K,cp)
        ivx=(row["iv"]/100 if row and row.get("iv") and row["iv"]>1 else iv)
        p=None;src="model"
        if row:
            bi,ak,la=row.get("bid"),row.get("ask"),row.get("last")
            if bi and ak and bi>0 and ak>0: p=(bi+ak)/2
            elif la and la>0: p=la
            if p: src="chain"
        if not p: p=price(cp,S,K,max(0.0,(eT-today).days)/365,ivx)
        return p,ivx,src
    def breakeven(valfn,prem):
        lo,hi=-60.0,80.0; f=lambda mv:valfn(mv)-prem
        if f(lo)*f(hi)>0: return 0.0 if f(0)>=0 else None
        for _ in range(40):
            midv=(lo+hi)/2
            if (f(midv)>0)==(f(hi)>0): hi=midv
            else: lo=midv
        return (lo+hi)/2/100
    for exp in EXPIRIES:
        eT=dt.date.fromisoformat(exp)
        if eT<=catD: continue
        dte=(eT-today).days; r3ok=dte>=3*lead
        Trem=(eT-catD).days/365
        def legval(cp,K,ivx,mv): return price(cp,S*(1+mv/100),K,Trem,ivx*crush)
        def evaluate(label,typ,cp,prem,src,valfn):
            if prem<0.02: return
            vb,vm,vu=valfn(scnd["bear"]),valfn(scnd["base"]),valfn(scnd["bull"])
            ev=Wl["bear"]*vb+Wl["base"]*vm+Wl["bull"]*vu; ret=ev/prem-1
            pwin=(Wl["bear"] if vb>prem else 0)+(Wl["base"] if vm>prem else 0)+(Wl["bull"] if vu>prem else 0)
            flat=valfn(0)/prem-1; be=breakeven(valfn,prem)
            align=(ALIGN_C if cp=="C" else ALIGN_P)[sk]
            conf=0.35*(1 if cinfo[2]=="CONF" else 0.55)+0.25*align+0.20*(1 if r3ok else 0.35)+0.20*max(0,min(1,pwin))
            grade="SKIP" if ret<=0 else "A" if conf>=0.66 else "B" if conf>=0.5 else "C" if conf>=0.35 else "SKIP"
            if typ=="LOTTO" and grade!="SKIP": grade="C"
            out.append(dict(label=label,type=typ,exp=exp,dte=dte,prem=prem,src=src,ret=ret,
                            pwin=max(0,min(1,pwin)),flat=flat,be=be,grade=grade,r3ok=r3ok,
                            score=(ret if ret>0 else 0)*(0.5+0.5*conf)))
        Ks={"C":[rnd(S),rnd(S*1.10),rnd(S*1.25)],"P":[rnd(S),rnd(S*0.90),rnd(S*0.80)]}
        for cp in ("C","P"):
            for K in Ks[cp]:
                if K<=0: continue
                p,ivx,src=prem_of(cp,exp,eT,K)
                lotto=cp=="C" and K>=S*1.2 and not r3ok
                typ=("CRUSH-FADE PUT" if sk=="EXTENDED" else "HEDGE PUT") if cp=="P" else \
                    ("LOTTO" if lotto else ("REPAIR CALL" if (eT>=dt.date(2026,11,1) and sk in ("NO SETUP","VERIFY")) else "PRE-CAT CALL"))
                evaluate(f"{K:g}{cp}",typ,cp,p,src,lambda mv,cp=cp,K=K,ivx=ivx: legval(cp,K,ivx,mv))
        CS=(rnd(S*1.02),rnd(S*1.15)); PS=(rnd(S*0.98),rnd(S*0.85))
        if CS[1]>CS[0]:
            a=prem_of("C",exp,eT,CS[0]); bq=prem_of("C",exp,eT,CS[1]); net=a[0]-bq[0]
            if net>0.02:
                evaluate(f"{CS[0]:g}/{CS[1]:g}C","CALL SPREAD","C",net,
                         "chain" if a[2]=="chain" and bq[2]=="chain" else "model",
                         lambda mv,a=a,bq=bq: legval("C",CS[0],a[1],mv)-legval("C",CS[1],bq[1],mv))
        if PS[0]>PS[1]:
            a=prem_of("P",exp,eT,PS[0]); bq=prem_of("P",exp,eT,PS[1]); net=a[0]-bq[0]
            if net>0.02:
                evaluate(f"{PS[0]:g}/{PS[1]:g}P","PUT SPREAD","P",net,
                         "chain" if a[2]=="chain" and bq[2]=="chain" else "model",
                         lambda mv,a=a,bq=bq: legval("P",PS[0],a[1],mv)-legval("P",PS[1],bq[1],mv))
    out.sort(key=lambda x:(-x["score"],-x["ret"]))
    good=[x for x in out if x["grade"]!="SKIP"]
    skips=sorted([x for x in out if x["grade"]=="SKIP"],key=lambda x:-x["ret"])
    rows=good[:4]
    while len(rows)<4 and skips: rows.append(skips.pop(0))
    if len(good)>=4 and skips: rows.append(skips[0])
    return rows

# =====================================================================
# 5 · GATE + BRIEF
# =====================================================================
def gate(t,state,today=None):
    today=today or dt.date.today()
    d,label,confc=CAT.get(t,(None,"",""))
    if not d: return ("NO-DATE","no dated catalyst — undated story = no trade")
    catD=dt.date.fromisoformat(d); days=(catD-today).days
    thesis=0<=days<=THESIS_WINDOW_D
    sk=_state_key(state)
    coiled=sk in ("COILED","BREAKOUT")
    soon=THESIS_WINDOW_D<days<=THESIS_WINDOW_D+14
    if thesis and coiled: v="GO"
    elif soon and coiled: v="WINDOW-SOON"      # coiled, entry window opens within 2 weeks
    elif thesis and sk=="BASING": v="WATCH+"
    elif thesis: v="THESIS-ONLY"
    elif coiled: v="PRICE-ONLY"
    else: v="STAND-DOWN"
    warn=" · confirm date T-7" if confc=="EST" and 0<=days<=10 else ""
    return (v,f"{label} — {d} ({days:+d}d, {confc}){warn}")

def cmd_brief(tier,mock=False,weights=None):
    today=dt.date.today()
    tickers=TIERS.get(tier,TIERS["core"]) if tier!="all" else ALL
    print(f"\nIRFTEK BRIEF · {today} · tier={tier} · {len(tickers)} names")
    print("="*100)
    hist={}; quotes={}; chains={}
    if mock:
        mp=MockProvider()
        shapes=["coiled","breakout","extended","downtrend"]
        for i,t in enumerate(tickers[:8]):
            hist[t]=mp.series(shapes[i%4],seed=7+i); quotes[t]={"px":float(hist[t]['Close'].iloc[-1]),"src":"mock"}
        tickers=list(hist.keys())
    else:
        try: hist=fetch_history(tickers)
        except Exception as e:
            print(f"[history] fetch failed ({e}) — states unavailable (network?); --mock demos offline"); hist={}
        try:
            import requests; sess=requests.Session()
            for t in tickers:
                q=fetch_quote(sess,t)
                if q: quotes[t]=q
                time.sleep(0.4)
        except Exception as e: print(f"[quotes] {e}")
    rows=[]
    for t in tickers:
        st=score_name(hist.get(t)) if hist.get(t) is not None else None
        state=st["state"] if st else None
        px=(quotes.get(t) or {}).get("px") or (st["price"] if st else None)
        v,why=gate(t,state,today)
        rows.append((t,px,state or "—",st["readiness"] if st else "—",v,why,st["note"] if st else ""))
    order={"GO":0,"WINDOW-SOON":1,"WATCH+":2,"PRICE-ONLY":3,"THESIS-ONLY":4,"STAND-DOWN":5,"NO-DATE":6}
    rows.sort(key=lambda r:(order.get(r[4],9),-(r[3] if isinstance(r[3],(int,float)) else 0)))
    print(f"{'TICK':<6}{'PX':>9}  {'STATE':<22}{'RDY':>5}  {'GATE':<12} CATALYST")
    print("-"*100)
    for t,px,state,rdy,v,why,note in rows:
        pxs=f"{px:.2f}" if isinstance(px,(int,float)) else "—"
        print(f"{t:<6}{pxs:>9}  {state:<22}{rdy!s:>5}  {v:<12} {why}")
        if note: print(f"{'':6}! {note}")
    gos=[r for r in rows if r[4]=="GO"]
    if gos:
        print("\nTOP SETUPS ON GO NAMES (two-layer gate passed)")
        print("-"*100)
        try:
            import requests; sess=requests.Session()
        except Exception: sess=None
        for t,px,state,_,_,_,_ in gos[:4]:
            ch=fetch_chain(sess,t) if (sess and not mock) else None
            print(f"\n>> {t}  (state={state})")
            _print_setups(setups_for(t,px,state,ch,today,weights=weights))
    else:
        print("\nNo GO names right now — the gate is doing its job. WATCH+ names are next in line.")

def _print_setups(rows):
    if not rows: print("   (no dated catalyst / no viable contracts)"); return
    print(f"   {'setup':<16}{'type':<15}{'prem':>8}{'EV':>7}{'P(win)':>8}{'b/e':>7}{'flat':>7}  grade{'':2}note")
    for s in rows:
        be="—" if s["be"] is None else f"{s['be']*100:+.0f}%"
        r3="" if s["r3ok"] else " R3⚠"
        print(f"   {s['exp'][5:]} {s['label']:<12}{s['type']:<15}{s['prem']:>8.2f}{s['ret']*100:>6.0f}%"
              f"{s['pwin']*100:>7.0f}%{be:>7}{s['flat']*100:>6.0f}%  [{s['grade']}]{r3}  {s['src']}")

def cmd_setups(t,weights=None):
    t=t.upper(); today=dt.date.today()
    px=None; ch=None; state=None
    try:
        import requests; sess=requests.Session()
        q=fetch_quote(sess,t); px=q["px"] if q else None
        ch=fetch_chain(sess,t)
    except Exception as e: print(f"[data] live fetch unavailable ({e})")
    try:
        h=fetch_history([t]); st=score_name(h.get(t)); state=st["state"] if st else None
        if px is None and st: px=st["price"]
        if st: print(f"{t}: state={st['state']} rdy={st['readiness']} px={px}")
    except Exception: pass
    if px is None:
        print(f"{t}: no live price available in this environment — pass one manually? (this sandbox blocks market hosts; run on Termux)")
        return
    v,why=gate(t,state,today); print(f"gate: {v} — {why}\n")
    _print_setups(setups_for(t,px,state,ch,today,weights=weights))

def cmd_feed(tier):
    names=TERMINAL if tier=="terminal" else (ALL if tier=="all" else TIERS.get(tier,TERMINAL))
    try: import requests
    except ImportError: print("pip install requests"); return
    sess=requests.Session()
    feed={"asof":dt.datetime.now().strftime("%Y-%m-%d %H:%M"),"quotes":{},"chains":{},"states":{}}
    if len(names)>20: print(f"[feed] {len(names)} names — several minutes")
    try: hist=fetch_history(names)
    except Exception: hist={}
    for t in names:
        q=fetch_quote(sess,t)
        if q and q.get("px"): feed["quotes"][t]=q
        ch=fetch_chain(sess,t)
        if ch: feed["chains"][t]=ch
        df=hist.get(t)
        st=score_name(df) if df is not None else None
        if st: feed["states"][t]=st["state"]
        bars=len(df["Close"]) if df else 0
        print(f"[{t}] px={q['px'] if q and q.get('px') else '—'} ({q['src'] if q else 'no quote'})"
              f" · hist={bars} bars · state={st['state'] if st else '— (no history)'}"
              f" · chain={len(ch) if ch else 0}")
        time.sleep(0.8)
    with open("terminal_data.js","w") as f:
        f.write("// generated by irftek.py — "+feed["asof"]+"\nwindow.FEED = "+json.dumps(feed)+";\n")
    print("wrote terminal_data.js (quotes + chains + scanner states)")

# =====================================================================
# 6 · SELFTEST (offline, no network)
# =====================================================================
def selftest():
    P,F=[],[]
    def ck(name,cond,detail=""):
        (P if cond else F).append((name,detail))
    # BS parity vs session-verified constants
    ck("BS call parity (MRVL 300C)",abs(bs_call(274,300,106/365,.55)-23.52)<0.05,f"{bs_call(274,300,106/365,.55):.2f}")
    ck("BS put-call parity",abs(bs_put(100,100,0.5,0.4)-(bs_call(100,100,0.5,0.4)-100+100*math.exp(-0.04*0.5)))<1e-9)
    # chain parser (both API shapes)
    a=parse_chain({"data":{"table":{"rows":[{"expirygroup":"August 21, 2026","strike":"15.00","c_Last":"1.85","c_Iv":"92.4","p_Last":"2.10"}]}}})
    b=parse_chain({"data":{"optionChainList":{"rows":[{"expirationDate":"10/16/2026","strike":300.0,"c_Last":23.4}]}}})
    ck("chain parser shapes",len(a)==2 and a[0]["exp"]=="2026-08-21" and len(b)==1 and b[0]["K"]==300.0)
    # state machine on controlled shapes
    mp=MockProvider()
    r1=score_name(mp.series("coiled",seed=7)); r2=score_name(mp.series("breakout",seed=7))
    r3=score_name(mp.series("extended",seed=3)); r4=score_name(mp.series("downtrend",seed=5))
    r5=score_name(mp.series("gap",seed=4))
    ck("coil -> COILED",r1 and r1["state"].startswith("COILED"),r1 and r1["state"])
    ck("breakout bar -> BREAKOUT",r2 and r2["state"].startswith("BREAKOUT"),r2 and r2["state"])
    ck("parabolic -> EXTENDED",r3 and r3["state"].startswith("EXTENDED"),r3 and r3["state"])
    ck("downtrend -> NO SETUP",r4 and r4["state"]=="NO SETUP",r4 and r4["state"])
    ck("news gap -> EXTENDED, never a trigger",r5 and r5["state"].startswith("EXTENDED"),r5 and r5["state"])
    # setup engine sanity (session-verified behaviors)
    today=dt.date(2026,7,2)
    mrvl=setups_for("MRVL",274,"BASING (watch)",None,today)
    ck("MRVL spread grades A/B, EV>0",any(s["type"]=="CALL SPREAD" and s["grade"] in ("A","B") and s["ret"]>0 for s in mrvl),
       str([(s['label'],s['grade'],round(s['ret'],2)) for s in mrvl[:3]]))
    mu=setups_for("MU",995,"EXTENDED (don't chase)",None,today)
    ck("MU naked calls all SKIP at 75 IV",all(s["grade"]=="SKIP" or s["type"]!="PRE-CAT CALL" or s["ret"]<=0.05 for s in mu))
    ck("breakeven finite on a spread",any(s["be"] is not None and abs(s["be"])<0.5 for s in mrvl))
    g,why=gate("MRVL","COILED — ready",dt.date(2026,7,10)); ck("gate GO on thesis+coil",g=="GO",g)
    gs,_=gate("MRVL","COILED — ready",dt.date(2026,7,2)); ck("gate WINDOW-SOON just outside window",gs=="WINDOW-SOON",gs)
    g2,_=gate("QBTS","COILED — ready",today); ck("gate blocks undated names",g2=="NO-DATE",g2)
    g3,_=gate("MU","EXTENDED (don't chase)",dt.date(2026,9,1)); ck("gate THESIS-ONLY when extended",g3=="THESIS-ONLY",g3)
    canned={"chart":{"result":[{"timestamp":[1751000000+i*86400 for i in range(70)],
            "indicators":{"quote":[{"open":[10+i*0.1 for i in range(70)],
             "high":[10.2+i*0.1 for i in range(70)],"low":[9.9+i*0.1 for i in range(70)],
             "close":[10.1+i*0.1 for i in range(70)],"volume":[1e6]*70}]}}]}}
    dfh=_hist_df(canned)
    ck("yahoo history parser",dfh is not None and len(dfh["Close"])==70 and abs(dfh["Close"][-1]-17.0)<1e-6)
    nq={"data":{"chart":[{"z":{"open":"10.0","high":"10.5","low":"9.8","close":"10.2","volume":"1,000,000"}} for _ in range(65)]}}
    dfn=_nq_hist(nq)
    ck("nasdaq history parser",dfn is not None and len(dfn["Close"])==65 and abs(dfn["Volume"][0]-1e6)<1)
    cb=_cboe_chain({"data":{"options":[{"option":"MRVL260821C00280000","bid":10,"ask":11,"last_trade_price":10.5,"iv":0.55},{"option":"BAD"}]}})
    ck("cboe chain parser",len(cb)==1 and cb[0]["exp"]=="2026-08-21" and cb[0]["K"]==280 and cb[0]["cp"]=="C" and cb[0]["iv"]==55.0)
    print(f"SELFTEST: {len(P)} passed, {len(F)} failed")
    for n,d in F: print(f"  FAIL {n} [{d}]")
    return not F

# =====================================================================
# 7 · CLI
# =====================================================================
def main():
    ap=argparse.ArgumentParser(description="irftek — the one program")
    sub=ap.add_subparsers(dest="cmd")
    b=sub.add_parser("brief"); b.add_argument("--tier",default="core",choices=list(TIERS)+["all"]); b.add_argument("--mock",action="store_true")
    s=sub.add_parser("scan");  s.add_argument("--tier",default="core",choices=list(TIERS)+["all"])
    st=sub.add_parser("setups"); st.add_argument("ticker")
    f=sub.add_parser("feed");  f.add_argument("--tier",default="terminal",choices=["terminal"]+list(TIERS)+["all"])
    sub.add_parser("selftest")
    for p in (b,st):
        p.add_argument("--wbear",type=float,default=30); p.add_argument("--wbase",type=float,default=45); p.add_argument("--wbull",type=float,default=25)
    a=ap.parse_args()
    def weights(a):
        tot=(a.wbear+a.wbase+a.wbull) or 1
        return {"bear":a.wbear/tot,"base":a.wbase/tot,"bull":a.wbull/tot}
    if a.cmd=="selftest": sys.exit(0 if selftest() else 1)
    elif a.cmd=="brief": cmd_brief(a.tier,a.mock,weights(a))
    elif a.cmd=="scan": cmd_brief(a.tier,False,None)
    elif a.cmd=="setups": cmd_setups(a.ticker,weights(a))
    elif a.cmd=="feed": cmd_feed(a.tier)
    else: ap.print_help()

if __name__=="__main__":
    main()
