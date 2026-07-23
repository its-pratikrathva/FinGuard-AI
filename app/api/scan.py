"""POST /scan — message analysis endpoint."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.scan_history import ScanHistory
from app.schemas.scan import ScanRequest, ScanResponse

from app.services.keyword_detector import detect_keywords
from app.services.url_extractor import extract_urls
from app.services.ai_detector import AIDetector
from app.services.gemini_service import analyze_message

router = APIRouter(
    prefix="/scan",
    tags=["Scan"],
)

ai_detector = AIDetector()


@router.post("", response_model=ScanResponse)
def scan_message(
    request: ScanRequest,
    db: Session = Depends(get_db),
):
    # Extract keywords
    keywords = detect_keywords(request.message)

    # Extract URLs
    urls = extract_urls(request.message)

    # Calculate score
    risk_score, status = ai_detector.analyze(
        keyword_count=len(keywords),
        suspicious_urls=len(urls),
    )

    # Gemini analysis
    # reason = analyze_message(request.message)

    # advice = "Avoid clicking unknown links. Never share OTPs or banking credentials."

    # Gemini analysis
    reason = analyze_message(request.message)
    print("=" * 60)
    print("GEMINI RESPONSE:")
    print(reason)
    print("=" * 60)
    
    advice = "Avoid clicking unknown links. Never share OTPs or banking credentials."
    # Save history
    history = ScanHistory(
        message=request.message,
        language="English",
        risk_score=risk_score,
        status=status,
        keywords=keywords,
        urls=urls,
        reason=reason,
        advice=advice,
    )

    db.add(history)
    db.commit()
    db.refresh(history)

    return ScanResponse(
        language="English",
        risk_score=risk_score,
        status=status,
        keywords=keywords,
        urls=urls,
        reason=reason,
        advice=advice,
    )