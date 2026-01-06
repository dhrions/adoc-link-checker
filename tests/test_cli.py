from click.testing import CliRunner
from unittest.mock import patch


from adoc_link_checker.cli import cli


def test_cli_requires_output(tmp_path):
    """
    CLI must fail if --output is missing,
    assuming PATH is valid.
    """
    # Create a valid .adoc file
    adoc_file = tmp_path / "test.adoc"
    adoc_file.write_text("= Test")

    runner = CliRunner()

    result = runner.invoke(
        cli,
        [
            "check-links",
            str(adoc_file),
        ],
    )

    assert result.exit_code != 0
    assert "--output" in result.output


@patch("adoc_link_checker.cli.run_check")
def test_cli_check_links_ok(mock_run, tmp_path):
    """
    CLI succeeds when PATH and --output are valid.
    """
    # Valid input file
    adoc_file = tmp_path / "test.adoc"
    adoc_file.write_text("= Test")

    output_file = tmp_path / "report.json"

    runner = CliRunner()

    result = runner.invoke(
        cli,
        [
            "check-links",
            str(adoc_file),
            "--output",
            str(output_file),
        ],
    )

    assert result.exit_code == 0
    mock_run.assert_called_once()
