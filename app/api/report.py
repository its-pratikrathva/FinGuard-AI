from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from io import BytesIO

from app.database.session import get_db
from app.models.scan_history import ScanHistory
from app.services.report_service import ReportService

router = APIRouter(
    prefix="/report",
    tags=["Report"],
)

service = ReportService()


@router.get("/{scan_id}")
def download_report(
    scan_id: int,
    db: Session = Depends(get_db),
):
    scan = (
        db.query(ScanHistory)
        .filter(ScanHistory.id == scan_id)
        .first()
    )

    if not scan:
        raise HTTPException(
            status_code=404,
            detail="Scan not found",
        )

    pdf = service.generate_pdf(scan)

    return StreamingResponse(
        BytesIO(pdf),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=report_{scan_id}.pdf"
        },
    )