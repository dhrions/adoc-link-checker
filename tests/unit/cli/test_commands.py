from unittest.mock import patch

from adoc_link_checker.cli.commands import check_links_command


@patch("adoc_link_checker.cli.commands.run_check")
def test_check_links_command_calls_runner(mock_run):
    check_links_command(
        path="docs",
        timeout=10,
        max_workers=4,
        delay=0.2,
        output="out.json",
        blacklist=("example.com",),
        exclude_from=None,
        fail_on_broken=False,
        verbose=0,
        quiet=False,
    )

    mock_run.assert_called_once()

    kwargs = mock_run.call_args.kwargs

    assert kwargs["root_path"].endswith("docs")
    assert kwargs["timeout"] == 10
    assert kwargs["max_workers"] == 4
    assert kwargs["delay"] == 0.2
    assert kwargs["output_file"] == "out.json"
    assert "example.com" in kwargs["blacklist"]
    assert kwargs["exclude_from"] is None
    assert kwargs["fail_on_broken"] is False


@patch("adoc_link_checker.cli.commands.run_check")
def test_check_links_command_fail_on_broken(mock_run):
    check_links_command(
        path="docs",
        timeout=5,
        max_workers=1,
        delay=0,
        output="out.json",
        blacklist=(),
        exclude_from=None,
        fail_on_broken=True,
        verbose=0,
        quiet=True,
    )

    kwargs = mock_run.call_args.kwargs
    assert kwargs["fail_on_broken"] is True
