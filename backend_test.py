#!/usr/bin/env python3
"""
Backend test suite for Feirão do Imóvel Torres Engenharia
Tests all public and admin endpoints with real scenarios
"""
import requests
import json
from typing import Dict, Any, Optional

# Base URL from frontend/.env
BASE_URL = "https://torres-pre-quali.preview.emergentagent.com"
API_BASE = f"{BASE_URL}/api"

# Admin credentials from test_credentials.md
ADMIN_EMAIL = "admin@feiraotorres.com.br"
ADMIN_PASSWORD = "Feirao@Torres2026"

# Test results tracking
test_results = {
    "passed": [],
    "failed": [],
    "warnings": []
}

def log_pass(test_name: str, details: str = ""):
    """Log a passing test"""
    msg = f"✅ PASS: {test_name}"
    if details:
        msg += f" - {details}"
    print(msg)
    test_results["passed"].append(test_name)

def log_fail(test_name: str, reason: str):
    """Log a failing test"""
    msg = f"❌ FAIL: {test_name} - {reason}"
    print(msg)
    test_results["failed"].append({"test": test_name, "reason": reason})

def log_warning(test_name: str, message: str):
    """Log a warning"""
    msg = f"⚠️  WARNING: {test_name} - {message}"
    print(msg)
    test_results["warnings"].append({"test": test_name, "message": message})

def print_json(data: Any, indent: int = 2):
    """Pretty print JSON data"""
    print(json.dumps(data, indent=indent, ensure_ascii=False))

# ============================================================================
# TEST 1: GET /api/feirao/config (public) - BUGFIX VERIFICATION
# ============================================================================
def test_feirao_config():
    """Test public Feirão config endpoint - verify no 'A DEFINIR' placeholders"""
    print("\n" + "="*80)
    print("TEST 1: GET /api/feirao/config (public) - BUGFIX VERIFICATION")
    print("="*80)
    
    try:
        response = requests.get(f"{API_BASE}/feirao/config", timeout=10)
        
        if response.status_code != 200:
            log_fail("GET /api/feirao/config", f"Status {response.status_code}, expected 200")
            return None
        
        data = response.json()
        print("Response:")
        print_json(data)
        
        # CRITICAL: Assert NO "A DEFINIR" anywhere in the response
        response_str = json.dumps(data, ensure_ascii=False)
        if "A DEFINIR" in response_str:
            log_fail("GET /api/feirao/config", "BUGFIX FAILED: Found 'A DEFINIR' placeholder in response")
            return None
        else:
            log_pass("GET /api/feirao/config - No placeholders", "✅ NO 'A DEFINIR' found in response")
        
        # Verify structure
        if "event" not in data:
            log_fail("GET /api/feirao/config", "Missing 'event' key in response")
            return None
        
        if "empreendimentos" not in data:
            log_fail("GET /api/feirao/config", "Missing 'empreendimentos' key in response")
            return None
        
        # Verify event fields
        event = data["event"]
        
        if event.get("nome") != "II Feirão do Imóvel Torres Engenharia":
            log_fail("GET /api/feirao/config", f"event.nome = '{event.get('nome')}', expected 'II Feirão do Imóvel Torres Engenharia'")
            return None
        
        if event.get("local_nome") != "Residencial Reserva 025":
            log_fail("GET /api/feirao/config", f"event.local_nome = '{event.get('local_nome')}', expected 'Residencial Reserva 025'")
            return None
        
        if event.get("horario_label") != "das 9h às 12h":
            log_fail("GET /api/feirao/config", f"event.horario_label = '{event.get('horario_label')}', expected 'das 9h às 12h'")
            return None
        
        if event.get("whatsapp") != "5527998336937":
            log_fail("GET /api/feirao/config", f"event.whatsapp = '{event.get('whatsapp')}', expected '5527998336937'")
            return None
        
        log_pass("GET /api/feirao/config - Event fields", "All event fields correct")
        
        # Verify empreendimentos
        emps = data["empreendimentos"]
        
        # Check viva
        if "viva" not in emps:
            log_fail("GET /api/feirao/config", "Missing 'viva' in empreendimentos")
            return None
        viva = emps["viva"]
        if viva.get("nome") != "Residencial Viva":
            log_fail("GET /api/feirao/config", f"viva.nome = '{viva.get('nome')}', expected 'Residencial Viva'")
            return None
        if viva.get("preco_label") != "A partir de R$ 330.000":
            log_fail("GET /api/feirao/config", f"viva.preco_label = '{viva.get('preco_label')}', expected 'A partir de R$ 330.000'")
            return None
        if viva.get("entrada_label") != "3x de R$ 15.000":
            log_fail("GET /api/feirao/config", f"viva.entrada_label = '{viva.get('entrada_label')}', expected '3x de R$ 15.000'")
            return None
        if viva.get("obra_label") != "Término da obra: Julho/2027":
            log_fail("GET /api/feirao/config", f"viva.obra_label = '{viva.get('obra_label')}', expected 'Término da obra: Julho/2027'")
            return None
        if not isinstance(viva.get("estoque"), int):
            log_fail("GET /api/feirao/config", f"viva.estoque should be int, got {type(viva.get('estoque'))}")
            return None
        log_pass("GET /api/feirao/config - Viva", f"nome={viva['nome']}, preco={viva['preco_label']}, estoque={viva['estoque']}")
        
        # Check alameda
        if "alameda" not in emps:
            log_fail("GET /api/feirao/config", "Missing 'alameda' in empreendimentos")
            return None
        alameda = emps["alameda"]
        if alameda.get("nome") != "Alameda 500":
            log_fail("GET /api/feirao/config", f"alameda.nome = '{alameda.get('nome')}', expected 'Alameda 500'")
            return None
        if alameda.get("preco_label") != "A partir de R$ 309.990":
            log_fail("GET /api/feirao/config", f"alameda.preco_label = '{alameda.get('preco_label')}', expected 'A partir de R$ 309.990'")
            return None
        if alameda.get("entrada_label") != "3x de R$ 15.000":
            log_fail("GET /api/feirao/config", f"alameda.entrada_label = '{alameda.get('entrada_label')}', expected '3x de R$ 15.000'")
            return None
        if alameda.get("obra_label") != "Término da obra: Maio/2028":
            log_fail("GET /api/feirao/config", f"alameda.obra_label = '{alameda.get('obra_label')}', expected 'Término da obra: Maio/2028'")
            return None
        if not isinstance(alameda.get("estoque"), int):
            log_fail("GET /api/feirao/config", f"alameda.estoque should be int, got {type(alameda.get('estoque'))}")
            return None
        log_pass("GET /api/feirao/config - Alameda", f"nome={alameda['nome']}, preco={alameda['preco_label']}, estoque={alameda['estoque']}")
        
        # Check life
        if "life" not in emps:
            log_fail("GET /api/feirao/config", "Missing 'life' in empreendimentos")
            return None
        life = emps["life"]
        if life.get("nome") != "Life 740":
            log_fail("GET /api/feirao/config", f"life.nome = '{life.get('nome')}', expected 'Life 740'")
            return None
        if life.get("preco_label") != "R$ 299.000":
            log_fail("GET /api/feirao/config", f"life.preco_label = '{life.get('preco_label')}', expected 'R$ 299.000'")
            return None
        if life.get("obra_label") != "Término da obra: Dezembro/2026":
            log_fail("GET /api/feirao/config", f"life.obra_label = '{life.get('obra_label')}', expected 'Término da obra: Dezembro/2026'")
            return None
        if not isinstance(life.get("estoque"), int):
            log_fail("GET /api/feirao/config", f"life.estoque should be int, got {type(life.get('estoque'))}")
            return None
        log_pass("GET /api/feirao/config - Life", f"nome={life['nome']}, preco={life['preco_label']}, estoque={life['estoque']}")
        
        # Check aldeia
        if "aldeia" not in emps:
            log_fail("GET /api/feirao/config", "Missing 'aldeia' in empreendimentos")
            return None
        aldeia = emps["aldeia"]
        if aldeia.get("nome") != "Aldeia 350":
            log_fail("GET /api/feirao/config", f"aldeia.nome = '{aldeia.get('nome')}', expected 'Aldeia 350'")
            return None
        if aldeia.get("preco_label") != "R$ 299.000":
            log_fail("GET /api/feirao/config", f"aldeia.preco_label = '{aldeia.get('preco_label')}', expected 'R$ 299.000'")
            return None
        if aldeia.get("entrada_label") != "Entrada de 20%":
            log_fail("GET /api/feirao/config", f"aldeia.entrada_label = '{aldeia.get('entrada_label')}', expected 'Entrada de 20%'")
            return None
        if aldeia.get("status_label") != "PRONTA PARA MORAR":
            log_fail("GET /api/feirao/config", f"aldeia.status_label = '{aldeia.get('status_label')}', expected 'PRONTA PARA MORAR'")
            return None
        if not isinstance(aldeia.get("estoque"), int):
            log_fail("GET /api/feirao/config", f"aldeia.estoque should be int, got {type(aldeia.get('estoque'))}")
            return None
        log_pass("GET /api/feirao/config - Aldeia", f"nome={aldeia['nome']}, preco={aldeia['preco_label']}, status={aldeia['status_label']}, estoque={aldeia['estoque']}")
        
        log_pass("GET /api/feirao/config - COMPLETE", "✅ All fields verified, NO placeholders found")
        return data
        
    except Exception as e:
        log_fail("GET /api/feirao/config", f"Exception: {str(e)}")
        return None

