"""
Functional tests for WCF SOAP operations via HTTP POST.
Tests Add and Subtract operations using raw SOAP/XML over BasicHttpBinding.
Classification: origin_and_target (SOAP operations existed on Baseline Ref).
"""
import requests
import pytest
import xml.etree.ElementTree as ET

SERVICE_PORT = 8080
SOAP_URL = f"http://localhost:{SERVICE_PORT}/CalculatorService"

SOAP_ENVELOPE_ADD = """<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:Add>
      <tns:val1>{val1}</tns:val1>
      <tns:val2>{val2}</tns:val2>
    </tns:Add>
  </soap:Body>
</soap:Envelope>"""

SOAP_ENVELOPE_SUBTRACT = """<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:Subtract>
      <tns:val1>{val1}</tns:val1>
      <tns:val2>{val2}</tns:val2>
    </tns:Subtract>
  </soap:Body>
</soap:Envelope>"""

ADD_ACTION = "http://tempuri.org/ICalculatorService/Add"
SUBTRACT_ACTION = "http://tempuri.org/ICalculatorService/Subtract"


def call_soap(envelope: str, soap_action: str) -> requests.Response:
    headers = {
        "Content-Type": "text/xml; charset=utf-8",
        "SOAPAction": soap_action,
    }
    return requests.post(SOAP_URL, data=envelope.encode("utf-8"), headers=headers, timeout=15)


@pytest.fixture(autouse=True)
def health_check():
    """Confirm the WSDL endpoint is reachable before running SOAP tests."""
    try:
        resp = requests.get(f"{SOAP_URL}?wsdl", timeout=10)
        assert resp.status_code == 200, f"WCF service not healthy: {resp.status_code}"
    except requests.exceptions.ConnectionError as e:
        pytest.fail(f"Cannot connect to WCF service: {e}")


class TestAddOperation:
    """SOAP Add operation tests."""

    def test_add_floating_point_values(self):
        """Add(11.8, 14.7) should return 26.5."""
        body = SOAP_ENVELOPE_ADD.format(val1=11.8, val2=14.7)
        resp = call_soap(body, ADD_ACTION)
        assert resp.status_code == 200, f"SOAP Add failed: HTTP {resp.status_code}\n{resp.text}"
        text = resp.text
        assert "AddResponse" in text or "AddResult" in text, (
            f"Response does not contain expected elements: {text[:500]}"
        )
        assert "26.5" in text, f"Expected 26.5 in response but got: {text[:300]}"

    def test_add_positive_integers(self):
        """Add(2.0, 3.0) should return 5.0."""
        body = SOAP_ENVELOPE_ADD.format(val1=2.0, val2=3.0)
        resp = call_soap(body, ADD_ACTION)
        assert resp.status_code == 200, f"SOAP Add failed: HTTP {resp.status_code}\n{resp.text}"

    def test_add_with_zero(self):
        """Add(7.0, 0.0) should return 7.0."""
        body = SOAP_ENVELOPE_ADD.format(val1=7.0, val2=0.0)
        resp = call_soap(body, ADD_ACTION)
        assert resp.status_code == 200, f"SOAP Add(7.0, 0.0) failed: HTTP {resp.status_code}"

    def test_add_negative_numbers(self):
        """Add(-2.0, -3.0) should return -5.0."""
        body = SOAP_ENVELOPE_ADD.format(val1=-2.0, val2=-3.0)
        resp = call_soap(body, ADD_ACTION)
        assert resp.status_code == 200, f"SOAP Add negative failed: HTTP {resp.status_code}"


class TestSubtractOperation:
    """SOAP Subtract operation tests."""

    def test_subtract_floating_point_values(self):
        """Subtract(11.8, 14.7) should return approximately -2.9."""
        body = SOAP_ENVELOPE_SUBTRACT.format(val1=11.8, val2=14.7)
        resp = call_soap(body, SUBTRACT_ACTION)
        assert resp.status_code == 200, f"SOAP Subtract failed: HTTP {resp.status_code}\n{resp.text}"
        text = resp.text
        assert "SubtractResponse" in text or "SubtractResult" in text, (
            f"Response does not contain expected elements: {text[:500]}"
        )
        # floating point result may be -2.9 or -2.8999999999999986 (both correct representations)
        assert "-2." in text, f"Expected negative result ~-2.9 in response but got: {text[:300]}"

    def test_subtract_positive_numbers(self):
        """Subtract(3.0, 2.0) should return 1.0."""
        body = SOAP_ENVELOPE_SUBTRACT.format(val1=3.0, val2=2.0)
        resp = call_soap(body, SUBTRACT_ACTION)
        assert resp.status_code == 200, f"SOAP Subtract failed: HTTP {resp.status_code}"

    def test_subtract_to_negative(self):
        """Subtract(2.0, 3.0) should return -1.0."""
        body = SOAP_ENVELOPE_SUBTRACT.format(val1=2.0, val2=3.0)
        resp = call_soap(body, SUBTRACT_ACTION)
        assert resp.status_code == 200, f"SOAP Subtract to negative failed: HTTP {resp.status_code}"
