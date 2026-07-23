from datetime import datetime

from pydantic import BaseModel


class HistoryItem(BaseModel):

    id: int

    message: str

    language: str

    risk_score: float

    status: str

    created_at: datetime


class HistoryResponse(BaseModel):

    history: list[HistoryItem]