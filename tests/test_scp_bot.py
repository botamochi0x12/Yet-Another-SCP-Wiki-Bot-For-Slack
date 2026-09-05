import json
from pathlib import Path

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
    monkeypatch.delenv("DISCORD_WEBHOOK_URL", raising=False)
    with pytest.raises(RuntimeError, match="DISCORD_WEBHOOK_URL"):
        _require_env("DISCORD_WEBHOOK_URL")


def test_post_to_discord_sends_content_and_thumbnail(mocker) -> None:  # type: ignore[no-untyped-def]
    mock_post = mocker.patch.object(scp_bot.requests, "post")
    scp_bot.post_to_discord("hello", webhook_url="https://discord.test/webhook/abc")
    args, kwargs = mock_post.call_args
    assert args[0] == "https://discord.test/webhook/abc"
    assert kwargs["json"]["content"] == "hello"
    assert kwargs["json"]["username"] == scp_bot.NAME_OF_BOT
    assert kwargs["json"]["embeds"][0]["thumbnail"]["url"] == scp_bot.SCP_LOGO_URL
    mock_post.return_value.raise_for_status.assert_called_once()


def test_post_to_discord_falls_back_to_module_webhook(mocker) -> None:  # type: ignore[no-untyped-def]
    mock_post = mocker.patch.object(scp_bot.requests, "post")
    mocker.patch.object(scp_bot, "WEBHOOK_URL", "https://discord.test/webhook/xyz")
    scp_bot.post_to_discord("hello")
    assert mock_post.call_args.args[0] == "https://discord.test/webhook/xyz"


def test_post_one_scp_sends_title_and_url(mocker) -> None:  # type: ignore[no-untyped-def]
    mock_discord = mocker.patch.object(scp_bot, "post_to_discord")
    scp_bot.post_one_scp({"path": {"0": "/scp-jp-001"}, "title": {"0": "テスト記事"}})
    text = mock_discord.call_args.args[0]
    assert "テスト記事" in text
    assert "/scp-jp-001" in text
