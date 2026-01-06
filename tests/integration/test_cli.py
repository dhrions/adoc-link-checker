from click.testing import CliRunner
from unittest.mock import patch

from adoc_link_checker.cli import cli


def _create_adoc(tmp_path):
    """
    Helper: create a minimal valid .adoc file.
    """
    adoc_file = tmp_path / "test.adoc"
    adoc_file.write_text("= Test\n\nhttps://example.com")
    return adoc_file


def test_cli_requires_output(tmp_path):
    """
    CLI must fail if --output is missing,
    assuming PATH is valid.
    """
    adoc_file = _create_adoc(tmp_path)

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


@patch("adoc_link_checker.cli.main.run_check")
def test_cli_check_links_ok(mock_run, tmp_path):
    """
    Nominal execution with required arguments.
    """
    adoc_file = _create_adoc(tmp_path)
    output = tmp_path / "report.json"

    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "check-links",
            str(adoc_file),
            "--output",
            str(output),
        ],
    )

    assert result.exit_code == 0
    mock_run.assert_called_once()


@patch("adoc_link_checker.cli.main.run_check")
def test_cli_quiet_mode(mock_run, tmp_path):
    """
    --quiet branch.
    """
    adoc_file = _create_adoc(tmp_path)
    output = tmp_path / "out.json"

    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "check-links",
            str(adoc_file),
            "--output",
            str(output),
            "--quiet",
        ],
    )

    assert result.exit_code == 0
    mock_run.assert_called_once()


@patch("adoc_link_checker.cli.main.run_check")
def test_cli_verbose_info(mock_run, tmp_path):
    """
    -v branch (INFO).
    """
    adoc_file = _create_adoc(tmp_path)
    output = tmp_path / "out.json"

    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "check-links",
            str(adoc_file),
            "--output",
            str(output),
            "-v",
        ],
    )

    assert result.exit_code == 0
    mock_run.assert_called_once()


@patch("adoc_link_checker.cli.main.run_check")
def test_cli_verbose_debug(mock_run, tmp_path):
    """
    -vv branch (DEBUG).
    """
    adoc_file = _create_adoc(tmp_path)
    output = tmp_path / "out.json"

    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "check-links",
            str(adoc_file),
            "--output",
            str(output),
            "-vv",
        ],
    )

    assert result.exit_code == 0
    mock_run.assert_called_once()


@patch("adoc_link_checker.cli.main.run_check")
def test_cli_blacklist_and_exclude(mock_run, tmp_path):
    """
    --blacklist and --exclude-from branches.
    """
    adoc_file = _create_adoc(tmp_path)

    exclude_file = tmp_path / "exclude.txt"
    exclude_file.write_text("https://example.com")

    output = tmp_path / "out.json"

    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "check-links",
            str(adoc_file),
            "--output",
            str(output),
            "--blacklist",
            "example.com",
            "--exclude-from",
            str(exclude_file),
        ],
    )

    assert result.exit_code == 0
    mock_run.assert_called_once()
