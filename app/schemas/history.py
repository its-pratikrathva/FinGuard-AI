from datetime import datetime

from pydantic import BaseModel


class HistoryItem(BaseModel):
    
    id: int
    
    message: str
    
    language: str
    
    risk_score: float
    
    status: str
    keywords: list[str]
    urls: list[str]
    reason: str
    advice: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }

class HistoryListResponse(BaseModel):
    scans: list[HistoryItem]