import os
import time
import logging
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from adoc_link_checker.link_extractor import extract_links_from_file
from adoc_link_checker.link_checker import check_url, create_session
from adoc_link_checker.url_utils import is_valid_url

logger = logging.getLogger(__name__)

def process_file(session, file_path: str, delay: float, timeout: int, blacklist: list) -> list:
    broken_links = []
    links = extract_links_from_file(file_path)
    logger.info(f"📂 Processing {file_path} ({len(links)} URLs to check)...")
    for url in links:
        if not is_valid_url(url):
            continue
        time.sleep(delay)
        if not check_url(session, url, timeout, tuple(blacklist)):
            logger.warning(f"❌ Broken URL: {url}")
            broken_links.append((url, "URL not accessible"))
        # Ne pas logger les succès pour éviter le bruit
    return broken_links



def run_check(root_dir: str, max_workers: int, delay: float, timeout: int, output_file: str, blacklist: list, exclude_from: str) -> None:
    """Lance la vérification des liens dans les fichiers .adoc."""
    broken_links = {}
    adoc_files = []
    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.adoc'):
                adoc_files.append(os.path.join(root, file))
    logger.info(f"🔍 Found {len(adoc_files)} .adoc files. Checking URLs...")
    session = create_session()
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(process_file, session, file, delay, timeout, blacklist): file
            for file in adoc_files
        }
        for future in as_completed(futures):
            file = futures[future]
            try:
                file_broken_links = future.result()
                if file_broken_links:
                    broken_links[file] = file_broken_links
            except Exception as e:
                logger.error(f"Error processing {file}: {e}")
    if not broken_links:
        logger.info("✅ No broken URLs found!")
    else:
        logger.info("❌ Broken URLs found:")
        for file, links in broken_links.items():
            logger.info(f"\n📄 {file}")
            for url, reason in links:
                logger.info(f"  🔗 {url} ({reason})")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(broken_links, f, indent=2, ensure_ascii=False)
    logger.info(f"📊 Results saved to {output_file}.")