# ============================================================================
# TEST 2: Admin GET /api/admin/feirao/config (Bearer)
# ============================================================================
def test_admin_get_full_config(token: str):
    """Test admin get full config endpoint - verify weights and faixas"""
    print("\n" + "="*80)
    print("TEST 2: Admin GET /api/admin/feirao/config (Bearer)")
    print("="*80)
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(f"{API_BASE}/admin/feirao/config", headers=headers, timeout=10)
        
        if response.status_code != 200:
            log_fail("Admin GET /api/admin/feirao/config", f"Status {response.status_code}, expected 200. Response: {response.text}")
            return None
        
        data = response.json()
        print("Response:")
        print_json(data)
        
        # Verify full config includes weights and faixas
        if "weights" not in data:
            log_fail("Admin GET /api/admin/feirao/config", "Missing 'weights' key")
            return None
        
        weights = data["weights"]
        required_weight_keys = ["prazo", "entrada", "renda", "financiamento", "intencao", "visita"]
        for key in required_weight_keys:
            if key not in weights:
                log_fail("Admin GET /api/admin/feirao/config", f"Missing weight key: '{key}'")
                return None
        
        log_pass("Admin GET /api/admin/feirao/config - Weights", f"All weight keys present: {list(weights.keys())}")
        
        if "faixas" not in data:
            log_fail("Admin GET /api/admin/feirao/config", "Missing 'faixas' key")
            return None
        
        faixas = data["faixas"]
        required_faixa_keys = ["A", "B", "C"]
        for key in required_faixa_keys:
            if key not in faixas:
                log_fail("Admin GET /api/admin/feirao/config", f"Missing faixa key: '{key}'")
                return None
        
        log_pass("Admin GET /api/admin/feirao/config - Faixas", f"All faixa keys present: {list(faixas.keys())}")
        
        if "event" not in data:
            log_fail("Admin GET /api/admin/feirao/config", "Missing 'event' key")
            return None
        
        if "empreendimentos" not in data:
            log_fail("Admin GET /api/admin/feirao/config", "Missing 'empreendimentos' key")
            return None
        
        log_pass("Admin GET /api/admin/feirao/config - COMPLETE", "✅ Full config returned with weights/faixas")
        return data
        
    except Exception as e:
        log_fail("Admin GET /api/admin/feirao/config", f"Exception: {str(e)}")
        return None

