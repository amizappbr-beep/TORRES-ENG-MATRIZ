"""Feirão do Imóvel — public + admin routes.

Public:
- GET  /api/feirao/config   → event info + empreendimentos (stock) [safe subset]
- POST /api/feirao/events   → funnel analytics events (page_view, quiz_started...)

Admin (JWT):
- GET  /api/admin/feirao/config    → full config
- PUT  /api/admin/feirao/config    → update stock / weights / faixas / event
- GET  /api/admin/feirao/overview  → A/B/C/D, hoje, inscritos, por empreendimento
- GET  /api/admin/feirao/funnel    → funnel counts from events + leads
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel, ConfigDict, Field

from auth import get_current_admin
from feirao_core import DEFAULT_CONFIG

public_router = APIRouter(prefix="/feirao", tags=["feirao"])
admin_feirao_router = APIRouter(prefix="/admin/feirao", tags=["feirao-admin"])


def get_db(request: Request):
    return request.app.state.db


async def load_config(db) -> Dict[str, Any]:
    cfg = await db.config.find_one({"_id": "feirao"})
    if not cfg:
        cfg = dict(DEFAULT_CONFIG)
        await db.config.insert_one(cfg)
    cfg.pop("_id", None)
    return cfg


async def seed_config(db) -> None:
    """Semeia/atualiza a config do Feirão.

    Idempotente: em cada startup sincroniza os campos de CONTEÚDO (evento e
    dados de apresentação/comercial dos empreendimentos) a partir do
    DEFAULT_CONFIG do código, PRESERVANDO os campos editáveis pela operação
    (estoque de cada empreendimento, weights e faixas). Isso garante que um
    novo deploy reflita os textos/preços atualizados mesmo que o documento já
    exista no banco (ex.: produção semeada em versão antiga com "A DEFINIR").
    """
    existing = await db.config.find_one({"_id": "feirao"})
    if not existing:
        await db.config.insert_one(dict(DEFAULT_CONFIG))
        return

    import copy

    new_cfg = copy.deepcopy(DEFAULT_CONFIG)

    # Preserva pesos/faixas se a operação já os tiver customizado.
    if isinstance(existing.get("weights"), dict) and existing["weights"]:
        new_cfg["weights"] = existing["weights"]
    if isinstance(existing.get("faixas"), dict) and existing["faixas"]:
        new_cfg["faixas"] = existing["faixas"]

    # Preserva o estoque atual de cada empreendimento (ajustado pela operação).
    existing_emps = existing.get("empreendimentos") or {}
    for slug, emp in new_cfg["empreendimentos"].items():
        ex_emp = existing_emps.get(slug) or {}
        if ex_emp.get("estoque") is not None:
            emp["estoque"] = ex_emp["estoque"]

    await db.config.replace_one({"_id": "feirao"}, new_cfg)


# ----------------------------- Public -----------------------------

@public_router.get("/config")
async def public_config(request: Request):
    cfg = await load_config(get_db(request))
    return {"event": cfg.get("event"), "empreendimentos": cfg.get("empreendimentos")}


class EventPayload(BaseModel):
    model_config = ConfigDict(extra="ignore")
    event: str  # page_view, quiz_started, quiz_step_completed, quiz_completed,
    #             lead_created, property_recommended, event_signup,
    #             whatsapp_clicked, appointment_created
    session_id: str
    lead_id: Optional[str] = None
    empreendimento: Optional[str] = None
    step: Optional[int] = None
    utm: Optional[Dict[str, Any]] = None
    origem: Optional[str] = None


@public_router.post("/events")
async def track_event(payload: EventPayload, request: Request):
    db = get_db(request)
    doc = payload.model_dump()
    doc["id"] = str(uuid.uuid4())
    doc["at"] = datetime.now(timezone.utc).isoformat()
    await db.events.insert_one(doc)
    return {"ok": True}


# ----------------------------- Admin -----------------------------

@admin_feirao_router.get("/config")
async def admin_get_config(request: Request, current=Depends(get_current_admin)):
    return await load_config(get_db(request))


class ConfigUpdate(BaseModel):
    model_config = ConfigDict(extra="ignore")
    event: Optional[Dict[str, Any]] = None
    empreendimentos: Optional[Dict[str, Any]] = None
    weights: Optional[Dict[str, int]] = None
    faixas: Optional[Dict[str, int]] = None


@admin_feirao_router.put("/config")
async def admin_update_config(
    payload: ConfigUpdate, request: Request, current=Depends(get_current_admin)
):
    db = get_db(request)
    await load_config(db)  # ensure exists
    update: Dict[str, Any] = {}
    for field in ("event", "empreendimentos", "weights", "faixas"):
        val = getattr(payload, field)
        if val is not None:
            update[field] = val
    if update:
        await db.config.update_one({"_id": "feirao"}, {"$set": update})
    return await load_config(db)


@admin_feirao_router.get("/overview")
async def admin_overview(request: Request, current=Depends(get_current_admin)):
    db = get_db(request)
    cfg = await load_config(db)

    total = await db.leads.count_documents({})
    now = datetime.now(timezone.utc)
    start_today = now.replace(hour=0, minute=0, second=0, microsecond=0).isoformat()
    hoje = await db.leads.count_documents({"created_at": {"$gte": start_today}})

    classes = {"A": 0, "B": 0, "C": 0, "D": 0}
    async for row in db.leads.aggregate(
        [{"$group": {"_id": "$classe", "count": {"$sum": 1}}}]
    ):
        if row["_id"] in classes:
            classes[row["_id"]] = row["count"]

    inscritos = await db.leads.count_documents({"confirmou_feirao": {"$in": ["sim", "talvez"]}})
    confirmados = await db.leads.count_documents({"confirmou_feirao": "sim"})

    por_empreendimento: Dict[str, int] = {}
    async for row in db.leads.aggregate(
        [{"$group": {"_id": "$empreendimento_recomendado", "count": {"$sum": 1}}}]
    ):
        if row["_id"]:
            por_empreendimento[row["_id"]] = row["count"]

    # garante todas as chaves de empreendimento
    for slug in cfg.get("empreendimentos", {}):
        por_empreendimento.setdefault(slug, 0)

    return {
        "total": total,
        "hoje": hoje,
        "classes": classes,
        "inscritos_feirao": inscritos,
        "confirmados_feirao": confirmados,
        "por_empreendimento": por_empreendimento,
    }


@admin_feirao_router.get("/analytics")
async def admin_analytics(
    request: Request, days: int = 30, current=Depends(get_current_admin)
):
    """Métricas para o dashboard: KPIs, série temporal, funil, origem/UTM."""
    db = get_db(request)
    days = max(1, min(days, 365))
    now = datetime.now(timezone.utc)
    start = (now - timedelta(days=days - 1)).replace(
        hour=0, minute=0, second=0, microsecond=0
    )
    start_iso = start.isoformat()
    today_iso = now.replace(hour=0, minute=0, second=0, microsecond=0).isoformat()
    d7 = (now - timedelta(days=7)).isoformat()

    total = await db.leads.count_documents({})
    hoje = await db.leads.count_documents({"created_at": {"$gte": today_iso}})
    leads7 = await db.leads.count_documents({"created_at": {"$gte": d7}})
    leads_range = await db.leads.count_documents({"created_at": {"$gte": start_iso}})

    classes = {"A": 0, "B": 0, "C": 0, "D": 0}
    async for row in db.leads.aggregate([{"$group": {"_id": "$classe", "count": {"$sum": 1}}}]):
        if row["_id"] in classes:
            classes[row["_id"]] = row["count"]

    # Série temporal (leads/dia + visitantes/dia)
    ts_leads: Dict[str, int] = {}
    async for row in db.leads.aggregate([
        {"$match": {"created_at": {"$gte": start_iso}}},
        {"$group": {"_id": {"$substrCP": ["$created_at", 0, 10]}, "count": {"$sum": 1}}},
    ]):
        ts_leads[row["_id"]] = row["count"]

    ts_vis: Dict[str, int] = {}
    async for row in db.events.aggregate([
        {"$match": {"event": "page_view", "at": {"$gte": start_iso}}},
        {"$group": {"_id": {"$substrCP": ["$at", 0, 10]}, "s": {"$addToSet": "$session_id"}}},
    ]):
        ts_vis[row["_id"]] = len(row["s"])

    series = []
    for i in range(days):
        d = (start + timedelta(days=i)).strftime("%Y-%m-%d")
        series.append({"date": d, "leads": ts_leads.get(d, 0), "visitantes": ts_vis.get(d, 0)})

    # Funil no período (sessões únicas)
    def _q(ev):
        return {"event": ev, "at": {"$gte": start_iso}}

    visitantes = len(await db.events.distinct("session_id", _q("page_view")))
    iniciaram = len(await db.events.distinct("session_id", _q("quiz_started")))
    finalizaram = len(await db.events.distinct("session_id", _q("quiz_completed")))
    whats = len(await db.events.distinct("session_id", _q("whatsapp_clicked")))
    cadastraram = await db.leads.count_documents(
        {"created_at": {"$gte": start_iso}, "name": {"$ne": None}}
    )
    agendaram = await db.leads.count_documents(
        {"created_at": {"$gte": start_iso}, "confirmou_feirao": "sim"}
    )

    # Origem (source + campaign) no período
    origem = []
    async for row in db.leads.aggregate([
        {"$match": {"created_at": {"$gte": start_iso}}},
        {"$group": {
            "_id": {
                "source": {"$ifNull": ["$utm.source", "direto"]},
                "campaign": {"$ifNull": ["$utm.campaign", None]},
            },
            "count": {"$sum": 1},
        }},
        {"$sort": {"count": -1}},
    ]):
        origem.append({
            "source": row["_id"]["source"] or "direto",
            "campaign": row["_id"].get("campaign"),
            "leads": row["count"],
        })

    por_emp: Dict[str, int] = {}
    async for row in db.leads.aggregate([
        {"$match": {"created_at": {"$gte": start_iso}}},
        {"$group": {"_id": "$empreendimento_recomendado", "count": {"$sum": 1}}},
    ]):
        if row["_id"]:
            por_emp[row["_id"]] = row["count"]

    return {
        "days": days,
        "kpis": {
            "total": total,
            "hoje": hoje,
            "leads_7d": leads7,
            "leads_range": leads_range,
            "agendaram": agendaram,
            "whatsapp": whats,
        },
        "classes": classes,
        "series": series,
        "funnel": {
            "visitantes": visitantes,
            "iniciaram_quiz": iniciaram,
            "finalizaram_quiz": finalizaram,
            "cadastraram": cadastraram,
            "agendaram": agendaram,
            "clicaram_whatsapp": whats,
        },
        "origem": origem,
        "por_empreendimento": por_emp,
    }



@admin_feirao_router.get("/funnel")
async def admin_funnel(request: Request, current=Depends(get_current_admin)):
    db = get_db(request)

    def _uniq_sessions(event_name):
        return db.events.distinct("session_id", {"event": event_name})

    page_view = len(await db.events.distinct("session_id", {"event": "page_view"}))
    quiz_started = len(await db.events.distinct("session_id", {"event": "quiz_started"}))
    quiz_completed = len(await db.events.distinct("session_id", {"event": "quiz_completed"}))
    whatsapp = len(await db.events.distinct("session_id", {"event": "whatsapp_clicked"}))

    cadastraram = await db.leads.count_documents({"name": {"$ne": None}})
    agendaram = await db.leads.count_documents({"confirmou_feirao": "sim"})

    # por origem (UTM source)
    por_origem: Dict[str, int] = {}
    async for row in db.leads.aggregate(
        [{"$group": {"_id": "$utm.source", "count": {"$sum": 1}}}]
    ):
        key = row["_id"] or "direto"
        por_origem[key] = por_origem.get(key, 0) + row["count"]

    return {
        "funil": {
            "visitantes": page_view,
            "iniciaram_quiz": quiz_started,
            "finalizaram_quiz": quiz_completed,
            "cadastraram": cadastraram,
            "agendaram": agendaram,
            "clicaram_whatsapp": whatsapp,
        },
        "por_origem": por_origem,
    }
