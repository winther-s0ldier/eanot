import os, json, pathlib
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import httpx
from dotenv import load_dotenv

load_dotenv()

DATA_PATH = pathlib.Path(__file__).resolve().parent.parent / "frontend" / "data.json"
FULL_CONTEXT = ""

def load_data():
    global FULL_CONTEXT
    if not DATA_PATH.exists():
        print(f"WARNING: data.json not found at {DATA_PATH}")
        return False
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        raw = json.load(f)
    FULL_CONTEXT = build_context(raw)
    count = raw.get("metadata", {}).get("recordCount", 0)
    print(f"Loaded data.json: {count:,} tickets, context={len(FULL_CONTEXT):,} chars")
    return True

def build_context(d):
    meta = d.get("metadata", {})
    summary = d.get("summary", {})
    kpis = summary.get("kpis", {})
    grades = d.get("grades", [])
    vendors = d.get("vendorScorecard", [])
    anomalies = d.get("anomalies", [])
    forecasts = d.get("forecasts", [])
    risk = d.get("predictiveRisk", {})
    clusters = d.get("clusters", {})
    top_assets = summary.get("topAssets", [])
    top_cats = summary.get("topCategories", [])
    top_stores = summary.get("topStores", [])
    monthly = summary.get("monthly", [])
    brands = summary.get("brands", [])
    pri_list = summary.get("priorities", [])
    teams = summary.get("teams", [])
    spend_region = summary.get("spendByRegion", [])

    L = []
    L.append("=== EAMOT MAINTENANCE DASHBOARD — COMPLETE DATA ===")
    dr = meta.get("dateRange", {})
    L.append(f"Period: {dr.get('start','?')} to {dr.get('end','?')}")
    L.append(f"Total tickets: {meta.get('recordCount',0):,}")
    L.append("")

    L.append("--- KEY PERFORMANCE INDICATORS ---")
    for k, v in kpis.items():
        if isinstance(v, float):
            L.append(f"  {k}: {v:.2f}")
        else:
            L.append(f"  {k}: {v}")
    L.append("")

    L.append("--- PRIORITY BREAKDOWN ---")
    for p in pri_list:
        L.append(f"  Priority {p.get('priority','?')}: {p.get('tickets',0):,} tickets, avgTAT={p.get('avgTatHours',0):.1f}h, spend={p.get('spend',0):,.0f}")
    L.append("")

    L.append("--- BRANDS ---")
    for b in brands:
        L.append(f"  {b.get('brand','?')}: {b.get('tickets',0):,} tickets, spend={b.get('spend',0):,.0f}, avgTAT={b.get('avgTatHours',0):.1f}h, onTime={b.get('onTimeRate',0)*100:.0f}%, repeat7d={b.get('repeat7dRate',0)*100:.0f}%")
    L.append("")

    L.append("--- TOP 20 CATEGORIES ---")
    for c in top_cats[:20]:
        L.append(f"  {c.get('category','?')}: {c.get('tickets',0):,} tickets, avgTAT={c.get('avgTatHours',0):.1f}h, spend={c.get('spend',0):,.0f}")
    L.append("")

    L.append("--- TOP 20 STORES ---")
    for s in top_stores[:20]:
        L.append(f"  {s.get('store','?')} ({s.get('brand','?')}, {s.get('region','?')}): {s.get('tickets',0):,} tickets, spend={s.get('spend',0):,.0f}, avgTAT={s.get('avgTatHours',0):.1f}h, repeat7d={s.get('repeat7dRate',0)*100:.0f}%")
    L.append("")

    L.append("--- TOP 15 ASSETS ---")
    for a in top_assets[:15]:
        L.append(f"  {a.get('asset','?')} ({a.get('assetFamily','?')}): {a.get('tickets',0):,} tickets, spend={a.get('spend',0):,.0f}, avgTAT={a.get('avgTatHours',0):.1f}h")
    L.append("")

    L.append("--- MONTHLY TREND ---")
    for m in monthly:
        L.append(f"  {m.get('month','?')}: {m.get('tickets',0):,} tickets")
    L.append("")

    L.append("--- SPEND BY REGION ---")
    for r in spend_region:
        L.append(f"  {r.get('region','?')}: spend={r.get('spend',0):,.0f}, tickets={r.get('tickets',0):,}, avgTAT={r.get('avgTatHours',0):.1f}h")
    L.append("")

    L.append(f"--- VENDOR SCORECARD (all {len(vendors)} vendors) ---")
    for v in vendors:
        L.append(f"  {v.get('assignee','?')} (team={v.get('team','?')}, brand={v.get('brand','?')}): tickets={v.get('tickets',0)}, avgTAT={v.get('avgTatHours',0):.1f}h, spend={v.get('spend',0):,.0f}, onTime={v.get('onTimeRate',0)*100:.0f}%, repeat7d={v.get('repeat7dRate',0)*100:.1f}%, score={v.get('score',0):.0f}, rank={v.get('rank','?')}")
    L.append("")

    L.append(f"--- MAINTENANCE TEAMS (all {len(teams)} teams) ---")
    for t in teams:
        L.append(f"  {t.get('team','?')} ({t.get('brand','?')}): tickets={t.get('tickets',0):,}, spend={t.get('spend',0):,.0f}, avgTAT={t.get('avgTatHours',0):.1f}h, onTime={t.get('onTimeRate',0)*100:.0f}%")
    L.append("")

    L.append(f"--- STORE GRADES (all {len(grades)} stores) ---")
    for g in grades:
        L.append(f"  {g.get('store','?')} ({g.get('brand','?')}, {g.get('region','?')}): grade={g.get('grade','?')}, tickets={g.get('tickets',0)}, avgTAT={g.get('avgTatHours',0):.1f}h, spend={g.get('spend',0):,.0f}, health={g.get('healthScore',0):.0f}, onTime={g.get('onTimeRate',0)*100:.0f}%, repeat7d={g.get('repeat7dRate',0)*100:.1f}%")
    L.append("")

    L.append(f"--- ANOMALIES (all {len(anomalies)}) ---")
    for a in anomalies:
        L.append(f"  {a.get('monthLabel','?')}: {a.get('brand','?')} {a.get('assetFamily','?')} ({a.get('region','?')}): {a.get('tickets',0)} tickets, spend={a.get('spend',0):,.0f}, severity={a.get('severity',0):.2f}, signal={a.get('signal','?')}")
    L.append("")

    if forecasts:
        L.append("--- FORECASTS (by region) ---")
        for fc in forecasts:
            region = fc.get("region", "?")
            pts = fc.get("points", [])
            forecast_pts = [p for p in pts if p.get("type") == "forecast"]
            if forecast_pts:
                trend = ", ".join(f"{p.get('weekLabel','?')}={p.get('tickets',0):.0f}" for p in forecast_pts[:4])
                L.append(f"  {region}: {trend}")
            else:
                L.append(f"  {region}: (no forecast points)")
        L.append("")

    if risk:
        tr = risk.get("topRisks", [])
        if tr:
            L.append(f"--- PREDICTIVE RISK (top {len(tr)}) ---")
            for r in tr[:25]:
                L.append(f"  {r.get('store','?')} ({r.get('brand','?')}): asset={r.get('asset','?')}, riskScore={r.get('riskScore',0):.0f}, riskProb={r.get('riskProbability',0)*100:.0f}%, past30={r.get('past30',0)}, past90={r.get('past90',0)}, band={r.get('priorityBand','?')}")
            L.append("")

    cl_list = clusters.get("clusters", [])
    if cl_list:
        L.append(f"--- STORE CLUSTERS ({len(cl_list)} clusters) ---")
        for cl in cl_list:
            L.append(f"  Cluster {cl.get('clusterId','?')} '{cl.get('clusterLabel','?')}': {cl.get('stores',0)} stores, {cl.get('tickets',0):,} tickets, avgTAT={cl.get('avgTatHours',0):.1f}h, avgAmount={cl.get('avgAmount',0):.0f}, spend={cl.get('spend',0):,.0f}, repeat7d={cl.get('repeat7dRate',0)*100:.0f}%, critical={cl.get('criticalShare',0)*100:.0f}%")
        L.append("")

    return "\n".join(L)