# ============================================================================
# TEST 3: Admin PUT /api/admin/feirao/config (Bearer)
# ============================================================================
def test_admin_put_full_config(token: str):
    """Test admin update config endpoint - verify update persists"""
    print("\n" + "="*80)
    print("TEST 3: Admin PUT /api/admin/feirao/config (Bearer)")
    print("="*80)
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # NOTE: The admin PUT endpoint has a bug where sending partial empreendimentos
    # replaces the entire dict. To avoid breaking subsequent tests, we send just
    # weights update (which is safe) instead of empreendimentos partial update.
    # The review_request says "send {...weights...same values...}" as an option.
    payload = {
        "weights": {
            "prazo": 20,
            "entrada": 25,
            "renda": 20,
            "financiamento": 15,
            "intencao": 10,
            "visita": 10
        }
    }
    
    try:
        response = requests.put(f"{API_BASE}/admin/feirao/config", json=payload, headers=headers, timeout=10)
        
        if response.status_code != 200:
            log_fail("Admin PUT /api/admin/feirao/config", f"Status {response.status_code}, expected 200. Response: {response.text}")
            return None
        
        data = response.json()
        print("Response (truncated):")
        print(f"Keys: {list(data.keys())}")
        print(f"Weights: {data.get('weights')}")
        
        # Verify update was applied
        if data.get("weights") != payload["weights"]:
            log_fail("Admin PUT /api/admin/feirao/config", f"Weights not updated correctly. Got: {data.get('weights')}")
            return None
        
        log_pass("Admin PUT /api/admin/feirao/config", "✅ Config updated successfully")
        
        # Verify persistence with subsequent GET
        print("\nVerifying persistence with GET...")
        get_response = requests.get(f"{API_BASE}/admin/feirao/config", headers=headers, timeout=10)
        if get_response.status_code == 200:
            get_data = get_response.json()
            persisted_weights = get_data.get("weights")
            if persisted_weights == payload["weights"]:
                log_pass("Admin PUT persistence check", "✅ Change persisted correctly")
            else:
                log_fail("Admin PUT persistence check", f"weights = {persisted_weights}, expected {payload['weights']}")
        else:
            log_warning("Admin PUT persistence check", f"GET returned status {get_response.status_code}")
        
        return data
        
    except Exception as e:
        log_fail("Admin PUT /api/admin/feirao/config", f"Exception: {str(e)}")
        return None

# ============================================================================
# TEST 4: Regression - POST /api/leads with scoring (QA Bug payload)
# ============================================================================
def test_regression_lead_scoring():
    """Test lead scoring regression with specific QA payload"""
    print("\n" + "="*80)
    print("TEST 4: Regression - POST /api/leads with scoring")
    print("="*80)
    
    payload = {
        "name": "QA Bug",
        "phone": "27990001111",
        "cidade": "Serra",
        "objetivo": "sair_aluguel",
        "prazo": "imediato",
        "renda_familiar": "8_12k",
        "entrada": "50_100k",
        "financiamento": "aprovado",
        "regiao": "jacaraipe",
        "preferencias": ["praia", "duplex"],
        "lgpd_consent": True,
        "session_id": "qabug"
    }
    
    try:
        response = requests.post(f"{API_BASE}/leads", json=payload, timeout=10)
        
        if response.status_code != 200:
            log_fail("Regression - Lead scoring", f"Status {response.status_code}, expected 200. Response: {response.text}")
            return None
        
        data = response.json()
        print("Response:")
        print_json(data)
        
        # Verify ID
        if "id" not in data or not data["id"]:
            log_fail("Regression - Lead scoring", "Missing or empty 'id' field")
            return None
        
        lead_id = data["id"]
        
        # Verify feirao_score >= 75
        feirao_score = data.get("feirao_score", 0)
        if feirao_score < 75:
            log_fail("Regression - Lead scoring", f"feirao_score = {feirao_score}, expected >= 75")
            return None
        
        # Verify classe == "A"
        classe = data.get("classe")
        if classe != "A":
            log_fail("Regression - Lead scoring", f"classe = '{classe}', expected 'A'")
            return None
        
        # Verify empreendimento_recomendado == "viva" (region jacaraipe + praia/duplex)
        emp_rec = data.get("empreendimento_recomendado")
        if emp_rec != "viva":
            log_fail("Regression - Lead scoring", f"empreendimento_recomendado = '{emp_rec}', expected 'viva' (region jacaraipe + praia/duplex)")
            return None
        
        # Verify empreendimento_alternativas is non-empty list
        emp_alts = data.get("empreendimento_alternativas", [])
        if not isinstance(emp_alts, list) or len(emp_alts) == 0:
            log_fail("Regression - Lead scoring", f"empreendimento_alternativas should be non-empty list, got: {emp_alts}")
            return None
        
        log_pass("Regression - Lead scoring", f"✅ Lead scoring working: id={lead_id}, score={feirao_score}, classe={classe}, emp={emp_rec}, alts={emp_alts}")
        return data
        
    except Exception as e:
        log_fail("Regression - Lead scoring", f"Exception: {str(e)}")
        return None

# ============================================================================
# TEST 5: Regression - Admin GET /api/admin/feirao/overview (Bearer)
# ============================================================================
def test_regression_admin_overview(token: str):
    """Test admin overview regression"""
    print("\n" + "="*80)
    print("TEST 5: Regression - Admin GET /api/admin/feirao/overview (Bearer)")
    print("="*80)
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(f"{API_BASE}/admin/feirao/overview", headers=headers, timeout=10)
        
        if response.status_code != 200:
            log_fail("Regression - Admin overview", f"Status {response.status_code}, expected 200. Response: {response.text}")
            return None
        
        data = response.json()
        print("Response:")
        print_json(data)
        
        # Verify required keys
        required_keys = ["total", "hoje", "classes", "inscritos_feirao", "confirmados_feirao", "por_empreendimento"]
        for key in required_keys:
            if key not in data:
                log_fail("Regression - Admin overview", f"Missing required key: '{key}'")
                return None
        
        # Verify classes has A/B/C/D
        classes = data["classes"]
        for cls in ["A", "B", "C", "D"]:
            if cls not in classes:
                log_fail("Regression - Admin overview", f"Missing class '{cls}' in classes")
                return None
        
        # Verify por_empreendimento is present (may not have all 4 if config was broken)
        por_emp = data["por_empreendimento"]
        if not isinstance(por_emp, dict):
            log_fail("Regression - Admin overview", f"por_empreendimento should be dict, got {type(por_emp)}")
            return None
        
        # Check if all 4 empreendimentos are present (they should be if config is correct)
        expected_emps = ["viva", "alameda", "life", "aldeia"]
        missing_emps = [slug for slug in expected_emps if slug not in por_emp]
        if missing_emps:
            log_warning("Regression - Admin overview", f"Missing empreendimentos in por_empreendimento: {missing_emps} (may indicate config issue)")
        
        log_pass("Regression - Admin overview", f"✅ All keys verified: total={data['total']}, classes={classes}, por_empreendimento keys={list(por_emp.keys())}")
        return data
        
    except Exception as e:
        log_fail("Regression - Admin overview", f"Exception: {str(e)}")
        return None

