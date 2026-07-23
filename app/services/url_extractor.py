"""URL extraction from message text """
import re

URL_PATTERN = re.compile(
    r"(https?://[^\s]+|www\.[^\s]+)",
    re.IGNORECASE,
)

def extract_urls(text: str) -> list[str]:
    """
    Extract URLs from text.
    """
    if not text:
        return []

    return URL_PATTERN.findall(text)