class BasicOCREngine:
    """Fallback OCR engine for portfolio demo.

    Reads text directly when possible; this keeps the E2E flow deterministic
    without requiring native OCR binaries in local demos.
    """

    def extract_text(self, content: bytes, filename: str) -> str:
        try:
            decoded = content.decode("utf-8", errors="ignore").strip()
            if decoded:
                return decoded
        except Exception:
            pass

        return f"UNREADABLE_CONTENT filename={filename} bytes={len(content)}"
