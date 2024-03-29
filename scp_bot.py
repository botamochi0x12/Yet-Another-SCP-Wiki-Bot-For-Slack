# %%
"""The main part of SCP bot system.
"""

import argparse
import json
import random
import sys
import typing
from datetime import datetime
from os import getenv as _getenv
from os import environ as _environ

from slack_sdk.web.client import WebClient

from wait import wait_until

SLACK_API_TOKEN: str = _environ["SLACK_API_TOKEN"]
CHANNEL_ID: str = _environ["CHANNEL_ID"]
POSTING_HOUR: int = int(_getenv("POSTING_HOUR", 10))
NAME_OF_BOT: str = "SCP-bot"

CLIENT = WebClient(token=SLACK_API_TOKEN)

# NOTE: list of the jp SCP objects: http://ja.scp-wiki.net/scp-series-jp
SCP_DOMAIN = "http://ja.scp-wiki.net/"
SCP_LIST_PATH = "./resources/scp-series-jp-list.json"


def load_scp_list(filepath=SCP_LIST_PATH):
    with open(filepath, "r") as f:
        scp_list = json.load(f)
    return scp_list


def get_scp_info(scp_list: dict, i: typing.Optional[int] = None):
    if i is None:
        i = random.randint(0, len(scp_list["path"]) - 1)
    id_ = str(i)
    return dict(url=SCP_DOMAIN[:-1] + scp_list["path"][id_],
                title=scp_list["title"][id_])


def post_to_slack(text_parts, channel=CHANNEL_ID, sender=NAME_OF_BOT):

    if isinstance(text_parts, list):
        key_of_text_parts = "blocks"
    elif isinstance(text_parts, str):
        key_of_text_parts = "text"
    else:
        print("Unknown type of *text_parts*", file=sys.stderr)
        key_of_text_parts = "text"
        text_parts = str(text_parts)

    CLIENT.chat_postMessage(channel=channel, **{key_of_text_parts: text_parts})


def test_initialization():
    text = "Initialized on {}".format(datetime.now())
    print(text)
    post_to_slack(text_parts=text, sender=NAME_OF_BOT)


def post_one_scp(scp_list):
    text = (":scp: {title} \n{url}" +
            (("\n"
              "Description: {description}") if False else "")).format(
                  **get_scp_info(scp_list))

    print(text)

    parts = [{
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": text
        },
        "accessory": {
            "type":
            "image",
            "image_url": ("http://scp-wiki.wdfiles.com/"
                          "local--files/component%3Atheme/"
                          "logo.png"),
            "alt_text":
            "SCP Foundation Logo"
        }
    }]

    post_to_slack(
        text_parts=parts,
        sender=NAME_OF_BOT,
    )


def test_posting():
    post_one_scp(load_scp_list())


def post_everyday(
    *,
    _wait_until=wait_until,
):
    # Referred from: https://github.com/naototachibana/memento_mori_bot

    scp_list = load_scp_list()

    while True:
        post_one_scp(scp_list)

        # Wait for 1 day
        _wait_until(hour=POSTING_HOUR)

if __name__ == "__main__":
    # %%
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument("--runforever", action="store_true")
    PARSER.add_argument("--test", action="store_true")
    namespace = PARSER.parse_args()

    # %%
    if namespace.test:
        test_initialization()
    elif namespace.runforever:
        wait_until(hour=POSTING_HOUR)
        post_everyday()
    else:
        test_posting()

# %%
