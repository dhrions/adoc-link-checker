import logging

logger = logging.getLogger(__name__)


def load_excluded_urls(exclude_from: str | None) -> set[str]:
    """
    Load excluded URLs from a file.

    Rules:
    - one URL per line
    - empty lines ignored
    - lines starting with '#' ignored
    - trailing slashes removed
    """
    if not exclude_from:
        return set()

    try:
        with open(exclude_from, "r", encoding="utf-8") as f:
            return {
                line.strip().rstrip("/")
                for line in f
                if line.strip() and not line.strip().startswith("#")
            }
    except Exception as e:
        logger.warning(
            f"Unable to read exclusion file {exclude_from}: {e}"
        )
        return set()
