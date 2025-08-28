import re
import logging
from adoc_link_checker.url_utils import normalize_url, youtube_id_to_url

logger = logging.getLogger(__name__)

# Patterns pour l'extraction des liens
LINK_PATTERNS = [
    r'(link:)?https?:\/\/(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-z]{2,6}\b(?:[-a-zA-Z0-9@:%_\+.~#?&\/\/=]*)',  # URLs classiques
    r'video::([A-Za-z0-9_\-]{11})',    # Identifiants YouTube
]

def extract_links_from_file(file_path: str) -> set:
    """Extrait les liens depuis un fichier .adoc."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        links = set()
        for pattern in LINK_PATTERNS:
            for match in re.finditer(pattern, content):
                if pattern == LINK_PATTERNS[1]:  # video::youtube_id
                    youtube_id = match.group(1)
                    url = youtube_id_to_url(youtube_id)
                    logger.debug(f"YouTube ID={youtube_id}, URL={url}")
                else:
                    url = match.group(0).replace('link:', '')
                    url = normalize_url(url)
                links.add(url)
        return links
    except Exception as e:
        logger.debug(f"Erreur lors de la lecture de {file_path}: {e}")
        return set()
