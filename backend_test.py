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
# TEST 1: GET /api/feirao/config (public)
# ============================================================================
def test_feirao_config():
    """Test public Feirão config endpoint"""
    print("\n" + "="*80)
    print("TEST 1: GET /api/feirao/config (public)")
    print("="*80)
    
    try:
        response = requests.get(f"{API_BASE}/feirao/config", timeout=10)
        
        if response.status_code != 200:
            log_fail("GET /api/feirao/config", f"Status {response.status_code}, expected 200")
            return None
        
        data = response.json()
        print("Response:")
        print_json(data)
        
        # Verify structure
        if "event" not in data:
            log_fail("GET /api/feirao/config", "Missing 'event' key in response")
            return None
        
        if "empreendimentos" not in data:
            log_fail("GET /api/feirao/config", "Missing 'empreendimentos' key in response")
            return None
        
        # Verify event fields
        event = data["event"]
        if event.get("data_label") != "19 de setembro de 2026":
            log_warning("GET /api/feirao/config", f"event.data_label = '{event.get('data_label')}', expected '19 de setembro de 2026'")
        
        if event.get("local_nome") != "Residencial Reserva (Reserva 025)":
            log_warning("GET /api/feirao/config", f"event.local_nome = '{event.get('local_nome')}', expected 'Residencial Reserva (Reserva 025)'")
        
        if event.get("whatsapp") != "5527998336937":
            log_fail("GET /api/feirao/config", f"event.whatsapp = '{event.get('whatsapp')}', expected '5527998336937'")
            return None
        
        # Verify empreendimentos
        emps = data["empreendimentos"]
        
        # Check viva
        if "viva" not in emps:
            log_fail("GET /api/feirao/config", "Missing 'viva' in empreendimentos")
            return None
        if emps["viva"].get("estoque") != 8:
            log_fail("GET /api/feirao/config", f"viva.estoque = {emps['viva'].get('estoque')}, expected 8")
            return None
        
        # Check alameda
        if "alameda" not in emps:
            log_fail("GET /api/feirao/config", "Missing 'alameda' in empreendimentos")
            return None
        if emps["alameda"].get("estoque") != 5:
            log_fail("GET /api/feirao/config", f"alameda.estoque = {emps['alameda'].get('estoque')}, expected 5")
            return None
        
        # Check life
        if "life" not in emps:
            log_fail("GET /api/feirao/config", "Missing 'life' in empreendimentos")
            return None
        if emps["life"].get("estoque") != 1:
            log_fail("GET /api/feirao/config", f"life.estoque = {emps['life'].get('estoque')}, expected 1")
            return None
        if not emps["life"].get("ultima_unidade"):
            log_fail("GET /api/feirao/config", "life.ultima_unidade should be true")
            return None
        
        # Check aldeia
        if "aldeia" not in emps:
            log_fail("GET /api/feirao/config", "Missing 'aldeia' in empreendimentos")
            return None
        if emps["aldeia"].get("estoque") != 1:
            log_fail("GET /api/feirao/config", f"aldeia.estoque = {emps['aldeia'].get('estoque')}, expected 1")
            return None
        if not emps["aldeia"].get("ultima_unidade"):
            log_fail("GET /api/feirao/config", "aldeia.ultima_unidade should be true")
            return None
        
        log_pass("GET /api/feirao/config", "All fields verified correctly")
        return data
        
    except Exception as e:
        log_fail("GET /api/feirao/config", f"Exception: {str(e)}")
        return None

