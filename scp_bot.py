"""The main part of SCP bot system."""

import argparse
import json
import logging
import os
import random
from collections.abc import Callable
from datetime import datetime
from pathlib import Path

import requests
from deprecated import deprecated
from dotenv import load_dotenv

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
SCP_LOGO_URL = "http://scp-wiki.wdfiles.com/local--files/component%3Atheme/logo.png"

WEBHOOK_URL: str = ""
POSTING_HOUR: int = 10


def _require_env(name: str) -> str:
    value = os.getenv(name)
    if value is None:
        raise RuntimeError(
            f"Required environment variable {name!r} is not set. "
            "Copy .env.example to .env and fill in the values."
        )
    return value


def _init_from_env() -> None:
    global WEBHOOK_URL, POSTING_HOUR
    load_dotenv()
    WEBHOOK_URL = _require_env("DISCORD_WEBHOOK_URL")
    POSTING_HOUR = int(os.getenv("POSTING_HOUR", "10"))


def load_scp_list(filepath: Path | str = SCP_LIST_PATH) -> dict:
    with open(filepath) as f:
        return json.load(f)


def get_scp_info(scp_list: dict, i: int | None = None) -> dict:
    if i is None:
        i = random.randint(0, len(scp_list["path"]) - 1)
    id_ = str(i)
    return dict(
        url=SCP_DOMAIN[:-1] + scp_list["path"][id_],
        title=scp_list["title"][id_],
    )


def post_to_discord(
    text: str,
    webhook_url: str = "",
    sender: str = NAME_OF_BOT,
    logo_url: str = SCP_LOGO_URL,
) -> None:
    url = webhook_url or WEBHOOK_URL
    assert url, "_init_from_env() must be called first"
    response = requests.post(
        url,
        json={
            "content": text,
            "username": sender,
            "embeds": [{"thumbnail": {"url": logo_url}}],
        },
        timeout=30,
    )
    response.raise_for_status()


@deprecated(
    reason="This function will be removed in the next release.", version="1.2.0"
)
def test_initialization() -> None:
    text = f"Initialized on {datetime.now()}"
    logger.info(text)
    post_to_discord(text)


def post_one_scp(scp_list: dict) -> None:
    info = get_scp_info(scp_list)
    text = f"**{info['title']}**\n{info['url']}"
    logger.info(text)
    post_to_discord(text)


@deprecated(
    reason="Use `post_once` instead.\n"
    + "This function will be removed in the next release.",
    version="1.2.0",
)
def test_posting() -> None:
    post_one_scp(load_scp_list())


@deprecated(
    reason="Use `cron` command in a terminal instead.\n"
    + "This function will be removed in the next release.",
    version="1.2.0",
)
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
