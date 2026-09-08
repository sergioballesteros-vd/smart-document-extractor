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
    @staticmethod
    def _extract(pattern: str, normalized_text: str, default, transform=str.strip):
        match = re.search(pattern, normalized_text, re.IGNORECASE | re.MULTILINE)
        return transform(match.group(1)) if match else default

    def map_to_schema(self, raw_text: str) -> dict:
        normalized_text = raw_text.replace("\\n", "\n")

        return {
            "vendor_name": self._extract(r"^vendor\s*[:=]\s*([^\n\r]+)", normalized_text, "UNKNOWN"),
            "invoice_number": self._extract(
                r"^invoice\s*(?:number|id)?\s*[:=]\s*([^\n\r]+)", normalized_text, "UNKNOWN"
            ),
            "total_amount": self._extract(
                r"^total\s*[:=]\s*([0-9]+(?:\.[0-9]{1,2})?)", normalized_text, 0, float
            ),
            "currency": self._extract(
                r"^currency\s*[:=]\s*([A-Za-z]{3})", normalized_text, "EUR", str.upper
            ),
        }
