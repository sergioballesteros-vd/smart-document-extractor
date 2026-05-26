from __future__ import annotations

import io
from pathlib import Path

import pytesseract
from pdf2image import convert_from_bytes
from PIL import Image


class TesseractOCREngine:
    def extract_text(self, content: bytes, filename: str) -> str:
        extension = Path(filename).suffix.lower()

        if extension == ".pdf":
            pages = convert_from_bytes(content)
            page_texts = [pytesseract.image_to_string(page) for page in pages]
            return "\n".join(page_texts).strip()

        image = Image.open(io.BytesIO(content))
        return pytesseract.image_to_string(image).strip()


class BasicOCREngine:
    def extract_text(self, content: bytes, filename: str) -> str:
        try:
            decoded = content.decode("utf-8", errors="ignore").strip()
            if decoded:
                return decoded
        except Exception:
            pass

        return f"UNREADABLE_CONTENT filename={filename} bytes={len(content)}"
