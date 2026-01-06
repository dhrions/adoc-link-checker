import logging
from urllib.parse import urlparse

logger = logging.getLogger(__name__)


def is_valid_url(url: str) -> bool:
    """Vérifie si une URL est valide (scheme http/https et présence d'un netloc)."""
    try:
        result = urlparse(url)
        valid = all([result.scheme in ('http', 'https'), result.netloc])
        # logger.debug(f"URL {url} est valide ? {valid}")
        return valid
    except ValueError:
        return False


def is_blacklisted(url: str, blacklist: list) -> bool:
    """Vérifie si une URL est dans la blacklist."""
    blacklisted = any(domain in url for domain in blacklist)
    # logger.debug(f"URL {url} est blacklistée ? {blacklisted}")
    return blacklisted


def normalize_url(url: str) -> str:
    """
    Normalize a URL by removing fragments, queries,
    surrounding quotes, trailing slashes and punctuation.
    """
    url = url.split("#")[0].split("?")[0].strip('"\'<>')

    # Remove common trailing punctuation from prose
    url = url.rstrip(".,;:!?)[]")

    # Remove trailing slash (optional, but consistent)
    url = url.rstrip("/")

    return url


def is_blacklisted(url: str, blacklist: list[str]) -> bool:
    """
    Return True if the URL's domain matches a blacklisted domain.
    """
    try:
        netloc = urlparse(url).netloc.lower()
    except ValueError:
        return False

    for domain in blacklist:
        domain = domain.lower()
        if netloc == domain or netloc.endswith("." + domain):
            return True

    return False


def youtube_id_to_url(youtube_id: str) -> str:
    """Convertit un ID YouTube en URL complète."""
    return f"https://www.youtube.com/watch?v={youtube_id}"
