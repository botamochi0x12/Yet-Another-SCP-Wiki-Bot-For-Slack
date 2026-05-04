import json
from pathlib import Path
from unittest.mock import MagicMock

import pytest

import scp_bot
from scp_bot import _require_env, get_scp_info, load_scp_list


def test_load_scp_list_uses_pathlib(tmp_path: Path) -> None:
    data = {"path": {"0": "/scp-jp-001"}, "title": {"0": "SCP-JP-001"}}
    f = tmp_path / "test_list.json"
    f.write_text(json.dumps(data))
    result = load_scp_list(filepath=f)
    assert result["path"]["0"] == "/scp-jp-001"


def test_get_scp_info_returns_url_and_title() -> None:
    scp_list = {"path": {"0": "/scp-jp-001"}, "title": {"0": "Test Article"}}
    info = get_scp_info(scp_list, i=0)
    assert "url" in info
    assert "title" in info
    assert info["title"] == "Test Article"
    assert info["url"].endswith("/scp-jp-001")


def test_require_env_raises_on_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("SLACK_API_TOKEN", raising=False)
    with pytest.raises(RuntimeError, match="SLACK_API_TOKEN"):
        _require_env("SLACK_API_TOKEN")


def test_post_to_slack_calls_client(mocker) -> None:  # type: ignore[no-untyped-def]
    mock_client = MagicMock()
    mocker.patch.object(scp_bot, "CLIENT", mock_client)
    mocker.patch.object(scp_bot, "CHANNEL_ID", "C123")
    scp_bot.post_to_slack("hello", channel="C123")
    mock_client.chat_postMessage.assert_called_once()
