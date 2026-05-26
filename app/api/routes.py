import os

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.core.pipeline import ExtractionPipeline
from app.schemas.extraction import ExtractionResponse
from app.services.llm_service import HeuristicLLMEngine, OpenAILLMEngine
from app.services.ocr_service import BasicOCREngine, TesseractOCREngine

router = APIRouter(prefix="/api", tags=["extractor"])

ocr_engine = TesseractOCREngine() if os.getenv("USE_TESSERACT", "false").lower() == "true" else BasicOCREngine()
llm_engine = OpenAILLMEngine() if os.getenv("OPENAI_API_KEY") else HeuristicLLMEngine()
pipeline = ExtractionPipeline(ocr_engine=ocr_engine, llm_engine=llm_engine)


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@router.post("/extract", response_model=ExtractionResponse)
async def extract_document(file: UploadFile = File(...)) -> ExtractionResponse:
    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename is required")

    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Uploaded file is empty")

    return pipeline.run(content=content, filename=file.filename)
