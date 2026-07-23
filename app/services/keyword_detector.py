import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"

SCAM_FILE = DATA_DIR / "scam_keywords.json"


def load_keywords():
    with open(SCAM_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


KEYWORDS = load_keywords()


def detect_keywords(text: str):
    text = text.lower()

    matched = []

    all_keywords = (
        KEYWORDS["english"]
        + KEYWORDS["hindi"]
        + KEYWORDS["gujarati"]
    )

    for keyword in all_keywords:
        if keyword.lower() in text:
            matched.append(keyword)

    return matched