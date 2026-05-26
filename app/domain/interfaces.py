from typing import Protocol


class OCREngine(Protocol):
    def extract_text(self, content: bytes, filename: str) -> str:
        ...


class LLMEngine(Protocol):
    def map_to_schema(self, raw_text: str) -> dict:
        ...
