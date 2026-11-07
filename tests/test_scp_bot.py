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


ENV_NAMES = ("SLACK_API_TOKEN", "CHANNEL_ID", "DISCORD_WEBHOOK_URL")
SCP_LIST = {"path": {"0": "/scp-jp-001"}, "title": {"0": "テスト記事"}}


@pytest.fixture
def env(monkeypatch: pytest.MonkeyPatch):  # type: ignore[no-untyped-def]
    monkeypatch.setattr(scp_bot, "load_dotenv", lambda: None)
    for name in ENV_NAMES:
        monkeypatch.delenv(name, raising=False)
    return monkeypatch


def test_init_from_env_raises_without_any_destination(env) -> None:  # type: ignore[no-untyped-def]
    with pytest.raises(RuntimeError, match="DISCORD_WEBHOOK_URL"):
        scp_bot._init_from_env()


def test_init_from_env_raises_with_only_one_slack_variable(env) -> None:  # type: ignore[no-untyped-def]
    env.setenv("SLACK_API_TOKEN", "xoxb-test")
    env.setenv("DISCORD_WEBHOOK_URL", "https://discord.test/webhook/abc")
    with pytest.raises(RuntimeError, match="CHANNEL_ID"):
        scp_bot._init_from_env()


def test_init_from_env_accepts_discord_only(env) -> None:  # type: ignore[no-untyped-def]
    env.setenv("DISCORD_WEBHOOK_URL", "https://discord.test/webhook/abc")
    scp_bot._init_from_env()
    assert scp_bot.DISCORD_WEBHOOK_URL == "https://discord.test/webhook/abc"
    assert scp_bot.CLIENT is None


def test_post_to_discord_sends_content_and_thumbnail(mocker) -> None:  # type: ignore[no-untyped-def]
    mock_post = mocker.patch.object(scp_bot.requests, "post")
    scp_bot.post_to_discord("hello", webhook_url="https://discord.test/webhook/abc")
    args, kwargs = mock_post.call_args
    assert args[0] == "https://discord.test/webhook/abc"
    assert kwargs["json"]["content"] == "hello"
    assert kwargs["json"]["username"] == scp_bot.NAME_OF_BOT
    assert kwargs["json"]["embeds"][0]["thumbnail"]["url"] == scp_bot.SCP_LOGO_URL
    assert kwargs["timeout"] == 30
    mock_post.return_value.raise_for_status.assert_called_once()


def test_post_one_scp_posts_to_both_destinations(env, mocker) -> None:  # type: ignore[no-untyped-def]
    env.setenv("SLACK_API_TOKEN", "xoxb-test")
    env.setenv("CHANNEL_ID", "C123")
    env.setenv("DISCORD_WEBHOOK_URL", "https://discord.test/webhook/abc")
    scp_bot._init_from_env()
    mock_slack = mocker.patch.object(scp_bot, "post_to_slack")
    mock_discord = mocker.patch.object(scp_bot, "post_to_discord")
    scp_bot.post_one_scp(SCP_LIST)
    mock_slack.assert_called_once()
    assert "テスト記事" in mock_discord.call_args.args[0]


def test_post_one_scp_skips_slack_when_discord_only(env, mocker) -> None:  # type: ignore[no-untyped-def]
    env.setenv("DISCORD_WEBHOOK_URL", "https://discord.test/webhook/abc")
    scp_bot._init_from_env()
    mock_slack = mocker.patch.object(scp_bot, "post_to_slack")
    mock_discord = mocker.patch.object(scp_bot, "post_to_discord")
    scp_bot.post_one_scp(SCP_LIST)
    mock_slack.assert_not_called()
    mock_discord.assert_called_once()


def test_post_one_scp_skips_discord_when_slack_only(env, mocker) -> None:  # type: ignore[no-untyped-def]
    env.setenv("SLACK_API_TOKEN", "xoxb-test")
    env.setenv("CHANNEL_ID", "C123")
    scp_bot._init_from_env()
    mock_slack = mocker.patch.object(scp_bot, "post_to_slack")
    mock_discord = mocker.patch.object(scp_bot, "post_to_discord")
    scp_bot.post_one_scp(SCP_LIST)
    mock_slack.assert_called_once()
    mock_discord.assert_not_called()
