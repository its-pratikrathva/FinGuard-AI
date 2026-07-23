"""POST /scan — message analysis endpoint ."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.scan_history import ScanHistory
from app.schemas.scan import ScanRequest, ScanResponse
from app.services.risk_score import RiskScoreService

router = APIRouter(
    prefix="/scan",
    tags=["Scan"],
)

service = RiskScoreService()


@router.post("", response_model=ScanResponse)
def scan_message(
    request: ScanRequest,
    db: Session = Depends(get_db),
):

    result = service.analyze(request.message)

    history = ScanHistory(
        message=request.message,
        language="English",
        risk_score=result["risk_score"],
        status=result["status"],
        keywords=result["keywords"],
        urls=result["urls"],
        reason=result["reason"],
        advice="Avoid clicking unknown links.",
    )

    db.add(history)
    db.commit()
    db.refresh(history)

    return ScanResponse(
        risk_score=result["risk_score"],
        status=result["status"],
        keywords=result["keywords"],
        urls=result["urls"],
        reason=result["reason"],
        advice="Avoid clicking unknown links.",
    )