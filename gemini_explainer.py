import streamlit as st
from google import genai

# Smart API Key Loading: Works locally AND on Streamlit Cloud!
try:
    # Tries to get the key from Streamlit Cloud Secrets (when deployed)
    api_key = st.secrets["GEMINI_API_KEY"]
except:
    # If that fails (meaning you are running locally), it uses your local config.py
    from config import GEMINI_API_KEY
    api_key = GEMINI_API_KEY

# Initialize the client using whichever key it successfully found
client = genai.Client(api_key=api_key)

def explain_url(url, features, risk):

    prompt = f"""
You are a cybersecurity expert.

Analyze this URL:

URL:
{url}

Extracted Features:
{features}

Risk Score:
{risk['risk_score']}/100

Risk Level:
{risk['risk_level']}

Explain:
1. Why the URL is risky.
2. Which features indicate phishing.
3. Give 3 security recommendations.

Keep the response under 150 words.
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt,
        )
        return response.text

    except Exception:
        return f"""
### AI Security Analysis

**Risk Level:** {risk['risk_level']}

This URL received a **{risk['risk_score']}/100** risk score based on heuristic analysis.

**Possible Reasons**
{chr(10).join("- " + r for r in risk["reasons"]) if risk["reasons"] else "- No suspicious indicators detected."}

**Recommendations**
- Do not enter passwords.
- Verify the domain before visiting.
- Enable two-factor authentication.
- Avoid downloading files from unknown websites.
"""