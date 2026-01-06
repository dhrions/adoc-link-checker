from adoc_link_checker.discovery import find_adoc_files


def test_find_single_adoc_file(tmp_path):
    file = tmp_path / "test.adoc"
    file.write_text("= Test")

    files = find_adoc_files(str(file))
    assert files == [str(file)]


def test_find_adoc_files_in_directory(tmp_path):
    (tmp_path / "a.adoc").write_text("= A")
    (tmp_path / "b.adoc").write_text("= B")
    (tmp_path / "c.txt").write_text("nope")

    files = find_adoc_files(str(tmp_path))

    assert len(files) == 2
    assert all(f.endswith(".adoc") for f in files)
