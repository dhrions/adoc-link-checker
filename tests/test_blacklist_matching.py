from adoc_link_checker.url_utils import is_blacklisted


def test_blacklist_false_positive_substring():
    """
    Demonstrates that substring-based blacklist matching
    incorrectly blocks unrelated domains.
    """

    blacklist = ["example.com"]

    # ❌ This should NOT be blacklisted
    url = "https://notexample.com/path"

    assert is_blacklisted(url, blacklist) is False
