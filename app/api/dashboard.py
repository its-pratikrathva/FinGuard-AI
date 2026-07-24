from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.dependencies.auth import get_current_user
from app.models.scan_history import ScanHistory
from app.models.user import User
from app.schemas.dashboard import DashboardResponse

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get(
    "",
    response_model=DashboardResponse,
)
def dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    scans = (
        db.query(ScanHistory)
        .filter(ScanHistory.user_id == current_user.id)
        .all()
    )

    total = len(scans)

    safe = sum(1 for s in scans if s.status == "Safe")
    warning = sum(1 for s in scans if s.status == "Warning")
    dangerous = sum(1 for s in scans if s.status == "Dangerous")

    average = (
        sum(s.risk_score for s in scans) / total
        if total
        else 0
    )

    return DashboardResponse(
        total_scans=total,
        safe=safe,
        warning=warning,
        dangerous=dangerous,
        average_risk=round(average, 2),
    )