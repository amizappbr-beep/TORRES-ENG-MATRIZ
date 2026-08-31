#!/usr/bin/env python3
"""Backend API tests for Feirão Torres - Meta CPL Integration with VALID Token

Tests the Meta CPL integration with a VALID access token.
The token should now be working and return real campaign data.
"""

import requests
import json
from typing import Dict, Any, List

# Base URL from frontend/.env
BASE_URL = "https://torres-pre-quali.preview.emergentagent.com"
API_BASE = f"{BASE_URL}/api"

# Admin credentials from test_credentials.md
ADMIN_EMAIL = "admin@feiraotorres.com.br"
ADMIN_PASSWORD = "Feirao@Torres2026"

# Expected campaign IDs (from backend/.env META_CAMPAIGN_IDS)
EXPECTED_CAMPAIGN_IDS = ["120253922856330231", "120254029527980231"]


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


def test_meta_cpl_valid_token(token: str, days: int) -> Dict[str, Any]:
    """
    Test GET /api/admin/feirao/meta-cpl with VALID token
    
    Expected:
    - HTTP 200
    - configured == true
    - NO "error" or "error_type" field (token is valid)
    - total_spend is a number (float) > 0
    - "campanhas" is a list containing ONLY the two Feirão campaign IDs
    - Each campaign has campaign_name and spend (number)
    - crm_leads is an integer
    - cpl_crm is either a number or null (null acceptable when crm_leads == 0)
    """
    print_test_header(f"1.{days}", f"Meta CPL endpoint with VALID token (days={days})")
    
    url = f"{API_BASE}/admin/feirao/meta-cpl?days={days}"
    headers = {"Authorization": f"Bearer {token}"}
    
    print(f"\nGET {url}")
    print(f"Headers: Authorization: Bearer {token[:20]}...")
    
    response = requests.get(url, headers=headers)
    print(f"\nStatus Code: {response.status_code}")
    
    # Check 1: Must return 200
    if response.status_code != 200:
        print_result(False, f"Expected status 200, got {response.status_code}")
        print(f"Response: {response.text}")
        return {"passed": False, "response": None, "total_spend": None, "campaign_ids": []}
    
    print_result(True, "Status code is 200")
    
    try:
        data = response.json()
        print(f"\nResponse JSON:")
        print(json.dumps(data, indent=2, ensure_ascii=False))
    except Exception as e:
        print_result(False, f"Failed to parse JSON response: {e}")
        return {"passed": False, "response": None, "total_spend": None, "campaign_ids": []}
    
    # Check 2: configured must be true
    configured = data.get("configured")
    if configured != True:
        print_result(False, f"Expected configured=true, got {configured}")
        return {"passed": False, "response": data, "total_spend": None, "campaign_ids": []}
    print_result(True, "configured == true")
    
    # Check 3: NO "error" or "error_type" field (token is valid)
    if "error" in data:
        print_result(False, f"Unexpected 'error' field present: {data.get('error')[:100]}")
        return {"passed": False, "response": data, "total_spend": None, "campaign_ids": []}
    print_result(True, "NO 'error' field (token is valid)")
    
    if "error_type" in data:
        print_result(False, f"Unexpected 'error_type' field present: {data.get('error_type')}")
        return {"passed": False, "response": data, "total_spend": None, "campaign_ids": []}
    print_result(True, "NO 'error_type' field (token is valid)")
    
    # Check 4: total_spend must be a number > 0
    total_spend = data.get("total_spend")
    if not isinstance(total_spend, (int, float)):
        print_result(False, f"total_spend is not a number: {type(total_spend)} = {total_spend}")
        return {"passed": False, "response": data, "total_spend": total_spend, "campaign_ids": []}
    print_result(True, f"total_spend is a number: {total_spend}")
    
    if total_spend <= 0:
        print_result(False, f"total_spend should be > 0, got {total_spend}")
        return {"passed": False, "response": data, "total_spend": total_spend, "campaign_ids": []}
    print_result(True, f"total_spend > 0: {total_spend}")
    
    # Check 5: campanhas must be a list
    campanhas = data.get("campanhas")
    if not isinstance(campanhas, list):
        print_result(False, f"campanhas is not a list: {type(campanhas)}")
        return {"passed": False, "response": data, "total_spend": total_spend, "campaign_ids": []}
    print_result(True, f"campanhas is a list with {len(campanhas)} items")
    
    # Check 6: Extract campaign IDs and verify they match expected IDs
    campaign_ids = [c.get("campaign_id") for c in campanhas if isinstance(c, dict)]
    print(f"\nCampaign IDs found: {campaign_ids}")
    print(f"Expected IDs: {EXPECTED_CAMPAIGN_IDS}")
    
    # Check that ONLY the expected campaign IDs are present
    unexpected_ids = [cid for cid in campaign_ids if cid not in EXPECTED_CAMPAIGN_IDS]
    if unexpected_ids:
        print_result(False, f"Unexpected campaign IDs found: {unexpected_ids}")
        return {"passed": False, "response": data, "total_spend": total_spend, "campaign_ids": campaign_ids}
    print_result(True, "NO unexpected campaign IDs")
    
    # Check that all expected IDs are present
    missing_ids = [cid for cid in EXPECTED_CAMPAIGN_IDS if cid not in campaign_ids]
    if missing_ids:
        print_result(False, f"Missing expected campaign IDs: {missing_ids}")
        return {"passed": False, "response": data, "total_spend": total_spend, "campaign_ids": campaign_ids}
    print_result(True, f"All expected campaign IDs present: {EXPECTED_CAMPAIGN_IDS}")
    
    # Check 7: Each campaign must have campaign_name and spend
    for i, campaign in enumerate(campanhas):
        if not isinstance(campaign, dict):
            print_result(False, f"Campaign {i} is not a dict: {type(campaign)}")
            return {"passed": False, "response": data, "total_spend": total_spend, "campaign_ids": campaign_ids}
        
        campaign_name = campaign.get("campaign_name")
        if not campaign_name:
            print_result(False, f"Campaign {i} missing campaign_name")
            return {"passed": False, "response": data, "total_spend": total_spend, "campaign_ids": campaign_ids}
        
        spend = campaign.get("spend")
        if not isinstance(spend, (int, float)):
            print_result(False, f"Campaign {i} spend is not a number: {type(spend)} = {spend}")
            return {"passed": False, "response": data, "total_spend": total_spend, "campaign_ids": campaign_ids}
        
        print(f"  Campaign {i}: {campaign_name} - spend: {spend}")
    
    print_result(True, "All campaigns have campaign_name and spend (number)")
    
    # Check 8: crm_leads must be an integer
    crm_leads = data.get("crm_leads")
    if not isinstance(crm_leads, int):
        print_result(False, f"crm_leads is not an integer: {type(crm_leads)} = {crm_leads}")
        return {"passed": False, "response": data, "total_spend": total_spend, "campaign_ids": campaign_ids}
    print_result(True, f"crm_leads is an integer: {crm_leads}")
    
    # Check 9: cpl_crm must be either a number or null
    cpl_crm = data.get("cpl_crm")
    if cpl_crm is not None and not isinstance(cpl_crm, (int, float)):
        print_result(False, f"cpl_crm is not a number or null: {type(cpl_crm)} = {cpl_crm}")
        return {"passed": False, "response": data, "total_spend": total_spend, "campaign_ids": campaign_ids}
    
    if cpl_crm is None:
        print_result(True, f"cpl_crm is null (acceptable when crm_leads == 0)")
    else:
        print_result(True, f"cpl_crm is a number: {cpl_crm}")
    
    print(f"\n✅ TEST 1.{days} PASSED: Meta CPL endpoint works with VALID token (days={days})")
    return {"passed": True, "response": data, "total_spend": total_spend, "campaign_ids": campaign_ids}


