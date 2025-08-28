import logging
from urllib.parse import urlparse

logger = logging.getLogger(__name__)


def is_valid_url(url: str) -> bool:
    """Vérifie si une URL est valide (scheme http/https et présence d'un netloc)."""
    try:
        result = urlparse(url)
        valid = all([result.scheme in ('http', 'https'), result.netloc])
        logger.debug(f"URL {url} est valide ? {valid}")
        return valid
    except ValueError:
        return False


def is_blacklisted(url: str, blacklist: list) -> bool:
    """Vérifie si une URL est dans la blacklist."""
    blacklisted = any(domain in url for domain in blacklist)
    logger.debug(f"URL {url} est blacklistée ? {blacklisted}")
    return blacklisted


def normalize_url(url: str) -> str:
    """Normalise une URL en supprimant les fragments, queries et caractères superflus."""
    url = url.split('#')[0].split('?')[0].strip('"\'<>').rstrip('/')
    return url


def youtube_id_to_url(youtube_id: str) -> str:
    """Convertit un ID YouTube en URL complète."""
    return f"https://www.youtube.com/watch?v={youtube_id}"
