"""AI detection pipeline orchestrator (to be implemented)."""
from app.utils.constants import (
    SAFE_THRESHOLD,
    SUSPICIOUS_THRESHOLD,
)


class AIDetector:

    def analyze(self, keyword_count: int, suspicious_urls: int):

        score = 0

        score += keyword_count * 12

        score += suspicious_urls * 30

        score = min(score, 100)

        if score < SAFE_THRESHOLD:

            status = "Safe"

        elif score < SUSPICIOUS_THRESHOLD:

            status = "Suspicious"

        else:

            status = "Dangerous"

        return score, status