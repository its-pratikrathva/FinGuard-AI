"""
Gemini AI service for scam message analysis.
"""

import google.generativeai as genai

from app.config.settings import settings

# Configure Gemini
genai.configure(api_key=settings.GEMINI_API_KEY)

# Load model
model = genai.GenerativeModel(settings.GEMINI_MODEL)


def analyze_message(message: str) -> str:
    """
    Analyze a message using Gemini AI.
    Returns only the analysis text.
    """

    prompt = f"""
You are a cybersecurity expert.

Analyze the following message for phishing, scams, financial fraud,
OTP fraud, fake KYC, fake jobs, lottery scams,
UPI fraud, banking fraud, WhatsApp scams and social engineering.

Return:
1. Risk Level
2. Why it is risky
3. Advice to the user

Message:
{message}
"""

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
     print(f"Gemini Error: {e}")
    return (
        "Unable to analyze the message using AI at the moment. "
        "Please try again later."
    )