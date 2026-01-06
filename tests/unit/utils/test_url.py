from adoc_link_checker.core.extractor import extract_links
from adoc_link_checker.utils.url import normalize_url


def test_normalize_url_trailing_dot():
    assert (
        normalize_url("https://example.com.")
        == "https://example.com"
    )


def test_normalize_url_trailing_comma():
    assert (
        normalize_url("https://example.com,")
        == "https://example.com"
    )


def test_normalize_url_trailing_parenthesis():
    assert (
        normalize_url("https://example.com)")
        == "https://example.com"
    )


def test_normalize_url_trailing_bracket():
    assert (
        normalize_url("https://example.com]")
        == "https://example.com"
    )


def test_normalize_url_keeps_valid_path():
    assert (
        normalize_url("https://fr.wikipedia.org/wiki/Tactique_militaire")
        == "https://fr.wikipedia.org/wiki/Tactique_militaire"
    )
