from typing import Dict


def generate_explanation(url: str,
                         features: Dict,
                         risk_result: Dict) -> Dict:

    explanation = []

    recommendations = []

    if features["uses_https"] == 0:
        explanation.append(
            "The website does not use HTTPS encryption, making communication less secure."
        )

    if features["has_ip_address"] == 1:
        explanation.append(
            "The URL uses an IP address instead of a registered domain, which is common in phishing attacks."
        )

    if features["url_length"] > 75:
        explanation.append(
            "The URL is unusually long, which can be used to hide suspicious information."
        )

    if features["dot_count"] > 3:
        explanation.append(
            "The URL contains multiple subdomains, a technique sometimes used to imitate trusted websites."
        )

    if features["hyphen_count"] >= 2:
        explanation.append(
            "Multiple hyphens were detected in the URL, which can indicate an attempt to mimic a legitimate domain."
        )

    if features["contains_suspicious_word"] == 1:
        explanation.append(
            "The URL contains terms such as 'login', 'verify', or 'account' that are frequently seen in phishing campaigns."
        )

    if features["at_symbol"] == 1:
        explanation.append(
            "The '@' symbol can hide the actual destination of a URL."
        )

    if features["digit_count"] > 5:
        explanation.append(
            "The URL contains many numeric characters, which may indicate automatically generated domains."
        )

    score = risk_result["risk_score"]

    if score >= 75:

        recommendations = [

            "Do NOT open this link.",

            "Avoid entering personal or banking information.",

            "Report the URL to your organization's security team.",

            "Verify the website through its official homepage."
        ]

    elif score >= 50:

        recommendations = [

            "Proceed with caution.",

            "Verify the domain name carefully.",

            "Do not download files unless the sender is trusted."
        ]

    elif score >= 25:

        recommendations = [

            "Double-check the sender and destination before continuing."
        ]

    else:

        recommendations = [

            "No major phishing indicators were detected, but always remain cautious."
        ]

    summary = (
        f"This URL received a risk score of "
        f"{risk_result['risk_score']}/100 "
        f"and is classified as "
        f"{risk_result['risk_level']} risk."
    )

    return {

        "summary": summary,

        "explanation": explanation,

        "recommendations": recommendations

    }