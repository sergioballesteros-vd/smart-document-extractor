from __future__ import annotations

import json
import os
import re

from openai import OpenAI


class OpenAILLMEngine:
    def __init__(self) -> None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY is required for OpenAILLMEngine")

        self.client = OpenAI(api_key=api_key)
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o")

    def map_to_schema(self, raw_text: str) -> dict:
        prompt = (
            "Extract invoice fields from this OCR text. "
            "Return strict JSON with keys vendor_name, invoice_number, total_amount, currency. "
            "No extra keys.\n\n"
            f"OCR_TEXT:\n{raw_text}"
        )

        completion = self.client.chat.completions.create(
            model=self.model,
            temperature=0,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": "You are an invoice extraction engine."},
                {"role": "user", "content": prompt},
            ],
        )

        return json.loads(completion.choices[0].message.content or "{}")


class HeuristicLLMEngine:
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
