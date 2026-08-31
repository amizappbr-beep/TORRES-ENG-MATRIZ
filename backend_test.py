#!/usr/bin/env python3
"""Backend API tests for Feirão Torres - Meta Token Expiration Handling

Tests the graceful handling of an EXPIRED Meta access token.
The stored token is currently expired (OAuthException code 190).
"""

import requests
import json
from typing import Dict, Any

# Base URL from frontend/.env
BASE_URL = "https://torres-pre-quali.preview.emergentagent.com"
API_BASE = f"{BASE_URL}/api"

# Admin credentials from test_credentials.md
ADMIN_EMAIL = "admin@feiraotorres.com.br"
ADMIN_PASSWORD = "Feirao@Torres2026"


def print_test_header(test_num: int, description: str):
    """Print formatted test header"""
    print(f"\n{'='*80}")
    print(f"TEST {test_num}: {description}")
    print(f"{'='*80}")


def print_result(passed: bool, message: str):
    """Print test result"""
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"{status}: {message}")


def get_admin_token() -> str:
    """Login as admin and return JWT token"""
    url = f"{API_BASE}/admin/login"
    payload = {"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD}
    
    print(f"\n🔐 Logging in as admin...")
    print(f"POST {url}")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    response = requests.post(url, json=payload)
    print(f"Status: {response.status_code}")
    
    if response.status_code != 200:
        print(f"❌ Login failed: {response.text}")
        raise Exception(f"Admin login failed with status {response.status_code}")
    
    data = response.json()
    token = data.get("access_token")
    print(f"✅ Login successful, token obtained")
    return token


def test_meta_cpl_expired_token(token: str) -> Dict[str, Any]:
    """
    TEST 1: GET /api/admin/feirao/meta-cpl?days=30 with expired token
    
    Expected:
    - HTTP 200 (NOT 500)
    - configured == true
    - error_type == "token_expired"
    - mensagem field with friendly message (contains "expirou" or "token")
    - error field with raw error for debugging
    """
    print_test_header(1, "Meta CPL endpoint with EXPIRED token")
    
    url = f"{API_BASE}/admin/feirao/meta-cpl?days=30"
    headers = {"Authorization": f"Bearer {token}"}
    
    print(f"\nGET {url}")
    print(f"Headers: Authorization: Bearer {token[:20]}...")
    
    response = requests.get(url, headers=headers)
    print(f"\nStatus Code: {response.status_code}")
    
    # Check 1: Must return 200, not 500
    if response.status_code != 200:
        print_result(False, f"Expected status 200, got {response.status_code}")
        print(f"Response: {response.text}")
        return {"passed": False, "response": None}
    
    print_result(True, "Status code is 200 (not 500)")
    
    try:
        data = response.json()
        print(f"\nResponse JSON:")
        print(json.dumps(data, indent=2, ensure_ascii=False))
    except Exception as e:
        print_result(False, f"Failed to parse JSON response: {e}")
        return {"passed": False, "response": None}
    
    # Check 2: configured must be true
    configured = data.get("configured")
    if configured != True:
        print_result(False, f"Expected configured=true, got {configured}")
        return {"passed": False, "response": data}
    print_result(True, "configured == true")
    
    # Check 3: error_type must be "token_expired"
    error_type = data.get("error_type")
    if error_type != "token_expired":
        print_result(False, f"Expected error_type='token_expired', got '{error_type}'")
        return {"passed": False, "response": data}
    print_result(True, "error_type == 'token_expired'")
    
    # Check 4: mensagem field must exist and mention token/expiration
    mensagem = data.get("mensagem", "")
    if not mensagem:
        print_result(False, "mensagem field is missing or empty")
        return {"passed": False, "response": data}
    
    mensagem_lower = mensagem.lower()
    has_token_mention = "token" in mensagem_lower or "expirou" in mensagem_lower
    if not has_token_mention:
        print_result(False, f"mensagem doesn't mention token/expiration: '{mensagem}'")
        return {"passed": False, "response": data}
    print_result(True, f"mensagem is user-friendly and mentions token: '{mensagem}'")
    
    # Check 5: error field must exist for debugging
    error = data.get("error")
    if not error:
        print_result(False, "error field is missing (needed for debugging)")
        return {"passed": False, "response": data}
    print_result(True, f"error field present for debugging (length: {len(error)} chars)")
    
    print(f"\n✅ TEST 1 PASSED: Meta CPL endpoint handles expired token gracefully")
    return {"passed": True, "response": data}


def test_meta_cpl_auth_required() -> bool:
    """
    TEST 2: GET /api/admin/feirao/meta-cpl WITHOUT Bearer token
    
    Expected:
    - HTTP 401 or 403 (not 500)
    """
    print_test_header(2, "Meta CPL endpoint requires authentication")
    
    url = f"{API_BASE}/admin/feirao/meta-cpl?days=30"
    
    print(f"\nGET {url}")
    print(f"Headers: (no Authorization header)")
    
    response = requests.get(url)
    print(f"\nStatus Code: {response.status_code}")
    print(f"Response: {response.text[:200]}")
    
    if response.status_code in [401, 403]:
        print_result(True, f"Auth required: returns {response.status_code}")
        return True
    else:
        print_result(False, f"Expected 401 or 403, got {response.status_code}")
        return False


def test_analytics_regression(token: str) -> bool:
    """
    TEST 3: GET /api/admin/feirao/analytics?days=30
    
    Expected:
    - HTTP 200
    - Response has keys: kpis, series, funnel, origem, por_empreendimento
    """
    print_test_header(3, "Regression: Analytics endpoint still works")
    
    url = f"{API_BASE}/admin/feirao/analytics?days=30"
    headers = {"Authorization": f"Bearer {token}"}
    
    print(f"\nGET {url}")
    print(f"Headers: Authorization: Bearer {token[:20]}...")
    
    response = requests.get(url, headers=headers)
    print(f"\nStatus Code: {response.status_code}")
    
    if response.status_code != 200:
        print_result(False, f"Expected status 200, got {response.status_code}")
        print(f"Response: {response.text}")
        return False
    
    print_result(True, "Status code is 200")
    
    try:
        data = response.json()
        required_keys = ["kpis", "series", "funnel", "origem", "por_empreendimento"]
        missing_keys = [k for k in required_keys if k not in data]
        
        if missing_keys:
            print_result(False, f"Missing keys: {missing_keys}")
            return False
        
        print_result(True, f"All required keys present: {required_keys}")
        print(f"\nSample data:")
        print(f"  - kpis.total: {data['kpis'].get('total')}")
        print(f"  - series length: {len(data['series'])}")
        print(f"  - funnel.visitantes: {data['funnel'].get('visitantes')}")
        return True
        
    except Exception as e:
        print_result(False, f"Failed to parse response: {e}")
        return False


def test_overview_funnel_regression(token: str) -> bool:
    """
    TEST 4: GET /api/admin/feirao/overview and /funnel
    
    Expected:
    - Both return HTTP 200
    """
    print_test_header(4, "Regression: Overview and Funnel endpoints still work")
    
    # Test overview
    url_overview = f"{API_BASE}/admin/feirao/overview"
    headers = {"Authorization": f"Bearer {token}"}
    
    print(f"\nGET {url_overview}")
    response_overview = requests.get(url_overview, headers=headers)
    print(f"Status Code: {response_overview.status_code}")
    
    overview_ok = response_overview.status_code == 200
    if overview_ok:
        print_result(True, "Overview endpoint returns 200")
        data = response_overview.json()
        print(f"  - total: {data.get('total')}")
        print(f"  - hoje: {data.get('hoje')}")
    else:
        print_result(False, f"Overview endpoint failed: {response_overview.status_code}")
    
    # Test funnel
    url_funnel = f"{API_BASE}/admin/feirao/funnel"
    
    print(f"\nGET {url_funnel}")
    response_funnel = requests.get(url_funnel, headers=headers)
    print(f"Status Code: {response_funnel.status_code}")
    
    funnel_ok = response_funnel.status_code == 200
    if funnel_ok:
        print_result(True, "Funnel endpoint returns 200")
        data = response_funnel.json()
        print(f"  - funil.visitantes: {data.get('funil', {}).get('visitantes')}")
    else:
        print_result(False, f"Funnel endpoint failed: {response_funnel.status_code}")
    
    return overview_ok and funnel_ok


def main():
    """Run all tests"""
    print("="*80)
    print("FEIRÃO TORRES - META TOKEN EXPIRATION HANDLING TESTS")
    print("="*80)
    print(f"\nBase URL: {BASE_URL}")
    print(f"API Base: {API_BASE}")
    print(f"Admin: {ADMIN_EMAIL}")
    
    results = {
        "test1_meta_cpl_expired": False,
        "test2_auth_required": False,
        "test3_analytics_regression": False,
        "test4_overview_funnel_regression": False,
    }
    
    meta_cpl_response = None
    
    try:
        # Get admin token
        token = get_admin_token()
        
        # TEST 1: Meta CPL with expired token
        test1_result = test_meta_cpl_expired_token(token)
        results["test1_meta_cpl_expired"] = test1_result["passed"]
        meta_cpl_response = test1_result["response"]
        
        # TEST 2: Auth required
        results["test2_auth_required"] = test_meta_cpl_auth_required()
        
        # TEST 3: Analytics regression
        results["test3_analytics_regression"] = test_analytics_regression(token)
        
        # TEST 4: Overview/Funnel regression
        results["test4_overview_funnel_regression"] = test_overview_funnel_regression(token)
        
    except Exception as e:
        print(f"\n❌ FATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
    
    # Final summary
    print("\n" + "="*80)
    print("FINAL SUMMARY")
    print("="*80)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, passed_flag in results.items():
        status = "✅ PASS" if passed_flag else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\n{'='*80}")
    print(f"TOTAL: {passed}/{total} tests passed")
    print(f"{'='*80}")
    
    if meta_cpl_response:
        print(f"\n📋 META CPL ENDPOINT RESPONSE (for review):")
        print(json.dumps(meta_cpl_response, indent=2, ensure_ascii=False))
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED - Meta token expiration handling is working correctly!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    exit(main())
