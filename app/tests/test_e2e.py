from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_extract_e2e() -> None:
    payload = b"Vendor: ACME Power\\nInvoice: INV-2026-001\\nTotal: 142.50\\nCurrency: EUR"
    response = client.post(
        "/api/extract",
        files={"file": ("invoice.txt", payload, "text/plain")},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["document_name"] == "invoice.txt"
    assert body["extracted_data"]["vendor_name"] == "ACME Power"
    assert body["extracted_data"]["invoice_number"] == "INV-2026-001"
    assert body["extracted_data"]["total_amount"] == 142.5
    assert body["extracted_data"]["currency"] == "EUR"
