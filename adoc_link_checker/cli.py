import click
import logging
import os

from adoc_link_checker.runner import run_check
from adoc_link_checker.config import (
    TIMEOUT,
    MAX_WORKERS,
    DELAY,
    BLACKLIST,
    LOGGING_CONFIG,
)


@click.group()
@click.version_option(version="1.0.0")
def cli():
    """AdocX – AsciiDoc utilities."""
    pass


@cli.command("check-links")
@click.argument(
    "path",
    type=click.Path(exists=True, file_okay=True, dir_okay=True),
)
@click.option(
    "--timeout",
    type=int,
    default=TIMEOUT,
    help=f"Timeout for HTTP requests (seconds). [Default: {TIMEOUT}]",
)
@click.option(
    "--max-workers",
    type=int,
    default=MAX_WORKERS,
    help=f"Maximum number of threads. [Default: {MAX_WORKERS}]",
)
@click.option(
    "--delay",
    type=float,
    default=DELAY,
    help=f"Delay between each request (seconds). [Default: {DELAY}]",
)
@click.option(
    "--output",
    type=click.Path(dir_okay=False, writable=True),
    required=True,
    help="JSON output file for broken links (required).",
)
@click.option(
    "--blacklist",
    type=str,
    multiple=True,
    default=[],
    help="Domain to ignore (can be specified multiple times).",
)
@click.option(
    "--exclude-from",
    type=click.Path(exists=True, dir_okay=False),
    default=None,
    help="File with list of links to exclude.",
)
@click.option(
    "-v",
    "--verbose",
    count=True,
    help="Increase verbosity (-v = INFO, -vv = DEBUG).",
)
@click.option(
    "--quiet",
    is_flag=True,
    help="Disable logs except errors.",
)
def check_links(
    path,
    timeout,
    max_workers,
    delay,
    output,
    blacklist,
    exclude_from,
    verbose,
    quiet,
):
    """Check broken links in AsciiDoc files."""

    # Logging configuration
    logging.getLogger("urllib3").setLevel(logging.WARNING)

    if quiet:
        LOGGING_CONFIG["level"] = logging.ERROR
    elif verbose == 1:
        LOGGING_CONFIG["level"] = logging.INFO
    elif verbose >= 2:
        LOGGING_CONFIG["level"] = logging.DEBUG
    else:
        LOGGING_CONFIG["level"] = logging.INFO

    logging.basicConfig(
        level=LOGGING_CONFIG["level"],
        format=LOGGING_CONFIG["format"],
        force=True,
    )

    logger = logging.getLogger(__name__)

    abs_path = os.path.abspath(path)
    logger.info(f"🔍 Checking links in {abs_path}")

    run_check(
        root_path=abs_path,
        max_workers=max_workers,
        delay=delay,
        timeout=timeout,
        output_file=output,
        blacklist=BLACKLIST + list(blacklist),
        exclude_from=exclude_from,
    )


if __name__ == "__main__":
    cli()
