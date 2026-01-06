import os
import re
import time
import logging
import json
from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from adoc_link_checker.config import (
    USER_AGENT,
    LINK_PATTERNS,
    RETRY_CONFIG,
)
from adoc_link_checker.url_utils import (
    is_valid_url,
    is_blacklisted,
    normalize_url,
    youtube_id_to_url,
)

logger = logging.getLogger(__name__)


def load_excluded_urls(exclude_from: str) -> set:
    if not exclude_from:
        return set()

    try:
        with open(exclude_from, "r", encoding="utf-8") as f:
            return {
                normalize_url(line.strip())
                for line in f
                if line.strip() and not line.strip().startswith("#")
            }
    except Exception as e:
        logger.warning(f"Unable to read exclusion file {exclude_from}: {e}")
        return set()


def extract_links_from_file(file_path: str) -> set:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        links = set()
        for pattern in LINK_PATTERNS:
            for match in re.finditer(pattern, content):
                if pattern == LINK_PATTERNS[1]:
                    url = youtube_id_to_url(match.group(1))
                else:
                    url = normalize_url(match.group(0).replace("link:", ""))

                if is_valid_url(url):
                    links.add(url)

        return links
    except Exception as e:
        logger.debug(f"Error reading {file_path}: {e}")
        return set()


@lru_cache(maxsize=1024)
def check_url(url: str, timeout: int, blacklist: tuple) -> bool:
    if is_blacklisted(url, list(blacklist)):
        return True

    try:
        response = requests.head(url, timeout=timeout, allow_redirects=True)
        if response.status_code >= 400:
            response = requests.get(url, timeout=timeout, stream=True)
        return response.status_code < 400
    except requests.RequestException as e:
        logger.warning(f"⚠️ {url} failed: {e}")
        return False


def create_session() -> requests.Session:
    session = requests.Session()
    retries = Retry(**RETRY_CONFIG)
    session.mount("https://", HTTPAdapter(max_retries=retries))
    session.mount("http://", HTTPAdapter(max_retries=retries))
    session.headers.update({"User-Agent": USER_AGENT})
    return session


def process_file(
    session: requests.Session,
    file_path: str,
    delay: float,
    timeout: int,
    blacklist: list,
    excluded_urls: set,
) -> list:
    broken_links = []
    links = extract_links_from_file(file_path)
    links = [url for url in links if url not in excluded_urls]

    for url in links:
        time.sleep(delay)
        if not check_url(url, timeout, tuple(blacklist)):
            broken_links.append((url, "URL not accessible"))

    return broken_links


def run_check(
    root_path: str,
    max_workers: int,
    delay: float,
    timeout: int,
    output_file: str,
    blacklist: list,
    exclude_from: str,
) -> None:
    if not output_file:
        raise ValueError("output_file must be provided")

    adoc_files = []

    if os.path.isfile(root_path):
        if not root_path.endswith(".adoc"):
            raise ValueError("Provided file is not a .adoc file")
        adoc_files.append(root_path)
    else:
        for root, _, files in os.walk(root_path):
            for file in files:
                if file.endswith(".adoc"):
                    adoc_files.append(os.path.join(root, file))

    logger.info(f"📄 Found {len(adoc_files)} .adoc file(s)")

    excluded_urls = load_excluded_urls(exclude_from)
    logger.info(f"📋 Excluded URLs loaded: {len(excluded_urls)}")

    session = create_session()
    broken_links = {}

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(
                process_file,
                session,
                file,
                delay,
                timeout,
                blacklist,
                excluded_urls,
            ): file
            for file in adoc_files
        }

        for future in as_completed(futures):
            file = futures[future]
            result = future.result()
            if result:
                broken_links[file] = result

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(broken_links, f, indent=2, ensure_ascii=False)

    if broken_links:
        logger.info("❌ Broken URLs found")
    else:
        logger.info("✅ No broken URLs found")
