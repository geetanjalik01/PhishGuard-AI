import re
import ipaddress
from urllib.parse import urlparse


SUSPICIOUS_WORDS = {
    "login",
    "verify",
    "secure",
    "account",
    "update",
    "bank",
    "paypal",
    "signin",
    "confirm",
    "wallet",
    "payment",
    "password"
}


def is_ip_address(domain: str) -> bool:
    try:
        ipaddress.ip_address(domain)
        return True
    except ValueError:
        return False


def extract_url_features(url: str) -> dict:

    parsed = urlparse(url)

    domain = parsed.netloc.lower()

    path = parsed.path.lower()

    full_url = url.lower()

    features = {}

    features["url_length"] = len(full_url)

    features["domain_length"] = len(domain)

    features["path_length"] = len(path)

    features["uses_https"] = int(parsed.scheme == "https")

    features["has_ip_address"] = int(is_ip_address(domain))

    features["dot_count"] = full_url.count(".")

    features["hyphen_count"] = full_url.count("-")

    features["slash_count"] = full_url.count("/")

    features["question_mark"] = int("?" in full_url)

    features["equal_sign"] = int("=" in full_url)

    features["at_symbol"] = int("@" in full_url)

    features["underscore_count"] = full_url.count("_")

    features["digit_count"] = sum(ch.isdigit() for ch in full_url)

    features["subdomain_count"] = max(domain.count(".") - 1, 0)

    features["contains_suspicious_word"] = int(
        any(word in full_url for word in SUSPICIOUS_WORDS)
    )

    return features