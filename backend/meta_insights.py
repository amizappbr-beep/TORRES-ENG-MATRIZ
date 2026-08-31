"""Meta Marketing API — Ads Insights (gasto por campanha) para CPL.

Lê credenciais das variáveis de ambiente do backend (nunca do frontend):
  META_APP_ID, META_APP_SECRET, META_SYSTEM_USER_TOKEN,
  META_AD_ACCOUNT_ID, META_GRAPH_API_VERSION

Se o token não estiver configurado, `is_configured()` retorna False e o
endpoint devolve {"configured": false} sem quebrar o dashboard.
"""
from __future__ import annotations

import hashlib
import hmac
import os
from datetime import date, datetime, timedelta, timezone
from typing import Any, Dict, List

import httpx


def _env(name: str) -> str:
    return (os.environ.get(name) or "").strip()


def is_configured() -> bool:
    return bool(
        _env("META_SYSTEM_USER_TOKEN")
        and _env("META_AD_ACCOUNT_ID")
        and _env("META_APP_SECRET")
    )


def _appsecret_proof(token: str, secret: str) -> str:
    return hmac.new(secret.encode(), token.encode(), hashlib.sha256).hexdigest()


async def fetch_campaign_insights(days: int = 30) -> List[Dict[str, Any]]:
    """Retorna [{campaign_id, campaign_name, spend(float), meta_leads(int),
    cpl_meta(float|None)}] no período (inclusivo)."""
    token = _env("META_SYSTEM_USER_TOKEN")
    account = _env("META_AD_ACCOUNT_ID")
    secret = _env("META_APP_SECRET")
    version = _env("META_GRAPH_API_VERSION") or "v21.0"
    if not (token and account and secret):
        return []

    end = date.today()
    start = end - timedelta(days=max(1, days) - 1)
    url = f"https://graph.facebook.com/{version}/act_{account}/insights"
    params = {
        "level": "campaign",
        "time_range": '{"since":"%s","until":"%s"}' % (start, end),
        "fields": "campaign_id,campaign_name,spend,actions",
        "limit": 500,
        "access_token": token,
        "appsecret_proof": _appsecret_proof(token, secret),
    }

    rows: List[Dict[str, Any]] = []
    async with httpx.AsyncClient(timeout=30) as client:
        next_url = url
        next_params = params
        while next_url:
            r = await client.get(next_url, params=next_params)
            if r.status_code >= 400:
                raise RuntimeError(f"Meta Insights error {r.status_code}: {r.text[:300]}")
            body = r.json()
            for x in body.get("data", []):
                spend = float(x.get("spend", 0) or 0)
                leads = 0
                for a in x.get("actions", []) or []:
                    if a.get("action_type") in ("lead", "offsite_conversion.fb_pixel_lead"):
                        leads += int(float(a.get("value", 0) or 0))
                rows.append({
                    "campaign_id": x.get("campaign_id"),
                    "campaign_name": x.get("campaign_name"),
                    "spend": round(spend, 2),
                    "meta_leads": leads,
                    "cpl_meta": round(spend / leads, 2) if leads else None,
                })
            next_url = body.get("paging", {}).get("next")
            next_params = None  # a URL de paginação já traz os parâmetros
    return rows


async def cpl_summary(db, days: int = 30) -> Dict[str, Any]:
    """Resumo de CPL cruzando gasto da Meta com os leads do nosso CRM."""
    if not is_configured():
        return {"configured": False}

    campaigns = await fetch_campaign_insights(days)
    total_spend = round(sum(c["spend"] for c in campaigns), 2)

    now = datetime.now(timezone.utc)
    start_iso = (now - timedelta(days=max(1, days) - 1)).replace(
        hour=0, minute=0, second=0, microsecond=0
    ).isoformat()
    crm_leads = await db.leads.count_documents({"created_at": {"$gte": start_iso}})

    return {
        "configured": True,
        "days": days,
        "moeda": "conta",  # moeda da conta de anúncios
        "total_spend": total_spend,
        "crm_leads": crm_leads,
        "cpl_crm": round(total_spend / crm_leads, 2) if crm_leads else None,
        "campanhas": sorted(campaigns, key=lambda c: c["spend"], reverse=True),
    }
