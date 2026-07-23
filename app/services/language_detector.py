from langdetect import detect


def detect_language(text: str) -> str:
    try:
        lang = detect(text)

        if lang == "en":
            return "English"

        if lang == "hi":
            return "Hindi"

        if lang == "gu":
            return "Gujarati"

        return "Unknown"

    except Exception:
        return "Unknown"