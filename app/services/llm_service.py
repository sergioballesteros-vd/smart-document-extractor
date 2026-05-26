import re


class HeuristicLLMEngine:
    """Deterministic LLM-like mapper for local/offline demo."""

    def map_to_schema(self, raw_text: str) -> dict:
        normalized_text = raw_text.replace("\\n", "\n")

        vendor_match = re.search(r"^vendor\s*[:=]\s*([^\n\r]+)", normalized_text, re.IGNORECASE | re.MULTILINE)
        invoice_match = re.search(
            r"^invoice\s*(?:number|id)?\s*[:=]\s*([^\n\r]+)",
            normalized_text,
            re.IGNORECASE | re.MULTILINE,
        )
        amount_match = re.search(
            r"^total\s*[:=]\s*([0-9]+(?:\.[0-9]{1,2})?)",
            normalized_text,
            re.IGNORECASE | re.MULTILINE,
        )
        currency_match = re.search(r"^currency\s*[:=]\s*([A-Za-z]{3})", normalized_text, re.IGNORECASE | re.MULTILINE)

        return {
            "vendor_name": vendor_match.group(1).strip() if vendor_match else "UNKNOWN",
            "invoice_number": invoice_match.group(1).strip() if invoice_match else "UNKNOWN",
            "total_amount": float(amount_match.group(1)) if amount_match else 0,
            "currency": currency_match.group(1).upper() if currency_match else "EUR",
        }
