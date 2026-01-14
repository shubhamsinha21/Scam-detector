from urllib.parse import urlparse

TRUSTED_DOMAINS = {
    "google.com",
    "instagram.com",
    "facebook.com",
    "youtube.com",
    "linkedin.com",
    "github.com",
    "microsoft.com",
    "amazon.com",
    "apple.com"
}

def extract_domain(url: str) -> str:
    parsed = urlparse(url)
    return parsed.netloc.lower().replace("www.", "")

def is_trusted_domain(url: str) -> bool:
    return extract_domain(url) in TRUSTED_DOMAINS