def test_analytics_regression(token: str) -> bool:
    """
    TEST 2: GET /api/admin/feirao/analytics?days=30
    
    Expected:
    - HTTP 200
    - Response has keys: kpis, series, funnel, origem, por_empreendimento
    """
    print_test_header(2, "Regression: Analytics endpoint still works")
    
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


def main():
    """Run all tests"""
    print("="*80)
    print("FEIRÃO TORRES - META CPL INTEGRATION WITH VALID TOKEN TESTS")
    print("="*80)
    print(f"\nBase URL: {BASE_URL}")
    print(f"API Base: {API_BASE}")
    print(f"Admin: {ADMIN_EMAIL}")
    print(f"Expected Campaign IDs: {EXPECTED_CAMPAIGN_IDS}")
    
    results = {
        "test1_meta_cpl_days_30": False,
        "test1_meta_cpl_days_7": False,
        "test1_meta_cpl_days_90": False,
        "test2_analytics_regression": False,
    }
    
    meta_cpl_responses = {}
    total_spends = {}
    campaign_ids_by_days = {}
    
    try:
        # Get admin token
        token = get_admin_token()
        
        # TEST 1: Meta CPL with VALID token - days=30
        test1_30_result = test_meta_cpl_valid_token(token, days=30)
        results["test1_meta_cpl_days_30"] = test1_30_result["passed"]
        meta_cpl_responses[30] = test1_30_result["response"]
        total_spends[30] = test1_30_result["total_spend"]
        campaign_ids_by_days[30] = test1_30_result["campaign_ids"]
        
        # TEST 1: Meta CPL with VALID token - days=7
        test1_7_result = test_meta_cpl_valid_token(token, days=7)
        results["test1_meta_cpl_days_7"] = test1_7_result["passed"]
        meta_cpl_responses[7] = test1_7_result["response"]
        total_spends[7] = test1_7_result["total_spend"]
        campaign_ids_by_days[7] = test1_7_result["campaign_ids"]
        
        # TEST 1: Meta CPL with VALID token - days=90
        test1_90_result = test_meta_cpl_valid_token(token, days=90)
        results["test1_meta_cpl_days_90"] = test1_90_result["passed"]
        meta_cpl_responses[90] = test1_90_result["response"]
        total_spends[90] = test1_90_result["total_spend"]
        campaign_ids_by_days[90] = test1_90_result["campaign_ids"]
        
        # TEST 2: Analytics regression
        results["test2_analytics_regression"] = test_analytics_regression(token)
        
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
    
    # Print key findings
    print(f"\n📊 KEY FINDINGS:")
    for days in [7, 30, 90]:
        if total_spends.get(days) is not None:
            print(f"  - days={days}: total_spend = {total_spends[days]}, campaign_ids = {campaign_ids_by_days[days]}")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED - Meta CPL integration is working correctly with VALID token!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    exit(main())
