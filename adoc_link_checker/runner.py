import os
import re
import time
import logging
import json
from functools import lru_cache
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import requests
from adoc_link_checker.config import (
    TIMEOUT, MAX_WORKERS, DELAY, USER_AGENT, BLACKLIST,
    LINK_PATTERNS, LOGGING_CONFIG, RETRY_CONFIG, OUTPUT_FILE
)
from adoc_link_checker.url_utils import is_valid_url, is_blacklisted, normalize_url, youtube_id_to_url

logger = logging.getLogger(__name__)

def load_excluded_urls(exclude_from: str) -> set:
    """Charge la liste des URLs à exclure depuis un fichier."""
    if not exclude_from:
        return set()
    try:
        with open(exclude_from, 'r', encoding='utf-8') as f:
            return {normalize_url(line.strip()) for line in f if line.strip()}
    except Exception as e:
        logger.warning(f"Impossible de lire le fichier d'exclusion {exclude_from}: {e}")
        return set()

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
                if is_valid_url(url):
                    links.add(url)
        return links
    except Exception as e:
        logger.debug(f"Erreur lors de la lecture de {file_path}: {e}")
        return set()

@lru_cache(maxsize=1024)
def check_url(session: requests.Session, url: str, timeout: int, blacklist: tuple) -> bool:
    """Vérifie si une URL est accessible."""
    if is_blacklisted(url, list(blacklist)):
        logger.debug(f"Ignoring blacklisted URL: {url}")
        return True
    try:
        response = session.head(url, timeout=timeout, allow_redirects=True)
        return response.status_code < 400
    except requests.exceptions.RequestException as e:
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

def process_file(session: requests.Session, file_path: str, delay: float, timeout: int, blacklist: list, excluded_urls: set) -> list:
    """Traite un fichier .adoc pour vérifier ses liens."""
    broken_links = []
    links = extract_links_from_file(file_path)
    logger.debug(f"📂 Processing {file_path} ({len(links)} URLs to check)...")

    # Filtrer les URLs exclues
    links = [url for url in links if url not in excluded_urls]

    for url in links:
        time.sleep(delay)
        if not check_url(session, url, timeout, tuple(blacklist)):
            logger.warning(f"  ❌ Broken URL: {url}")
            broken_links.append((url, "URL not accessible"))
        else:
            logger.debug(f"  ✅ URL checked: {url}")
    return broken_links

def run_check(root_dir: str, max_workers: int, delay: float, timeout: int, output_file: str, blacklist: list, exclude_from: str) -> None:
    """Lance la vérification des liens dans les fichiers .adoc."""
    broken_links = {}
    adoc_files = []
    total_urls_checked = 0

    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.adoc'):
                adoc_files.append(os.path.join(root, file))

    excluded_urls = load_excluded_urls(exclude_from)
    logger.info(f"📋 Excluded URLs loaded: {len(excluded_urls)}")
    logger.info(f"🔍 Found {len(adoc_files)} .adoc files. Checking URLs...")

    session = create_session()
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(process_file, session, file, delay, timeout, blacklist, excluded_urls): file
            for file in adoc_files
        }
        for future in as_completed(futures):
            file = futures[future]
            try:
                file_broken_links = future.result()
                if file_broken_links:
                    broken_links[file] = file_broken_links
                # Compter le nombre d'URLs traitées dans ce fichier
                links_in_file = extract_links_from_file(file)
                total_urls_checked += len(links_in_file)
            except Exception as e:
                logger.error(f"Error processing {file}: {e}")

    # Afficher le nombre total d'URLs traitées
    logger.info(f"📊 Total URLs checked: {total_urls_checked}")

    if not broken_links:
        logger.info("✅ No broken URLs found!")
    else:
        logger.info("❌ Broken URLs found:")
        for file, links in broken_links.items():
            logger.info(f"\n📄 {os.path.abspath(file)}")
            for url, reason in links:
                logger.info(f"  🔗 {url} ({reason})")

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(broken_links, f, indent=2, ensure_ascii=False)
    logger.info(f"📊 Results saved to {output_file}.")

