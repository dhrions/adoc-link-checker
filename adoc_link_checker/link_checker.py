import logging
from functools import lru_cache
from urllib.parse import urlparse
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import requests
from requests.exceptions import RequestException, ConnectionError
from adoc_link_checker.url_utils import is_blacklisted
from adoc_link_checker.config import USER_AGENT, RETRY_CONFIG

logger = logging.getLogger(__name__)


@lru_cache(maxsize=1024)
def check_url(session: requests.Session, url: str, timeout: int, blacklist: tuple) -> bool:
    if is_blacklisted(url, list(blacklist)):
        logger.debug(f"Ignoring blacklisted URL: {url}")
        return True
    try:
        response = session.head(url, timeout=timeout, allow_redirects=True)
        return response.status_code < 400
    except ConnectionError as e:
        if "NameResolutionError" in str(e):
            logger.warning(f"⚠️ DNS resolution failed for {url}. Marking as broken.")
            return False  # Considérer comme un lien brisé
        logger.warning(f"⚠️ Connection error for {url}: {str(e)}")
        return False
    except RequestException as e:
        logger.warning(f"⚠️ {url} failed: {str(e)}")
        return False



def create_session() -> requests.Session:
    """Crée une session configurée avec retries et user-agent."""
    session = requests.Session()
    retries = Retry(**RETRY_CONFIG)
    session.mount('https://', HTTPAdapter(max_retries=retries))
    session.mount('http://', HTTPAdapter(max_retries=retries))
    session.headers.update({"User-Agent": USER_AGENT})
    return session
