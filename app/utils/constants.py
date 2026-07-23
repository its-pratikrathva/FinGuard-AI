from enum import Enum

class ScanStatus(str, Enum):
    SAFE = "Safe"
    SUSPICIOUS = "Suspicious"
    DANGEROUS = "Dangerous"


SAFE_THRESHOLD = 30
SUSPICIOUS_THRESHOLD = 70
DANGEROUS_THRESHOLD = 100


DEFAULT_SAFE_MESSAGE = (
    "This message appears safe."
)

DEFAULT_WARNING_MESSAGE = (
    "Be careful before clicking any links."
)

DEFAULT_DANGER_MESSAGE = (
    "This message is highly suspicious."
)