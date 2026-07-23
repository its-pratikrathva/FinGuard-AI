from pydantic import BaseModel, Field


class ScanRequest(BaseModel):

    message: str = Field(
        ...,
        min_length=1,
        max_length=5000,
        description="SMS / Email / WhatsApp message"
    )


class ScanResponse(BaseModel):

    language: str

    risk_score: float = Field(
        ge=0,
        le=100
    )

    status: str

    keywords: list[str]

    urls: list[str]

    reason: str

    advice: str