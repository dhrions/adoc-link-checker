from unittest.mock import patch

from adoc_link_checker.runner import run_check


@patch("adoc_link_checker.runner.write_report")
@patch("adoc_link_checker.runner.find_adoc_files")
@patch("adoc_link_checker.runner.check_url")
@patch("adoc_link_checker.runner.extract_links")
@patch("adoc_link_checker.runner.create_session")
def test_run_check_happy_path(
    mock_session,
    mock_extract,
    mock_check,
    mock_find,
    mock_report,
    tmp_path,
):
    mock_find.return_value = ["file.adoc"]
    mock_extract.return_value = {"https://example.com"}
    mock_check.return_value = True

    output = tmp_path / "out.json"

    run_check(
        root_path="file.adoc",
        max_workers=1,
        delay=0,
        timeout=5,
        output_file=str(output),
        blacklist=[],
        exclude_from=None,
    )

    mock_report.assert_called_once()
