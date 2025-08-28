import click
import logging
import os
from adoc_link_checker.runner import run_check
from adoc_link_checker.config import TIMEOUT, MAX_WORKERS, DELAY, BLACKLIST, OUTPUT_FILE, LOGGING_CONFIG

@click.command()
@click.argument(
    "root_dir",
    type=click.Path(exists=True, file_okay=False),
    default=".",
    required=False,
)
@click.option(
    "--timeout",
    type=int,
    default=TIMEOUT,
    help=f"Timeout for HTTPs requests (seconds). [Default: {TIMEOUT}]",
)
@click.option(
    "--max-workers",
    type=int,
    default=MAX_WORKERS,
    help=f"Maximal number of threads for parallel processing [Default: {MAX_WORKERS}]",
)
@click.option(
    "--delay",
    type=float,
    default=DELAY,
    help=f"Delay between each request (seconds). [Default: {DELAY}]",
)
@click.option(
    "--output",
    type=click.Path(),
    default=OUTPUT_FILE,
    help=f"JSON ouput file for broken links. [Default: {OUTPUT_FILE}]",
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
    help="File with list of links to exclude (a link by line).",
)
@click.option(
    "-v",
    "--verbose",
    count=True,  # Permet de compter le nombre de fois que -v est utilisé
    help="Augmente la verbosité (INFO avec -v, DEBUG avec -vv).",
)
@click.option(
    "--quiet",
    is_flag=True,
    help="Désactive les logs sauf les erreurs (niveau ERROR).",
)
@click.option(
    "--log-file",
    type=click.Path(),
    default=None,
    help="Fichier pour enregistrer les logs (en plus de la console).",
)
@click.version_option(version="1.0.0")
def cli(root_dir, timeout, max_workers, delay, output, blacklist, exclude_from, verbose, quiet, log_file):
    """Check broken links in .adoc files"""
    # Configuration du niveau de log selon la verbosité
    if quiet:
        LOGGING_CONFIG["level"] = logging.ERROR
    elif verbose == 1:  # -v
        LOGGING_CONFIG["level"] = logging.INFO
    elif verbose >= 2:  # -vv ou plus
        LOGGING_CONFIG["level"] = logging.DEBUG
    else:  # Par défaut
        LOGGING_CONFIG["level"] = logging.WARNING
    logging.basicConfig(level=LOGGING_CONFIG["level"], format=LOGGING_CONFIG["format"], force=True)
    logger = logging.getLogger(__name__)
    logger.info(f"🔍 Begin check in {os.path.abspath(root_dir)}")
    run_check(
        root_dir=root_dir,
        max_workers=max_workers,
        delay=delay,
        timeout=timeout,
        output_file=output,
        blacklist=BLACKLIST + list(blacklist),
        exclude_from=exclude_from
    )
    logger.debug(f"Output file : {os.path.abspath(output)}")  # Debug

if __name__ == "__main__":
    cli()
