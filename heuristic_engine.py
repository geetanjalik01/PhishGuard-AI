from typing import Dict


def calculate_risk(features: Dict) -> Dict:

    score = 0
    reasons = []

    if features["uses_https"] == 0:
        score += 20
        reasons.append(
            "HTTPS encryption is not used on the website."
        )

    
    if features["has_ip_address"] == 1:
        score += 30
        reasons.append(
            "Rather of using a domain name, the URL employs an IP address."
        )

    
    if features["url_length"] > 75:
        score += 10
        reasons.append(
            "The URL is unusually long."
        )

    
    if features["dot_count"] > 3:
        score += 10
        reasons.append(
            "The URL contains many subdomains."
        )

    
    if features["hyphen_count"] >= 2:
        score += 10
        reasons.append(
            "The URL contains multiple hyphens."
        )

    
    if features["at_symbol"] == 1:
        score += 20
        reasons.append(
            "The URL contains an '@' symbol."
        )

    
    if features["digit_count"] > 5:
        score += 5
        reasons.append(
            "The URL contains many numeric characters."
        )

    
    if features["contains_suspicious_word"] == 1:
        score += 15
        reasons.append(
            "There are often used phishing keywords in the URL."
        )

    
    if features["question_mark"] == 1:
        score += 5
        reasons.append(
            "The URL contains query parameters."
        )

    
    if features["equal_sign"] == 1:
        score += 5
        reasons.append(
            "The URL contains parameter assignments."
        )

    
    score = min(score, 100)

    if score >= 75:
        level = "Critical"
    elif score >= 50:
        level = "High"
    elif score >= 25:
        level = "Medium"
    else:
        level = "Low"

    return {
        "risk_score": score,
        "risk_level": level,
        "reasons": reasons
    }

