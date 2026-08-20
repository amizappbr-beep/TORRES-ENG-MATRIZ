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
    existing = await db.config.find_one({"_id": "feirao"})
    if not existing:
        await db.config.insert_one(dict(DEFAULT_CONFIG))


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
