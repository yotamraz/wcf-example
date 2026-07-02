"""
Functional tests for the WCF WSDL metadata endpoint.
Verifies GET http://localhost:8080/CalculatorService?wsdl returns 200 with valid WSDL.
Classification: origin_and_target (WSDL endpoint existed on Baseline Ref).
"""
import requests
import pytest

SERVICE_PORT = 8080
BASE_URL = f"http://localhost:{SERVICE_PORT}"
WSDL_URL = f"{BASE_URL}/CalculatorService?wsdl"


@pytest.fixture(autouse=True)
def health_check():
    """Confirm the WSDL endpoint is reachable before running tests."""
    try:
        resp = requests.get(WSDL_URL, timeout=10)
        assert resp.status_code == 200, (
            f"Health check failed: WSDL endpoint returned {resp.status_code}"
        )
    except requests.exceptions.ConnectionError as e:
        pytest.fail(f"Cannot connect to WCF service at {WSDL_URL}: {e}")


class TestWsdlEndpoint:
    """GET /CalculatorService?wsdl — WSDL metadata endpoint."""

    def test_wsdl_returns_200(self):
        """WSDL endpoint should return HTTP 200."""
        resp = requests.get(WSDL_URL, timeout=10)
        assert resp.status_code == 200

    def test_wsdl_contains_definitions(self):
        """Response body should contain wsdl:definitions."""
        resp = requests.get(WSDL_URL, timeout=10)
        assert resp.status_code == 200
        assert "wsdl:definitions" in resp.text, (
            f"Response does not contain 'wsdl:definitions'.\n"
            f"First 500 chars: {resp.text[:500]}"
        )

    def test_wsdl_contains_calculator_service(self):
        """WSDL should reference the CalculatorService."""
        resp = requests.get(WSDL_URL, timeout=10)
        assert resp.status_code == 200
        body = resp.text
        assert "CalculatorService" in body, (
            f"WSDL does not mention 'CalculatorService'.\nFirst 500 chars: {body[:500]}"
        )

    def test_wsdl_mentions_add_and_subtract_operations(self):
        """WSDL should define Add and Subtract operations."""
        resp = requests.get(WSDL_URL, timeout=10)
        assert resp.status_code == 200
        body = resp.text
        assert "Add" in body, "WSDL does not define the Add operation."
        assert "Subtract" in body, "WSDL does not define the Subtract operation."

    def test_base_endpoint_returns_valid_response(self):
        """GET on the base endpoint (without ?wsdl) should return some response from WCF."""
        resp = requests.get(f"{BASE_URL}/CalculatorService", timeout=10)
        # CoreWCF may return 400 or 200 for plain GET on SOAP endpoint
        assert resp.status_code in (200, 400, 405), (
            f"Unexpected status {resp.status_code} from base SOAP endpoint."
        )
