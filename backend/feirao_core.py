"""Feirão do Imóvel — Torres Engenharia.

Core business logic for the pre-qualification funnel:
- Default configuration (event info, empreendimentos/stock, score weights, faixas)
- Lead scoring (0..100)
- A/B/C/D classification
- Empreendimento recommendation engine

All numbers (stock, weights, faixas) are stored in the `config` Mongo
collection and are editable from the admin panel. The DEFAULT_CONFIG below is
only used to seed the collection on first run.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

# --------------------------------------------------------------------------
# DEFAULT CONFIG (seeded once; editable via admin)
# --------------------------------------------------------------------------

DEFAULT_CONFIG: Dict[str, Any] = {
    "_id": "feirao",
    "event": {
        "nome": "II Feirão do Imóvel Torres Engenharia",
        "data": "2026-09-19",
        "data_label": "19 de setembro de 2026",
        "local_nome": "Residencial Reserva 025",
        "endereco": "Rua Terezina, 25 - Alterosas, Serra - ES",
        "whatsapp": "5527998336937",
    },
    # Empreendimentos — preços/condições ficam como "A DEFINIR" até o cliente
    # fornecer. Só o estoque é numérico (editável no admin).
    "empreendimentos": {
        "viva": {
            "slug": "viva",
            "nome": "Residencial Viva",
            "estoque": 8,
            "regiao": "Jacaraípe",
            "regioes_match": ["jacaraipe"],
            "tags": ["praia", "duplex", "quintal", "familia", "localizacao"],
            "destaque": False,
            "ultima_unidade": False,
            "preco_label": "A partir de R$ 330.000",
            "entrada_label": "3x de R$ 15.000",
            "obra_label": "Término da obra: Julho/2027",
            "status_label": None,
        },
        "alameda": {
            "slug": "alameda",
            "nome": "Alameda 500",
            "estoque": 5,
            "regiao": "Serra",
            "regioes_match": ["serra", "alterosas"],
            "tags": ["preco", "entrada_facil", "familia", "valorizacao"],
            "destaque": True,  # prioritário na campanha
            "ultima_unidade": False,
            "preco_label": "A partir de R$ 309.990",
            "entrada_label": "3x de R$ 15.000",
            "obra_label": "Término da obra: Maio/2028",
            "status_label": None,
        },
        "life": {
            "slug": "life",
            "nome": "Life 740",
            "estoque": 1,
            "regiao": "Serra",
            "regioes_match": ["serra", "alterosas"],
            "tags": ["ultima_unidade", "preco", "valorizacao"],
            "destaque": False,
            "ultima_unidade": True,
            "preco_label": "R$ 299.000",
            "entrada_label": "3x de R$ 15.000",
            "obra_label": "Término da obra: Dezembro/2026",
            "status_label": None,
        },
        "aldeia": {
            "slug": "aldeia",
            "nome": "Aldeia 350",
            "estoque": 1,
            "regiao": "Serra",
            "regioes_match": ["serra", "alterosas"],
            "tags": ["ultima_unidade", "familia", "valorizacao"],
            "destaque": False,
            "ultima_unidade": True,
            "preco_label": "R$ 299.000",
            "entrada_label": "Entrada de 20%",
            "obra_label": "Pronta para morar",
            "status_label": "PRONTA PARA MORAR",
        },
    },
    # Pesos máximos por dimensão (soma = 100)
    "weights": {
        "prazo": 20,
        "entrada": 25,
        "renda": 20,
        "financiamento": 15,
        "intencao": 10,
        "visita": 10,
    },
    # Faixas de classificação (score mínimo para cada classe)
    "faixas": {"A": 75, "B": 55, "C": 35},  # D = abaixo de C
}

# --------------------------------------------------------------------------
# SCORING TABLES (fração do peso de cada dimensão, 0..1)
# --------------------------------------------------------------------------

_PRAZO_PTS = {
    "imediato": 1.0,
    "30d": 0.85,
    "1_3m": 0.6,
    "3_6m": 0.3,
    "nao_sei": 0.1,
}
_ENTRADA_PTS = {
    "acima_150k": 1.0,
    "100_150k": 0.92,
    "50_100k": 0.8,
    "30_50k": 0.6,
    "10_30k": 0.4,
    "ate_10k": 0.2,
    "sem_entrada": 0.0,
}
_RENDA_PTS = {
    "acima_12k": 1.0,
    "8_12k": 0.9,
    "6_8k": 0.75,
    "4.5_6k": 0.6,
    "3_4.5k": 0.4,
    "ate_3k": 0.25,
}
_FIN_PTS = {
    "aprovado": 1.0,
    "nao_conclui": 0.55,
    "nao_aprovado": 0.35,
    "nunca": 0.3,
}
_INTENCAO_PTS = {
    "sair_aluguel": 1.0,
    "primeira_casa": 0.9,
    "casa_maior": 0.8,
    "investir": 0.7,
    "pesquisando": 0.2,
}
_VISITA_PTS = {
    "sim": 1.0,
    "talvez": 0.5,
    "nao": 0.0,
}


def compute_feirao_score(lead: Dict[str, Any], weights: Dict[str, int]) -> int:
    """Score 0..100 based on quiz answers. Missing answers score 0."""
    score = 0.0
    score += weights.get("prazo", 20) * _PRAZO_PTS.get(lead.get("prazo"), 0.0)
    score += weights.get("entrada", 25) * _ENTRADA_PTS.get(lead.get("entrada"), 0.0)
    score += weights.get("renda", 20) * _RENDA_PTS.get(lead.get("renda_familiar"), 0.0)
    score += weights.get("financiamento", 15) * _FIN_PTS.get(lead.get("financiamento"), 0.0)
    score += weights.get("intencao", 10) * _INTENCAO_PTS.get(lead.get("objetivo"), 0.0)
    score += weights.get("visita", 10) * _VISITA_PTS.get(lead.get("confirmou_feirao"), 0.0)
    return int(round(min(100.0, score)))


def classify_feirao(score: int, faixas: Dict[str, int]) -> str:
    if score >= faixas.get("A", 75):
        return "A"
    if score >= faixas.get("B", 55):
        return "B"
    if score >= faixas.get("C", 35):
        return "C"
    return "D"


def temperatura_from_classe(classe: str) -> str:
    """Map A/B/C/D to the legacy temperatura used by the Kanban/metrics."""
    return {"A": "quente", "B": "morno", "C": "morno", "D": "frio"}.get(classe, "frio")


# --------------------------------------------------------------------------
# RECOMMENDATION ENGINE
# --------------------------------------------------------------------------

def recomendar_empreendimentos(
    lead: Dict[str, Any], empreendimentos: Dict[str, Any]
) -> Tuple[Optional[str], List[str]]:
    """Return (best_slug, [alternative_slugs]) among empreendimentos with stock.

    Uses region (regiao), preferences (preferencias) and campaign priority.
    Only empreendimentos with estoque > 0 are considered.
    """
    regiao = (lead.get("regiao") or "").lower()
    prefs = set(lead.get("preferencias") or [])

    candidates = [e for e in empreendimentos.values() if int(e.get("estoque", 0)) > 0]
    if not candidates:
        return None, []

    scored: List[Tuple[float, Dict[str, Any]]] = []
    for e in candidates:
        s = 0.0
        # Priority (Alameda etc.)
        if e.get("destaque"):
            s += 2.0
        # Region match
        rmatch = [r.lower() for r in e.get("regioes_match", [])]
        if regiao in ("todas", "aberto", ""):
            s += 1.0  # neutral base — user open to all
        elif regiao in rmatch:
            s += 6.0
        # Preference/tag overlap
        tags = set(e.get("tags", []))
        s += 2.0 * len(prefs & tags)
        # "última unidade" preference matches Life/Aldeia strongly
        if "ultima_unidade" in prefs and e.get("ultima_unidade"):
            s += 3.0
        # slight preference for larger available stock as tie-breaker
        s += min(2.0, int(e.get("estoque", 0)) * 0.1)
        scored.append((s, e))

    scored.sort(key=lambda x: x[0], reverse=True)
    best = scored[0][1]["slug"]
    alternativas = [row[1]["slug"] for row in scored[1:3]]
    return best, alternativas
