from unittest.mock import patch

from adoc_link_checker.runner import run_check


@patch("adoc_link_checker.runner.write_report")
@patch("adoc_link_checker.runner.find_adoc_files")
@patch("adoc_link_checker.runner.process_file")
def test_run_check_happy_path(
    mock_process,
    mock_find,
    mock_report,
    tmp_path,
):
    """
    run_check orchestrates processing and writes a report.
    """
    mock_find.return_value = ["file.adoc"]
    mock_process.return_value = []

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

    mock_process.assert_called_once()
    mock_report.assert_called_once()
