from unittest.mock import Mock, patch

from adoc_link_checker.http.service import LinkChecker
from adoc_link_checker.core.context import LinkCheckContext


def test_linkchecker_uses_cache():
    """
    Ensure that LinkChecker does not perform multiple HTTP checks
    for the same URL thanks to the shared cache.
    """
    # --- Setup ---
    session = Mock()
    context = LinkCheckContext(timeout=5, blacklist=[])

    checker = LinkChecker(session=session, context=context)
    url = "https://example.com"

    # --- Patch the low-level HTTP check ---
    with patch(
        "adoc_link_checker.http.service.check_url",
        return_value=True,
    ) as mock_check_url:

        # --- First call: real check ---
        result1 = checker.check(url)

        # --- Second call: must use cache ---
        result2 = checker.check(url)

    # --- Assertions ---
    assert result1 is True
    assert result2 is True

    # check_url must be called only once
    mock_check_url.assert_called_once_with(
        session=session,
        url=url,
        timeout=context.timeout,
        blacklist=tuple(context.blacklist),
    )
