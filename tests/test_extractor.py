from adoc_link_checker.extractor import extract_links


def test_extract_http_links(tmp_path):
    content = """
    link:https://example.com[]
    https://example.org/page
    """
    file = tmp_path / "doc.adoc"
    file.write_text(content)

    links = extract_links(str(file))

    assert "https://example.com" in links
    assert "https://example.org/page" in links


def test_extract_youtube_id(tmp_path):
    file = tmp_path / "doc.adoc"
    file.write_text("video::dQw4w9WgXcQ[]")

    links = extract_links(str(file))

    assert "https://www.youtube.com/watch?v=dQw4w9WgXcQ" in links
