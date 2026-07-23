from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.scan_history import ScanHistory
from app.schemas.history import HistoryListResponse

router = APIRouter(
    prefix="/history",
    tags=["History"],
)


@router.get("", response_model=HistoryListResponse)
def get_history(
    db: Session = Depends(get_db),
):
    scans = (
        db.query(ScanHistory)
        .order_by(ScanHistory.created_at.desc())
        .all()
    )

    return {
        "scans": scans
    }