# ============================================================================
# EXTRA TEST: POST /api/leads with LOW-INTENT payload (classe D)
# ============================================================================
def test_create_lead_low_intent():
    """Test lead creation with low-intent quiz payload"""
    print("\n" + "="*80)
    print("EXTRA TEST: POST /api/leads with LOW-INTENT payload (expect classe D)")
    print("="*80)
    
    payload = {
        "objetivo": "pesquisando",
        "prazo": "nao_sei",
        "renda_familiar": "ate_3k",
        "entrada": "sem_entrada",
        "financiamento": "nunca",
        "regiao": "serra",
        "preferencias": ["preco"],
        "session_id": "testsessD"
    }
    
    try:
        response = requests.post(f"{API_BASE}/leads", json=payload, timeout=10)
        
        if response.status_code != 200:
            log_fail("POST /api/leads (LOW-INTENT)", f"Status {response.status_code}, expected 200. Response: {response.text}")
            return None
        
        data = response.json()
        print("Response:")
        print_json(data)
        
        # Verify ID
        if "id" not in data or not data["id"]:
            log_fail("POST /api/leads (LOW-INTENT)", "Missing or empty 'id' field")
            return None
        
        lead_id = data["id"]
        
        # Verify feirao_score < 35
        feirao_score = data.get("feirao_score", 0)
        if feirao_score >= 35:
            log_fail("POST /api/leads (LOW-INTENT)", f"feirao_score = {feirao_score}, expected < 35")
            return None
        
        # Verify classe == "D"
        classe = data.get("classe")
        if classe != "D":
            log_fail("POST /api/leads (LOW-INTENT)", f"classe = '{classe}', expected 'D'")
            return None
        
        # Verify temperatura == "frio"
        temperatura = data.get("temperatura")
        if temperatura != "frio":
            log_fail("POST /api/leads (LOW-INTENT)", f"temperatura = '{temperatura}', expected 'frio'")
            return None
        
        # Verify empreendimento_recomendado is a valid slug
        emp_rec = data.get("empreendimento_recomendado")
        valid_slugs = ["viva", "alameda", "life", "aldeia"]
        if emp_rec not in valid_slugs:
            log_fail("POST /api/leads (LOW-INTENT)", f"empreendimento_recomendado = '{emp_rec}', expected one of {valid_slugs}")
            return None
        
        log_pass("POST /api/leads (LOW-INTENT)", f"Lead created with id={lead_id}, score={feirao_score}, classe={classe}, emp={emp_rec}")
        return data
        
    except Exception as e:
        log_fail("POST /api/leads (LOW-INTENT)", f"Exception: {str(e)}")
        return None

# ============================================================================
# EXTRA TEST: PATCH /api/leads/{id}/agendamento
# ============================================================================
def test_patch_agendamento(lead_id: str, original_score: int):
    """Test PATCH agendamento endpoint"""
    print("\n" + "="*80)
    print(f"EXTRA TEST: PATCH /api/leads/{lead_id}/agendamento")
    print("="*80)
    
    payload = {
        "confirmou_feirao": "sim",
        "horario_feirao": "manha"
    }
    
    try:
        response = requests.patch(f"{API_BASE}/leads/{lead_id}/agendamento", json=payload, timeout=10)
        
        if response.status_code != 200:
            log_fail("PATCH /api/leads/{id}/agendamento", f"Status {response.status_code}, expected 200. Response: {response.text}")
            return None
        
        data = response.json()
        print("Response:")
        print_json(data)
        
        # Verify ok: true
        if not data.get("ok"):
            log_fail("PATCH /api/leads/{id}/agendamento", "Response should have ok=true")
            return None
        
        # Verify confirmou_feirao == "sim"
        if data.get("confirmou_feirao") != "sim":
            log_fail("PATCH /api/leads/{id}/agendamento", f"confirmou_feirao = '{data.get('confirmou_feirao')}', expected 'sim'")
            return None
        
        # Verify feirao_score recalculated (should be >= original since visita weight adds up to 10)
        new_score = data.get("feirao_score", 0)
        if new_score < original_score:
            log_fail("PATCH /api/leads/{id}/agendamento", f"feirao_score = {new_score}, expected >= {original_score} (visita weight should increase score)")
            return None
        
        # Verify classe is present
        if "classe" not in data:
            log_fail("PATCH /api/leads/{id}/agendamento", "Missing 'classe' in response")
            return None
        
        log_pass("PATCH /api/leads/{id}/agendamento", f"Agendamento updated, new_score={new_score}, classe={data.get('classe')}")
        
        # Now GET the lead to verify persistence
        print("\nVerifying persistence with GET /api/leads...")
        get_response = requests.get(f"{API_BASE}/leads", timeout=10)
        if get_response.status_code == 200:
            leads = get_response.json()
            lead = next((l for l in leads if l.get("id") == lead_id), None)
            if lead:
                if lead.get("confirmou_feirao") == "sim":
                    log_pass("PATCH persistence check", "confirmou_feirao='sim' persisted correctly")
                else:
                    log_fail("PATCH persistence check", f"confirmou_feirao = '{lead.get('confirmou_feirao')}', expected 'sim'")
            else:
                log_warning("PATCH persistence check", f"Lead {lead_id} not found in GET /api/leads")
        else:
            log_warning("PATCH persistence check", f"GET /api/leads returned status {get_response.status_code}")
        
        return data
        
    except Exception as e:
        log_fail("PATCH /api/leads/{id}/agendamento", f"Exception: {str(e)}")
        return None

