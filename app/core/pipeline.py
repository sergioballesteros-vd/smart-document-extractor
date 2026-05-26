from app.domain.interfaces import LLMEngine, OCREngine
from app.schemas.extraction import ExtractionResponse, ExtractedInvoice


class ExtractionPipeline:
    def __init__(self, ocr_engine: OCREngine, llm_engine: LLMEngine):
        self.ocr_engine = ocr_engine
        self.llm_engine = llm_engine

    def run(self, content: bytes, filename: str) -> ExtractionResponse:
        raw_text = self.ocr_engine.extract_text(content=content, filename=filename)
        mapped = self.llm_engine.map_to_schema(raw_text=raw_text)

        return ExtractionResponse(
            document_name=filename,
            extracted_data=ExtractedInvoice(**mapped),
            confidence=0.91,
        )
