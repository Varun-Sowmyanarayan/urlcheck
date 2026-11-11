from urllib.parse import urlparse
import ipaddress

SUSPICIOUS_WORDS = ["login", "verify", "secure", "account", "update", "password", "bank"]


def check_url(url):
    url = url.strip()
    if "://" not in url:
        url = "http://" + url

    parsed = urlparse(url)
    host = parsed.hostname or ""

    score = 0
    reasons = []

    # Rule 1: no HTTPS
    if parsed.scheme != "https":
        score += 20
        reasons.append("Does not use HTTPS")

    # Rule 2: IP address instead of a domain name
    is_ip = False
    try:
        ipaddress.ip_address(host)
        is_ip = True
        score += 30
        reasons.append("Uses an IP address instead of a domain name")
    except ValueError:
        pass

    # Rule 3: too many subdomains (only for real domain names)
    if host.count(".") >= 3 and not is_ip:
        score += 20
        reasons.append("Too many subdomains")

    # Rule 4: suspicious words
    found = [word for word in SUSPICIOUS_WORDS if word in url.lower()]
    if found:
        score += 10 * len(found)
        reasons.append("Suspicious words: " + ", ".join(found))

    # Rule 5: very long URL
    if len(url) > 75:
        score += 15
        reasons.append("Very long URL")

    score = min(score, 100)

    if score < 20:
        verdict = "SAFE"
    elif score < 50:
        verdict = "SUSPICIOUS"
    else:
        verdict = "DANGEROUS"

    return {"url": url, "score": score, "verdict": verdict, "reasons": reasons}