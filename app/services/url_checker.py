import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"

TRUSTED_FILE = DATA_DIR / "trusted_domains.json"
PHISHING_FILE = DATA_DIR / "phishing_domains.json"


def load_domains(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


TRUSTED_DOMAINS = load_domains(TRUSTED_FILE)
PHISHING_DOMAINS = load_domains(PHISHING_FILE)


def check_urls(urls: list[str]):
    """
    Check extracted URLs against trusted and phishing lists.
    """

    results = []

    for url in urls:
        status = "unknown"

        lower_url = url.lower()

        if any(domain.lower() in lower_url for domain in PHISHING_DOMAINS):
            status = "phishing"

        elif any(domain.lower() in lower_url for domain in TRUSTED_DOMAINS):
            status = "trusted"

        results.append(
            {
                "url": url,
                "status": status,
            }
        )

    return results