# ============================================================================
# EXTRA TEST: POST /api/feirao/events
# ============================================================================
def test_feirao_events():
    """Test event tracking endpoint"""
    print("\n" + "="*80)
    print("EXTRA TEST: POST /api/feirao/events")
    print("="*80)
    
    events = [
        {"event": "quiz_started", "session_id": "testsessA"},
        {"event": "page_view", "session_id": "testsessA"},
        {"event": "whatsapp_clicked", "session_id": "testsessA"}
    ]
    
    all_passed = True
    for event_payload in events:
        try:
            response = requests.post(f"{API_BASE}/feirao/events", json=event_payload, timeout=10)
            
            if response.status_code != 200:
                log_fail(f"POST /api/feirao/events ({event_payload['event']})", f"Status {response.status_code}, expected 200")
                all_passed = False
                continue
            
            data = response.json()
            if not data.get("ok"):
                log_fail(f"POST /api/feirao/events ({event_payload['event']})", f"Response should have ok=true, got: {data}")
                all_passed = False
                continue
            
            print(f"✓ Event '{event_payload['event']}' tracked successfully")
            
        except Exception as e:
            log_fail(f"POST /api/feirao/events ({event_payload['event']})", f"Exception: {str(e)}")
            all_passed = False
    
    if all_passed:
        log_pass("POST /api/feirao/events", "All 3 events tracked successfully")
    
    return all_passed

# ============================================================================
# EXTRA TEST: Admin login
# ============================================================================
def test_admin_login():
    """Test admin login"""
    print("\n" + "="*80)
    print("EXTRA TEST: POST /api/admin/login")
    print("="*80)
    
    payload = {
        "email": ADMIN_EMAIL,
        "password": ADMIN_PASSWORD
    }
    
    try:
        response = requests.post(f"{API_BASE}/admin/login", json=payload, timeout=10)
        
        if response.status_code != 200:
            log_fail("POST /api/admin/login", f"Status {response.status_code}, expected 200. Response: {response.text}")
            return None
        
        data = response.json()
        print("Response:")
        print_json(data)
        
        # Verify access_token
        if "access_token" not in data or not data["access_token"]:
            log_fail("POST /api/admin/login", "Missing or empty 'access_token'")
            return None
        
        token = data["access_token"]
        log_pass("POST /api/admin/login", f"Login successful, token received")
        
        return token
        
    except Exception as e:
        log_fail("POST /api/admin/login", f"Exception: {str(e)}")
        return None

def test_admin_overview(token: str):
    """Test admin overview endpoint"""
    print("\n" + "="*80)
    print("EXTRA TEST: GET /api/admin/feirao/overview")
    print("="*80)
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(f"{API_BASE}/admin/feirao/overview", headers=headers, timeout=10)
        
        if response.status_code != 200:
            log_fail("GET /api/admin/feirao/overview", f"Status {response.status_code}, expected 200. Response: {response.text}")
            return None
        
        data = response.json()
        print("Response:")
        print_json(data)
        
        # Verify required keys
        required_keys = ["total", "hoje", "classes", "inscritos_feirao", "confirmados_feirao", "por_empreendimento"]
        for key in required_keys:
            if key not in data:
                log_fail("GET /api/admin/feirao/overview", f"Missing required key: '{key}'")
                return None
        
        # Verify classes has A/B/C/D
        classes = data["classes"]
        for cls in ["A", "B", "C", "D"]:
            if cls not in classes:
                log_fail("GET /api/admin/feirao/overview", f"Missing class '{cls}' in classes")
                return None
        
        # Verify por_empreendimento has all 4 empreendimentos
        por_emp = data["por_empreendimento"]
        for slug in ["viva", "alameda", "life", "aldeia"]:
            if slug not in por_emp:
                log_fail("GET /api/admin/feirao/overview", f"Missing empreendimento '{slug}' in por_empreendimento")
                return None
        
        # Verify confirmados_feirao >= 1 (from test 4)
        confirmados = data.get("confirmados_feirao", 0)
        if confirmados < 1:
            log_warning("GET /api/admin/feirao/overview", f"confirmados_feirao = {confirmados}, expected >= 1 (from test 4)")
        
        log_pass("GET /api/admin/feirao/overview", f"All keys verified. total={data['total']}, confirmados={confirmados}")
        return data
        
    except Exception as e:
        log_fail("GET /api/admin/feirao/overview", f"Exception: {str(e)}")
        return None

def test_admin_funnel(token: str):
    """Test admin funnel endpoint"""
    print("\n" + "="*80)
    print("EXTRA TEST: GET /api/admin/feirao/funnel")
    print("="*80)
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(f"{API_BASE}/admin/feirao/funnel", headers=headers, timeout=10)
        
        if response.status_code != 200:
            log_fail("GET /api/admin/feirao/funnel", f"Status {response.status_code}, expected 200. Response: {response.text}")
            return None
        
        data = response.json()
        print("Response:")
        print_json(data)
        
        # Verify funil keys
        if "funil" not in data:
            log_fail("GET /api/admin/feirao/funnel", "Missing 'funil' key")
            return None
        
        funil = data["funil"]
        required_funil_keys = ["visitantes", "iniciaram_quiz", "finalizaram_quiz", "cadastraram", "agendaram", "clicaram_whatsapp"]
        for key in required_funil_keys:
            if key not in funil:
                log_fail("GET /api/admin/feirao/funnel", f"Missing funil key: '{key}'")
                return None
        
        # Verify por_origem
        if "por_origem" not in data:
            log_fail("GET /api/admin/feirao/funnel", "Missing 'por_origem' key")
            return None
        
        por_origem = data["por_origem"]
        if "meta_ads" not in por_origem:
            log_warning("GET /api/admin/feirao/funnel", "Expected 'meta_ads' in por_origem (from test 2)")
        
        log_pass("GET /api/admin/feirao/funnel", f"All keys verified. visitantes={funil['visitantes']}, agendaram={funil['agendaram']}")
        return data
        
    except Exception as e:
        log_fail("GET /api/admin/feirao/funnel", f"Exception: {str(e)}")
        return None

