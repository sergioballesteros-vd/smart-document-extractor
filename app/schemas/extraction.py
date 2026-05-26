from pydantic import BaseModel, Field


class ExtractedInvoice(BaseModel):
    vendor_name: str = Field(default="UNKNOWN")
    invoice_number: str = Field(default="UNKNOWN")
    total_amount: float = Field(default=0)
    currency: str = Field(default="EUR")


class ExtractionResponse(BaseModel):
    document_name: str
    extracted_data: ExtractedInvoice
    confidence: float
