from adoc_link_checker.exclusions import load_excluded_urls
from adoc_link_checker.extractor import extract_links
from adoc_link_checker.processing import process_file
from adoc_link_checker.context import LinkCheckContext

from unittest.mock import patch


def test_excluded_url_with_trailing_slash_not_normalized(tmp_path):
    """
    Demonstrates that exclusion fails when URL normalization
    differs between excluded URLs and extracted URLs.
    """

    # --- Exclusion file ---
    exclude_file = tmp_path / "exclude.txt"
    exclude_file.write_text("https://example.com\n")

    excluded_urls = load_excluded_urls(str(exclude_file))

    # --- AsciiDoc file with trailing slash ---
    adoc_file = tmp_path / "doc.adoc"
    adoc_file.write_text(
        "= Test\n\nhttps://example.com/\n"
    )

    # --- Context ---
    context = LinkCheckContext(timeout=5, blacklist=[])

    # --- Mock HTTP check to always fail ---
    with patch("adoc_link_checker.processing.LinkChecker.check", return_value=False):
        broken_links = process_file(
            file_path=str(adoc_file),
            delay=0,
            context=context,
            excluded_urls=excluded_urls,
        )

    # ❌ Fails today: link is NOT excluded
    # ✅ Should be empty after normalization fix
    assert broken_links == []