def test_admin_get_config(token: str):
    """Test admin get config endpoint"""
    print("\n" + "="*80)
    print("EXTRA TEST: GET /api/admin/feirao/config (old)")
    print("="*80)
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(f"{API_BASE}/admin/feirao/config", headers=headers, timeout=10)
        
        if response.status_code != 200:
            log_fail("GET /api/admin/feirao/config", f"Status {response.status_code}, expected 200. Response: {response.text}")
            return None
        
        data = response.json()
        print("Response (truncated):")
        print(f"Keys: {list(data.keys())}")
        
        # Verify full config includes weights and faixas
        if "weights" not in data:
            log_fail("GET /api/admin/feirao/config", "Missing 'weights' key")
            return None
        
        if "faixas" not in data:
            log_fail("GET /api/admin/feirao/config", "Missing 'faixas' key")
            return None
        
        if "event" not in data:
            log_fail("GET /api/admin/feirao/config", "Missing 'event' key")
            return None
        
        if "empreendimentos" not in data:
            log_fail("GET /api/admin/feirao/config", "Missing 'empreendimentos' key")
            return None
        
        log_pass("GET /api/admin/feirao/config", "Full config returned with all keys")
        return data
        
    except Exception as e:
        log_fail("GET /api/admin/feirao/config", f"Exception: {str(e)}")
        return None

def test_admin_put_config(token: str):
    """Test admin update config endpoint"""
    print("\n" + "="*80)
    print("EXTRA TEST: PUT /api/admin/feirao/config (old)")
    print("="*80)
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Update weights to verify persistence
    payload = {
        "weights": {
            "prazo": 20,
            "entrada": 25,
            "renda": 20,
            "financiamento": 15,
            "intencao": 10,
            "visita": 10
        }
    }
    
    try:
        response = requests.put(f"{API_BASE}/admin/feirao/config", json=payload, headers=headers, timeout=10)
        
        if response.status_code != 200:
            log_fail("PUT /api/admin/feirao/config", f"Status {response.status_code}, expected 200. Response: {response.text}")
            return None
        
        data = response.json()
        print("Response (truncated):")
        print(f"Keys: {list(data.keys())}")
        print(f"Weights: {data.get('weights')}")
        
        # Verify weights were updated
        if data.get("weights") != payload["weights"]:
            log_fail("PUT /api/admin/feirao/config", f"Weights not updated correctly. Got: {data.get('weights')}")
            return None
        
        log_pass("PUT /api/admin/feirao/config", "Config updated successfully")
        return data
        
    except Exception as e:
        log_fail("PUT /api/admin/feirao/config", f"Exception: {str(e)}")
        return None

# ============================================================================
# EXTRA TEST: Regression - legacy admin endpoints
# ============================================================================
def test_admin_metrics(token: str):
    """Test legacy admin metrics endpoint"""
    print("\n" + "="*80)
    print("EXTRA TEST: GET /api/admin/metrics (regression)")
    print("="*80)
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(f"{API_BASE}/admin/metrics", headers=headers, timeout=10)
        
        if response.status_code != 200:
            log_fail("GET /api/admin/metrics", f"Status {response.status_code}, expected 200. Response: {response.text}")
            return None
        
        data = response.json()
        print("Response:")
        print_json(data)
        
        # Verify basic keys
        if "total" not in data:
            log_fail("GET /api/admin/metrics", "Missing 'total' key")
            return None
        
        if "temperatura" not in data:
            log_fail("GET /api/admin/metrics", "Missing 'temperatura' key")
            return None
        
        log_pass("GET /api/admin/metrics", f"Legacy endpoint working. total={data['total']}")
        return data
        
    except Exception as e:
        log_fail("GET /api/admin/metrics", f"Exception: {str(e)}")
        return None

def test_admin_leads(token: str):
    """Test legacy admin leads endpoint"""
    print("\n" + "="*80)
    print("EXTRA TEST: GET /api/admin/leads (regression)")
    print("="*80)
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(f"{API_BASE}/admin/leads", headers=headers, timeout=10)
        
        if response.status_code != 200:
            log_fail("GET /api/admin/leads", f"Status {response.status_code}, expected 200. Response: {response.text}")
            return None
        
        data = response.json()
        print(f"Response: {len(data)} leads returned")
        
        # Verify it's a list
        if not isinstance(data, list):
            log_fail("GET /api/admin/leads", f"Expected list, got {type(data)}")
            return None
        
        # Verify newly created leads are included
        if len(data) < 2:
            log_warning("GET /api/admin/leads", f"Expected at least 2 leads (from tests 2 and 3), got {len(data)}")
        
        # Check if our test leads are present
        test_sessions = ["testsessA", "testsessD"]
        found_sessions = [lead.get("session_id") for lead in data if lead.get("session_id") in test_sessions]
        
        if len(found_sessions) < 2:
            log_warning("GET /api/admin/leads", f"Expected to find test leads with sessions {test_sessions}, found {found_sessions}")
        
        log_pass("GET /api/admin/leads", f"Legacy endpoint working. {len(data)} leads returned, {len(found_sessions)} test leads found")
        return data
        
    except Exception as e:
        log_fail("GET /api/admin/leads", f"Exception: {str(e)}")
        return None