# ============================================================================
# TEST 2: POST /api/leads with HIGH-INTENT payload (classe A)
# ============================================================================
def test_create_lead_high_intent():
    """Test lead creation with high-intent quiz payload"""
    print("\n" + "="*80)
    print("TEST 2: POST /api/leads with HIGH-INTENT payload (expect classe A)")
    print("="*80)
    
    payload = {
        "name": "Henrique A",
        "phone": "27999990001",
        "email": "a@t.com",
        "cidade": "Serra",
        "objetivo": "sair_aluguel",
        "prazo": "imediato",
        "renda_familiar": "8_12k",
        "composicao_renda": "conjuge",
        "tipo_renda": ["clt"],
        "fgts": "sim",
        "fgts_valor": "30_50k",
        "entrada": "50_100k",
        "moradia": "aluguel",
        "financiamento": "aprovado",
        "restricao": "nao",
        "regiao": "jacaraipe",
        "preferencias": ["praia", "duplex", "quintal"],
        "lgpd_consent": True,
        "utm": {"source": "meta_ads"},
        "session_id": "testsessA"
    }
    
    try:
        response = requests.post(f"{API_BASE}/leads", json=payload, timeout=10)
        
        if response.status_code != 200:
            log_fail("POST /api/leads (HIGH-INTENT)", f"Status {response.status_code}, expected 200. Response: {response.text}")
            return None
        
        data = response.json()
        print("Response:")
        print_json(data)
        
        # Verify ID
        if "id" not in data or not data["id"]:
            log_fail("POST /api/leads (HIGH-INTENT)", "Missing or empty 'id' field")
            return None
        
        lead_id = data["id"]
        
        # Verify feirao_score >= 75
        feirao_score = data.get("feirao_score", 0)
        if feirao_score < 75:
            log_fail("POST /api/leads (HIGH-INTENT)", f"feirao_score = {feirao_score}, expected >= 75")
            return None
        
        # Verify classe == "A"
        classe = data.get("classe")
        if classe != "A":
            log_fail("POST /api/leads (HIGH-INTENT)", f"classe = '{classe}', expected 'A'")
            return None
        
        # Verify lead_score == feirao_score
        lead_score = data.get("lead_score", 0)
        if lead_score != feirao_score:
            log_fail("POST /api/leads (HIGH-INTENT)", f"lead_score = {lead_score}, expected {feirao_score} (should equal feirao_score)")
            return None
        
        # Verify temperatura == "quente"
        temperatura = data.get("temperatura")
        if temperatura != "quente":
            log_fail("POST /api/leads (HIGH-INTENT)", f"temperatura = '{temperatura}', expected 'quente'")
            return None
        
        # Verify empreendimento_recomendado == "viva" (region jacaraipe + praia/duplex)
        emp_rec = data.get("empreendimento_recomendado")
        if emp_rec != "viva":
            log_warning("POST /api/leads (HIGH-INTENT)", f"empreendimento_recomendado = '{emp_rec}', expected 'viva' (region jacaraipe + praia/duplex)")
        
        # Verify empreendimento_alternativas is non-empty list
        emp_alts = data.get("empreendimento_alternativas", [])
        if not isinstance(emp_alts, list) or len(emp_alts) == 0:
            log_fail("POST /api/leads (HIGH-INTENT)", f"empreendimento_alternativas should be non-empty list, got: {emp_alts}")
            return None
        
        log_pass("POST /api/leads (HIGH-INTENT)", f"Lead created with id={lead_id}, score={feirao_score}, classe={classe}, emp={emp_rec}")
        return data
        
    except Exception as e:
        log_fail("POST /api/leads (HIGH-INTENT)", f"Exception: {str(e)}")
        return None

# ============================================================================
# TEST 3: POST /api/leads with LOW-INTENT payload (classe D)
# ============================================================================
def test_create_lead_low_intent():
    """Test lead creation with low-intent quiz payload"""
    print("\n" + "="*80)
    print("TEST 3: POST /api/leads with LOW-INTENT payload (expect classe D)")
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
# TEST 4: PATCH /api/leads/{id}/agendamento
# ============================================================================
def test_patch_agendamento(lead_id: str, original_score: int):
    """Test PATCH agendamento endpoint"""
    print("\n" + "="*80)
    print(f"TEST 4: PATCH /api/leads/{lead_id}/agendamento")
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
# TEST 5: POST /api/feirao/events
# ============================================================================
def test_feirao_events():
    """Test event tracking endpoint"""
    print("\n" + "="*80)
    print("TEST 5: POST /api/feirao/events")
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
# TEST 6: Admin login and endpoints
# ============================================================================
def test_admin_login():
    """Test admin login"""
    print("\n" + "="*80)
    print("TEST 6a: POST /api/admin/login")
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
    print("TEST 6b: GET /api/admin/feirao/overview")
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
    print("TEST 6c: GET /api/admin/feirao/funnel")
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
    print("TEST 6d: GET /api/admin/feirao/config")
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
    print("TEST 6e: PUT /api/admin/feirao/config")
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
# TEST 7: Regression - legacy admin endpoints
# ============================================================================
def test_admin_metrics(token: str):
    """Test legacy admin metrics endpoint"""
    print("\n" + "="*80)
    print("TEST 7a: GET /api/admin/metrics (regression)")
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
    print("TEST 7b: GET /api/admin/leads (regression)")
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
# MAIN TEST RUNNER
# ============================================================================
def main():
    """Run all tests"""
    print("\n" + "="*80)
    print("FEIRÃO DO IMÓVEL TORRES ENGENHARIA - BACKEND TEST SUITE")
    print("="*80)
    print(f"Base URL: {BASE_URL}")
    print(f"API Base: {API_BASE}")
    print(f"Admin: {ADMIN_EMAIL}")
    print("="*80)
    
    # Test 1: Public config
    test_feirao_config()
    
    # Test 2: High-intent lead
    high_intent_lead = test_create_lead_high_intent()
    
    # Test 3: Low-intent lead
    low_intent_lead = test_create_lead_low_intent()
    
    # Test 4: Patch agendamento (if high-intent lead was created)
    if high_intent_lead and "id" in high_intent_lead:
        test_patch_agendamento(high_intent_lead["id"], high_intent_lead.get("feirao_score", 0))
    else:
        log_fail("PATCH /api/leads/{id}/agendamento", "Skipped - high-intent lead not created")
    
    # Test 5: Event tracking
    test_feirao_events()
    
    # Test 6: Admin endpoints
    token = test_admin_login()
    if token:
        test_admin_overview(token)
        test_admin_funnel(token)
        test_admin_get_config(token)
        test_admin_put_config(token)
        
        # Test 7: Regression
        test_admin_metrics(token)
        test_admin_leads(token)
    else:
        log_fail("Admin endpoints", "Skipped - login failed")
    
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
