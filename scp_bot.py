"""The main part of SCP bot system."""

import argparse
import json
import logging
import os
import random
from collections.abc import Callable
from datetime import datetime
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from slack_sdk.web.client import WebClient
from deprecated import deprecated

from wait import wait_until

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
logger = logging.getLogger(__name__)

NAME_OF_BOT: str = "SCP-bot"

# NOTE: list of the jp SCP objects: http://ja.scp-wiki.net/scp-series-jp
SCP_DOMAIN = "http://ja.scp-wiki.net/"
SCP_LIST_PATH = Path(__file__).parent / "resources" / "scp-series-jp-list.json"

SLACK_API_TOKEN: str = ""
CHANNEL_ID: str = ""
POSTING_HOUR: int = 10
CLIENT: Optional[WebClient] = None


def _require_env(name: str) -> str:
    value = os.getenv(name)
    if value is None:
        raise RuntimeError(
            f"Required environment variable {name!r} is not set. "
            "Copy .env.example to .env and fill in the values."
        )
    return value


def _init_from_env() -> None:
    global SLACK_API_TOKEN, CHANNEL_ID, POSTING_HOUR, CLIENT
    load_dotenv()
    SLACK_API_TOKEN = _require_env("SLACK_API_TOKEN")
    CHANNEL_ID = _require_env("CHANNEL_ID")
    POSTING_HOUR = int(os.getenv("POSTING_HOUR", "10"))
    CLIENT = WebClient(token=SLACK_API_TOKEN)


def load_scp_list(filepath: Path | str = SCP_LIST_PATH) -> dict:
    with open(filepath) as f:
        return json.load(f)


def get_scp_info(scp_list: dict, i: Optional[int] = None) -> dict:
    if i is None:
        i = random.randint(0, len(scp_list["path"]) - 1)
    id_ = str(i)
    return dict(
        url=SCP_DOMAIN[:-1] + scp_list["path"][id_],
        title=scp_list["title"][id_],
    )


def post_to_slack(
    text_parts: list | str,
    channel: str = "",
    sender: str = NAME_OF_BOT,
) -> None:
    assert CLIENT is not None, "_init_from_env() must be called first"
    ch = channel or CHANNEL_ID
    if isinstance(text_parts, list):
        CLIENT.chat_postMessage(channel=ch, blocks=text_parts)
    else:
        if not isinstance(text_parts, str):
            logger.warning("Unknown type of text_parts, converting to str")
            text_parts = str(text_parts)
        CLIENT.chat_postMessage(channel=ch, text=text_parts)


@deprecated(reason="This function will be removed in the next release.", version="1.2.0")
def test_initialization() -> None:
    text = f"Initialized on {datetime.now()}"
    logger.info(text)
    post_to_slack(text_parts=text, sender=NAME_OF_BOT)


def post_one_scp(scp_list: dict) -> None:
    info = get_scp_info(scp_list)
    text = f":scp: {info['title']} \n{info['url']}"
    logger.info(text)

    parts = [
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": text},
            "accessory": {
                "type": "image",
                "image_url": (
                    "http://scp-wiki.wdfiles.com/local--files/component%3Atheme/logo.png"
                ),
                "alt_text": "SCP Foundation Logo",
            },
        }
    ]
    post_to_slack(text_parts=parts, sender=NAME_OF_BOT)


@deprecated(reason="Use `post_once` instead. This function will be removed in the next release.", version="1.2.0")
def test_posting() -> None:
    post_one_scp(load_scp_list())


@deprecated(reason="Use `cron` command in a terminal instead. This function will be removed in the next release.", version="1.2.0")
def post_everyday(*, _wait_until: Callable = wait_until) -> None:
    # Referred from: https://github.com/naototachibana/memento_mori_bot
    scp_list = load_scp_list()
    while True:
        post_one_scp(scp_list)
        _wait_until(hour=POSTING_HOUR)


if __name__ == "__main__":
    _init_from_env()

    PARSER = argparse.ArgumentParser()
    PARSER.add_argument("--runforever", action="store_true")
    PARSER.add_argument("--test", action="store_true")
    namespace = PARSER.parse_args()

    if namespace.test:
        test_initialization()
    elif namespace.runforever:
        wait_until(hour=POSTING_HOUR)
        post_everyday()
    else:
        test_posting()