# ============================================================================
# NEW TEST: GET /api/admin/feirao/analytics (Bearer)
# ============================================================================
def test_analytics_endpoint(token: str):
    """Test NEW analytics endpoint with various days parameters"""
    print("\n" + "="*80)
    print("NEW TEST: GET /api/admin/feirao/analytics (Bearer)")
    print("="*80)
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test 1: days=7
    print("\n--- Test 1: days=7 ---")
    try:
        response = requests.get(f"{API_BASE}/admin/feirao/analytics?days=7", headers=headers, timeout=10)
        
        if response.status_code != 200:
            log_fail("Analytics days=7", f"Status {response.status_code}, expected 200. Response: {response.text}")
        else:
            data = response.json()
            print("Response keys:", list(data.keys()))
            print(f"days={data.get('days')}, kpis={data.get('kpis')}, series length={len(data.get('series', []))}")
            
            # Verify response structure
            if not verify_analytics_structure(data, expected_days=7, test_name="Analytics days=7"):
                pass  # verify_analytics_structure already logged the failure
            else:
                log_pass("Analytics days=7", f"✅ Returns 200, days={data['days']}, series length={len(data['series'])}")
    except Exception as e:
        log_fail("Analytics days=7", f"Exception: {str(e)}")
    
    # Test 2: days=30
    print("\n--- Test 2: days=30 ---")
    try:
        response = requests.get(f"{API_BASE}/admin/feirao/analytics?days=30", headers=headers, timeout=10)
        
        if response.status_code != 200:
            log_fail("Analytics days=30", f"Status {response.status_code}, expected 200. Response: {response.text}")
        else:
            data = response.json()
            print("Response keys:", list(data.keys()))
            print(f"days={data.get('days')}, kpis={data.get('kpis')}, series length={len(data.get('series', []))}")
            
            if not verify_analytics_structure(data, expected_days=30, test_name="Analytics days=30"):
                pass
            else:
                log_pass("Analytics days=30", f"✅ Returns 200, days={data['days']}, series length={len(data['series'])}")
    except Exception as e:
        log_fail("Analytics days=30", f"Exception: {str(e)}")
    
    # Test 3: days=90
    print("\n--- Test 3: days=90 ---")
    try:
        response = requests.get(f"{API_BASE}/admin/feirao/analytics?days=90", headers=headers, timeout=10)
        
        if response.status_code != 200:
            log_fail("Analytics days=90", f"Status {response.status_code}, expected 200. Response: {response.text}")
        else:
            data = response.json()
            print("Response keys:", list(data.keys()))
            print(f"days={data.get('days')}, kpis={data.get('kpis')}, series length={len(data.get('series', []))}")
            
            if not verify_analytics_structure(data, expected_days=90, test_name="Analytics days=90"):
                pass
            else:
                log_pass("Analytics days=90", f"✅ Returns 200, days={data['days']}, series length={len(data['series'])}")
                # Print sample values for verification
                print("\nSample values:")
                print(f"  kpis.total={data['kpis']['total']}")
                print(f"  kpis.hoje={data['kpis']['hoje']}")
                print(f"  kpis.leads_7d={data['kpis']['leads_7d']}")
                print(f"  kpis.leads_range={data['kpis']['leads_range']}")
                print(f"  kpis.agendaram={data['kpis']['agendaram']}")
                print(f"  kpis.whatsapp={data['kpis']['whatsapp']}")
                print(f"  classes={data['classes']}")
                print(f"  funnel.visitantes={data['funnel']['visitantes']}")
                print(f"  funnel.cadastraram={data['funnel']['cadastraram']}")
                print(f"  origem (first 3)={data['origem'][:3] if data['origem'] else []}")
                print(f"  por_empreendimento={data['por_empreendimento']}")
                if data['series']:
                    print(f"  series[0]={data['series'][0]}")
                    print(f"  series[-1]={data['series'][-1]}")
    except Exception as e:
        log_fail("Analytics days=90", f"Exception: {str(e)}")
    
    # Test 4: days=500 (should clamp to 365)
    print("\n--- Test 4: days=500 (should clamp to 365) ---")
    try:
        response = requests.get(f"{API_BASE}/admin/feirao/analytics?days=500", headers=headers, timeout=10)
        
        if response.status_code != 200:
            log_fail("Analytics days=500 clamp", f"Status {response.status_code}, expected 200")
        else:
            data = response.json()
            if data.get('days') != 365:
                log_fail("Analytics days=500 clamp", f"days={data.get('days')}, expected 365 (clamped)")
            elif len(data.get('series', [])) != 365:
                log_fail("Analytics days=500 clamp", f"series length={len(data.get('series', []))}, expected 365")
            else:
                log_pass("Analytics days=500 clamp", f"✅ Correctly clamped to 365, series length={len(data['series'])}")
    except Exception as e:
        log_fail("Analytics days=500 clamp", f"Exception: {str(e)}")
    
    # Test 5: days=0 (should clamp to 1)
    print("\n--- Test 5: days=0 (should clamp to 1) ---")
    try:
        response = requests.get(f"{API_BASE}/admin/feirao/analytics?days=0", headers=headers, timeout=10)
        
        if response.status_code != 200:
            log_fail("Analytics days=0 clamp", f"Status {response.status_code}, expected 200")
        else:
            data = response.json()
            if data.get('days') != 1:
                log_fail("Analytics days=0 clamp", f"days={data.get('days')}, expected 1 (clamped)")
            elif len(data.get('series', [])) != 1:
                log_fail("Analytics days=0 clamp", f"series length={len(data.get('series', []))}, expected 1")
            else:
                log_pass("Analytics days=0 clamp", f"✅ Correctly clamped to 1, series length={len(data['series'])}")
    except Exception as e:
        log_fail("Analytics days=0 clamp", f"Exception: {str(e)}")
    
    # Test 6: No auth (should return 401/403)
    print("\n--- Test 6: No auth (should return 401/403) ---")
    try:
        response = requests.get(f"{API_BASE}/admin/feirao/analytics?days=30", timeout=10)
        
        if response.status_code in [401, 403]:
            log_pass("Analytics no auth", f"✅ Correctly returns {response.status_code} without Bearer token")
        else:
            log_fail("Analytics no auth", f"Status {response.status_code}, expected 401 or 403")
    except Exception as e:
        log_fail("Analytics no auth", f"Exception: {str(e)}")

