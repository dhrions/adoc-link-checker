import time
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

from adoc_link_checker.discovery import find_adoc_files
from adoc_link_checker.extractor import extract_links
from adoc_link_checker.checker import create_session, check_url
from adoc_link_checker.report import write_report

logger = logging.getLogger(__name__)


def process_file(
    file_path: str,
    delay: float,
    timeout: int,
    blacklist: list,
    excluded_urls: set,
) -> list:
    """
    Process a single .adoc file and return its broken links.
    A dedicated HTTP session is created per thread (thread-safe).
    """
    session = create_session()
    broken_links = []

    links = extract_links(file_path)
    links = [url for url in links if url not in excluded_urls]

    logger.debug(f"📂 Processing {file_path} ({len(links)} URLs)")

    for url in links:
        time.sleep(delay)
        if not check_url(session, url, timeout, tuple(blacklist)):
            logger.warning(f"❌ Broken URL: {url}")
            broken_links.append((url, "URL not accessible"))
        else:
            logger.debug(f"✅ URL OK: {url}")

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
    """
    Orchestrate the link checking process.
    """
    if not output_file:
        raise ValueError("output_file must be provided")

    # 1️⃣ Discover .adoc files
    adoc_files = find_adoc_files(root_path)
    logger.info(f"📄 Found {len(adoc_files)} .adoc file(s)")

    # 2️⃣ Load excluded URLs
    excluded_urls = set()
    if exclude_from:
        try:
            with open(exclude_from, "r", encoding="utf-8") as f:
                excluded_urls = {
                    line.strip().rstrip("/")
                    for line in f
                    if line.strip() and not line.strip().startswith("#")
                }
        except Exception as e:
            logger.warning(
                f"Unable to read exclusion file {exclude_from}: {e}"
            )

    logger.info(f"📋 Excluded URLs loaded: {len(excluded_urls)}")

    broken_links: dict[str, list] = {}

    # 3️⃣ Parallel processing (one HTTP session per thread)
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(
                process_file,
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
            try:
                result = future.result()
                if result:
                    broken_links[file] = result
            except Exception as e:
                logger.error(f"Error processing {file}: {e}")

    # 4️⃣ Write report
    write_report(output_file, broken_links)

    # 5️⃣ Final status
    if broken_links:
        logger.info("❌ Broken URLs found")
    else:
        logger.info("✅ No broken URLs found")