app = FastAPI(title="EAMOT Proxy")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

FRONTEND_DIR = pathlib.Path(__file__).resolve().parent.parent / "frontend"

GEMINI_KEY = os.environ.get("GOOGLE_GEMINI_KEY", "")
MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.1-pro-preview")

@app.on_event("startup")
async def startup():
    load_data()

class ChatRequest(BaseModel):
    messages: list = []
    context: dict = {}

@app.get("/api/health")
async def health():
    return {"status": "ok", "keyConfigured": bool(GEMINI_KEY), "dataLoaded": bool(FULL_CONTEXT)}

@app.get("/api/data")
async def get_data():
    if not FULL_CONTEXT:
        return JSONResponse({"error": "No data loaded"}, status_code=404)
    return {"context": FULL_CONTEXT}

@app.post("/api/chat")
async def chat(req: ChatRequest):
    if not GEMINI_KEY:
        return JSONResponse({"error": "Server not configured: missing GOOGLE_GEMINI_KEY"}, status_code=500)
    messages = req.messages
    ctx_from_frontend = req.context
    user_text = messages[-1]["text"] if messages else ""
    active_tab = ctx_from_frontend.get("activeTab", "overview")
    tab_charts = {
        "overview": "OVERVIEW TAB CHARTS: Monthly volume by brand (stacked bar), Priority breakdown (doughnut), Grade distribution (doughnut), Spend by brand (bar), TAT heatmap by priority, Category trend (line), Grade trend (line), Monthly tickets (line)",
        "anomalies": "ANOMALIES TAB: Top repeat offender stores, Regional heatmap, Z-score scatter, Top anomaly stores/categories, Repeat offenders within 24h",
        "ai": "AI & PREDICTIVE INSIGHTS: Regional performance radar, Asset trend, Grade trend, Predictive risk scores and clusters",
    }
    charts_desc = tab_charts.get(active_tab, "")
    sys_prompt = f"""You are EAMOT AI, an expert maintenance data analyst for Devyani International, a QSR operator in India (KFC, Pizza Hut, Taco Bell, Costa Coffee, etc.). Answer concisely in plain English for management users. Cite specific numbers from the data. You have access to ALL dashboard data below — never say "not available".

ACTIVE TAB: {active_tab}
{charts_desc}

COMPLETE DASHBOARD DATA:
{FULL_CONTEXT}"""
    contents = [
        {"role": "user", "parts": [{"text": sys_prompt}]},
        {"role": "model", "parts": [{"text": "Understood. I have complete access to all data and am ready to answer."}]},
    ]
    for m in messages[:-1]:
        role = "user" if m.get("role") == "user" else "model"
        contents.append({"role": role, "parts": [{"text": m["text"]}]})
    contents.append({"role": "user", "parts": [{"text": user_text}]})
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={GEMINI_KEY}"
    payload = {
        "contents": contents,
        "systemInstruction": {"parts": [{"text": "You are EAMOT AI. You have complete access to ALL 64,570 maintenance tickets, ALL 40 vendor scores, ALL 1,748 store grades, ALL 80 anomalies, forecasts, clusters, and risk scores. Answer any question using this data. Be concise, cite specific numbers, use plain English for management. Never make up data."}]},
        "generationConfig": {"temperature": 0.3, "maxOutputTokens": 4096},
    }
    try:
        async with httpx.AsyncClient(timeout=120) as client:
            resp = await client.post(url, json=payload)
        if not resp.is_success:
            reason = "Gemini API error"
            if resp.status_code == 403:
                reason = "Invalid API key"
            elif resp.status_code == 404:
                reason = f"Model {MODEL} not found"
            return JSONResponse({"error": reason}, status_code=min(resp.status_code, 500))
        data = resp.json()
        candidates = data.get("candidates", [])
        if not candidates:
            reason = data.get("promptFeedback", {}).get("blockReason", "unknown")
            return JSONResponse({"reply": "", "error": f"Request blocked: {reason}"}, status_code=200)
        reply = candidates[0].get("content", {}).get("parts", [{}])[0].get("text", "")
        return {"reply": reply or "No response."}
    except httpx.TimeoutException:
        return JSONResponse({"error": "Gemini API timed out (120s). Try a shorter question."}, status_code=504)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

if FRONTEND_DIR.exists():
    app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")
