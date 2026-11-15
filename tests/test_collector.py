import json
import runpy
from pathlib import Path

import pytest

pytest.importorskip("pandas")
pytest.importorskip("bs4")
pytest.importorskip("lxml")
pytest.importorskip("IPython")

COLLECTOR = Path(__file__).resolve().parents[1] / "resources" / "collector.py"


def test_collector_uses_external_directories(tmp_path, monkeypatch, mocker):  # type: ignore[no-untyped-def]
    data = tmp_path / "data"
    scraped = data / "scraped"
    scraped.mkdir(parents=True)
    (scraped / "scp-series.csv").write_text(
        "path,title\n/scp-001,SCP-001\n", encoding="utf-8"
    )
    monkeypatch.setenv("SCP_DATA_DIR", str(data))
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    monkeypatch.chdir(elsewhere)
    response = mocker.patch("requests.get").return_value
    response.content = b"""
        <div class="content-panel standalone series">
          <ul><li>Navigation</li></ul>
          <ul><li><a href="/scp-8000">SCP-8000</a> - Test</li></ul>
        </div>
    """
    runpy.run_path(str(COLLECTOR), run_name="__main__")
    assert Path.cwd() == elsewhere
    assert list(elsewhere.iterdir()) == []
    assert (scraped / "scp-series-9.csv").is_file()
    assert (data / "posting" / "scp-series-list.csv").is_file()
    result = json.loads((data / "posting" / "scp-series-list.json").read_text())
    assert result["path"] == {"0": "/scp-001", "1": "/scp-8000"}
    assert result["title"] == {"0": "SCP-001", "1": "SCP-8000 - Test"}


@pytest.mark.parametrize("value", [None, ""])
def test_collector_requires_data_dir(value, monkeypatch, mocker):  # type: ignore[no-untyped-def]
    monkeypatch.delenv("SCP_DATA_DIR", raising=False)
    if value is not None:
        monkeypatch.setenv("SCP_DATA_DIR", value)
    get = mocker.patch("requests.get")
    with pytest.raises(RuntimeError, match="SCP_DATA_DIR"):
        runpy.run_path(str(COLLECTOR), run_name="__main__")
    get.assert_not_called()
