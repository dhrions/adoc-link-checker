# tests/test_main.py
import pytest
from adoc_link_checker.main import is_valid_url, normalize_url, extract_links_from_file
import os
import tempfile

@pytest.mark.parametrize(
    "url, expected",
    [
        # URLs valides
        ("https://example.com", True),
        ("http://example.com/path?query=value", True),
        ("https://sub.example.com:8080/path#section", True),
        # URLs invalides
        ("ftp://example.com", False),  # Scheme non supporté
        ("example.com", False),         # Pas de scheme
        ("", False),                    # Chaîne vide
        ("javascript:alert(1)", False), # Scheme dangereux
        ("mailto:test@example.com", False),  # Scheme non supporté
    ],
)
def test_is_valid_url(url, expected):
    """Teste si une URL est valide selon les critères de la fonction."""
    assert is_valid_url(url) == expected

@pytest.mark.parametrize(
    "url, expected",
    [
        ("https://example.com/path?query=value#section", "https://example.com/path"),
        ("https://example.com/", "https://example.com"),
        ("https://example.com//", "https://example.com"),
        ('"https://example.com"', "https://example.com"),
        ("<https://example.com>", "https://example.com"),
        ("https://example.com/path/#", "https://example.com/path"),
    ],
)
def test_normalize_url(url, expected):
    """Teste la normalisation des URLs."""
    assert normalize_url(url) == expected

def test_extract_links_from_file():
    """Teste l'extraction des liens depuis un fichier .adoc."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.adoc', delete=False, encoding='utf-8') as f:
        f.write("""
= Page de test
link:https://example.com[Exemple]
link:https://another.example.com/path[Autre lien]
video::dQw4w9WgXcQ
""")
        f.flush()
        file_path = f.name

    try:
        links = extract_links_from_file(file_path)
        print("Liens extraits :", links)  # Ajout pour débogage
        assert links == {
            "https://example.com",
            "https://another.example.com/path",
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        }
    finally:
        os.unlink(file_path)
