from app.utils.constants import (
    SAFE_THRESHOLD,
    SUSPICIOUS_THRESHOLD,
    ScanStatus,
)


def calculate_risk_score(
    keywords: list[str],
    urls: list[str],
    ai_score: int = 0,
) -> dict:
    """
    Calculate overall scam risk score.
    """

    score = 0

    # Keyword contribution
    score += len(keywords) * 10

    # URL contribution
    score += len(urls) * 15

    # AI contribution
    score += ai_score

    # Maximum score = 100
    score = min(score, 100)

    if score < SAFE_THRESHOLD:
        status = ScanStatus.SAFE
    elif score < SUSPICIOUS_THRESHOLD:
        status = ScanStatus.SUSPICIOUS
    else:
        status = ScanStatus.DANGEROUS

    return {
        "score": score,
        "status": status.value,
    }