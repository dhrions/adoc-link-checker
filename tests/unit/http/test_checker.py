import responses

from adoc_link_checker.http.checker import check_url, create_session


@responses.activate
def test_check_url_head_ok():
    url = "https://example.com"

    responses.add(responses.HEAD, url, status=200)

    session = create_session()
    assert check_url(session, url, timeout=5, blacklist=()) is True


@responses.activate
def test_check_url_head_fails_get_ok():
    url = "https://example.com"

    responses.add(responses.HEAD, url, status=403)
    responses.add(responses.GET, url, status=200)

    session = create_session()
    assert check_url(session, url, timeout=5, blacklist=()) is True


@responses.activate
def test_check_url_get_fails():
    url = "https://example.com"

    responses.add(responses.HEAD, url, status=500)
    responses.add(responses.GET, url, status=500)

    session = create_session()
    assert check_url(session, url, timeout=5, blacklist=()) is False
