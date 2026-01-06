import json

from adoc_link_checker.reporting.json import write_report


def test_write_report(tmp_path):
    output = tmp_path / "report.json"

    write_report(str(output), {"file.adoc": []})

    assert output.exists()

    data = json.loads(output.read_text())
    assert "file.adoc" in data