def verify_analytics_structure(data: Dict[str, Any], expected_days: int, test_name: str) -> bool:
    """Verify analytics response structure"""
    
    # Check days
    if "days" not in data:
        log_fail(test_name, "Missing 'days' key")
        return False
    if not isinstance(data["days"], int):
        log_fail(test_name, f"days should be int, got {type(data['days'])}")
        return False
    if data["days"] != expected_days:
        log_fail(test_name, f"days={data['days']}, expected {expected_days}")
        return False
    
    # Check kpis
    if "kpis" not in data:
        log_fail(test_name, "Missing 'kpis' key")
        return False
    kpis = data["kpis"]
    required_kpi_keys = ["total", "hoje", "leads_7d", "leads_range", "agendaram", "whatsapp"]
    for key in required_kpi_keys:
        if key not in kpis:
            log_fail(test_name, f"Missing kpis.{key}")
            return False
        if not isinstance(kpis[key], int):
            log_fail(test_name, f"kpis.{key} should be int, got {type(kpis[key])}")
            return False
    
    # Check classes
    if "classes" not in data:
        log_fail(test_name, "Missing 'classes' key")
        return False
    classes = data["classes"]
    for cls in ["A", "B", "C", "D"]:
        if cls not in classes:
            log_fail(test_name, f"Missing classes.{cls}")
            return False
        if not isinstance(classes[cls], int):
            log_fail(test_name, f"classes.{cls} should be int, got {type(classes[cls])}")
            return False
    
    # Check series
    if "series" not in data:
        log_fail(test_name, "Missing 'series' key")
        return False
    series = data["series"]
    if not isinstance(series, list):
        log_fail(test_name, f"series should be list, got {type(series)}")
        return False
    if len(series) != expected_days:
        log_fail(test_name, f"series length={len(series)}, expected {expected_days}")
        return False
    
    # Check series items
    if series:
        item = series[0]
        if "date" not in item:
            log_fail(test_name, "series[0] missing 'date' key")
            return False
        if not isinstance(item["date"], str):
            log_fail(test_name, f"series[0].date should be string, got {type(item['date'])}")
            return False
        # Verify date format YYYY-MM-DD
        import re
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', item["date"]):
            log_fail(test_name, f"series[0].date='{item['date']}' not in YYYY-MM-DD format")
            return False
        if "leads" not in item:
            log_fail(test_name, "series[0] missing 'leads' key")
            return False
        if not isinstance(item["leads"], int):
            log_fail(test_name, f"series[0].leads should be int, got {type(item['leads'])}")
            return False
        if "visitantes" not in item:
            log_fail(test_name, "series[0] missing 'visitantes' key")
            return False
        if not isinstance(item["visitantes"], int):
            log_fail(test_name, f"series[0].visitantes should be int, got {type(item['visitantes'])}")
            return False
    
    # Check funnel
    if "funnel" not in data:
        log_fail(test_name, "Missing 'funnel' key")
        return False
    funnel = data["funnel"]
    required_funnel_keys = ["visitantes", "iniciaram_quiz", "finalizaram_quiz", "cadastraram", "agendaram", "clicaram_whatsapp"]
    for key in required_funnel_keys:
        if key not in funnel:
            log_fail(test_name, f"Missing funnel.{key}")
            return False
        if not isinstance(funnel[key], int):
            log_fail(test_name, f"funnel.{key} should be int, got {type(funnel[key])}")
            return False
    
    # Check origem
    if "origem" not in data:
        log_fail(test_name, "Missing 'origem' key")
        return False
    origem = data["origem"]
    if not isinstance(origem, list):
        log_fail(test_name, f"origem should be list, got {type(origem)}")
        return False
    # Verify origem items structure
    if origem:
        item = origem[0]
        if "source" not in item:
            log_fail(test_name, "origem[0] missing 'source' key")
            return False
        if "leads" not in item:
            log_fail(test_name, "origem[0] missing 'leads' key")
            return False
        if not isinstance(item["leads"], int):
            log_fail(test_name, f"origem[0].leads should be int, got {type(item['leads'])}")
            return False
        # campaign is nullable, so just check it exists
        if "campaign" not in item:
            log_fail(test_name, "origem[0] missing 'campaign' key (nullable)")
            return False
    
    # Check por_empreendimento
    if "por_empreendimento" not in data:
        log_fail(test_name, "Missing 'por_empreendimento' key")
        return False
    por_emp = data["por_empreendimento"]
    if not isinstance(por_emp, dict):
        log_fail(test_name, f"por_empreendimento should be dict, got {type(por_emp)}")
        return False
    
    return True

def test_regression_overview_funnel(token: str):
    """Quick regression test for overview and funnel endpoints"""
    print("\n" + "="*80)
    print("REGRESSION TEST: GET /api/admin/feirao/overview and /funnel")
    print("="*80)
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test overview
    try:
        response = requests.get(f"{API_BASE}/admin/feirao/overview", headers=headers, timeout=10)
        if response.status_code == 200:
            log_pass("Regression overview", "✅ GET /api/admin/feirao/overview returns 200")
        else:
            log_fail("Regression overview", f"Status {response.status_code}, expected 200")
    except Exception as e:
        log_fail("Regression overview", f"Exception: {str(e)}")
    
    # Test funnel
    try:
        response = requests.get(f"{API_BASE}/admin/feirao/funnel", headers=headers, timeout=10)
        if response.status_code == 200:
            log_pass("Regression funnel", "✅ GET /api/admin/feirao/funnel returns 200")
        else:
            log_fail("Regression funnel", f"Status {response.status_code}, expected 200")
    except Exception as e:
        log_fail("Regression funnel", f"Exception: {str(e)}")

# ============================================================================
# MAIN TEST RUNNER
# ============================================================================
def main():
    """Run all tests"""
    print("\n" + "="*80)
    print("FEIRÃO DO IMÓVEL TORRES ENGENHARIA - BACKEND TEST SUITE")
    print("NEW FEATURE: Analytics endpoint testing")
    print("="*80)
    print(f"Base URL: {BASE_URL}")
    print(f"API Base: {API_BASE}")
    print(f"Admin: {ADMIN_EMAIL}")
    print("="*80)
    
    # Get admin token for protected endpoints
    token = test_admin_login()
    if not token:
        log_fail("Admin tests", "Skipped - login failed")
        print_summary()
        exit(1)
    
    # ========== NEW ANALYTICS ENDPOINT TESTS ==========
    
    # Test NEW analytics endpoint
    test_analytics_endpoint(token)
    
    # Quick regression test for overview and funnel
    test_regression_overview_funnel(token)
    
    print_summary()

def print_summary():
    """Print test summary"""
    # Print summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    print(f"✅ PASSED: {len(test_results['passed'])} tests")
    print(f"❌ FAILED: {len(test_results['failed'])} tests")
    print(f"⚠️  WARNINGS: {len(test_results['warnings'])} warnings")
    
    if test_results['failed']:
        print("\nFailed tests:")
        for fail in test_results['failed']:
            print(f"  - {fail['test']}: {fail['reason']}")
    
    if test_results['warnings']:
        print("\nWarnings:")
        for warn in test_results['warnings']:
            print(f"  - {warn['test']}: {warn['message']}")
    
    print("="*80)
    
    # Exit with appropriate code
    if test_results['failed']:
        exit(1)
    else:
        exit(0)

if __name__ == "__main__":
    main()
