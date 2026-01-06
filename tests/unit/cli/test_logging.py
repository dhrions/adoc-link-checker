from adoc_link_checker.cli.config import build_check_config
from adoc_link_checker.config import BLACKLIST


def test_build_check_config_merges_blacklist():
    config = build_check_config(
        timeout=10,
        max_workers=5,
        delay=0.1,
        blacklist=("example.com", "test.com"),
    )

    for domain in BLACKLIST:
        assert domain in config.blacklist

    assert "example.com" in config.blacklist
    assert "test.com" in config.blacklist


def test_build_check_config_removes_duplicates():
    config = build_check_config(
        timeout=10,
        max_workers=5,
        delay=0.1,
        blacklist=("example.com", "example.com"),
    )

    assert config.blacklist.count("example.com") == 1


def test_build_check_config_preserves_order():
    config = build_check_config(
        timeout=10,
        max_workers=5,
        delay=0.1,
        blacklist=("b.com", "a.com"),
    )

    expected = []
    for domain in BLACKLIST:
        if domain not in expected:
            expected.append(domain)

    expected.extend(["b.com", "a.com"])

    assert config.blacklist == expected
