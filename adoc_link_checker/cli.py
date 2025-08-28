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
    help=f"Timeout pour les requêtes HTTP (secondes). [Default: {TIMEOUT}]",
)
@click.option(
    "--max-workers",
    type=int,
    default=MAX_WORKERS,
    help=f"Nombre maximal de threads pour le traitement parallèle. [Default: {MAX_WORKERS}]",
)
@click.option(
    "--delay",
    type=float,
    default=DELAY,
    help=f"Délai entre chaque requête (secondes). [Default: {DELAY}]",
)
@click.option(
    "--output",
    type=click.Path(),
    default=OUTPUT_FILE,
    help=f"Fichier de sortie JSON pour les liens brisés. [Default: {OUTPUT_FILE}]",
)
@click.option(
    "--blacklist",
    type=str,
    multiple=True,
    default=[],
    help="Domaine à ignorer (peut être spécifié plusieurs fois).",
)
@click.option(
    "--verbose",
    is_flag=True,
    help="Active le mode verbeux (DEBUG).",
)
@click.option(
    "--exclude-from",
    type=click.Path(exists=True, dir_okay=False),
    default=None,
    help="Fichier contenant la liste des liens à exclure (un lien par ligne).",
)
@click.version_option(version="1.0.0")
def cli(root_dir, timeout, max_workers, delay, output, blacklist, verbose, exclude_from):
    """Vérifie les liens brisés dans les fichiers .adoc du répertoire ROOT_DIR."""
    if verbose:
        LOGGING_CONFIG["level"] = logging.DEBUG
    logging.basicConfig(level=LOGGING_CONFIG["level"], format=LOGGING_CONFIG["format"], force=True)
    logger = logging.getLogger(__name__)
    logger.info(f"🔍 Démarrage de la vérification dans {os.path.abspath(root_dir)}")
    run_check(
        root_dir=root_dir,
        max_workers=max_workers,
        delay=delay,
        timeout=timeout,
        output_file=output,
        blacklist=BLACKLIST + list(blacklist),
        exclude_from=exclude_from
    )
    logger.debug(f"Fichier de sortie : {os.path.abspath(output)}")  # Debug

if __name__ == "__main__":
    cli()
