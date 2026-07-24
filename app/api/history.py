from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.dependencies.auth import get_current_user
from app.models.scan_history import ScanHistory
from app.models.user import User
from app.schemas.history import HistoryListResponse

router = APIRouter(
    prefix="/history",
    tags=["History"],
)


@router.get("", response_model=HistoryListResponse)
def get_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    scans = (
        db.query(ScanHistory)
        .filter(ScanHistory.user_id == current_user.id)
        .order_by(ScanHistory.created_at.desc())
        .all()
    )

    return {
        "scans": scans
    }