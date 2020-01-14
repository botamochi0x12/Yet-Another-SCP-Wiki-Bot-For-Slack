# %%
"""The main part of SCP bot system

Almost half of this code is from https://github.com/naototachibana/memento_mori_bot
"""

import os
import datetime
import json
import random
import time

import requests

SLACK_API_TOKEN = os.environ['SLACK_API_TOKEN']
CHANNEL_ID = os.environ['CHANNEL_ID']
URL_TO_POST = (
    r"https://slack.com/api/chat.postMessage"
    )
NAME_OF_BOT = "SCP-bot"

# NOTE: list of the jp SCP objects: http://ja.scp-wiki.net/scp-series-jp
SCP_DOMAIN = "http://ja.scp-wiki.net/"
SCP_LIST_PATH = "./resources/scp-series-jp-list.json"


def load_scp_list(filepath=SCP_LIST_PATH):
    with open(filepath, "r") as f:
        scp_list = json.load(f)
    return scp_list

def get_scp_info(scp_list: list, i: int = None):
    if i is None:
        i = random.randint(0, len(scp_list["path"]) - 1)
    id_ = str(i)
    return dict(
        url=SCP_DOMAIN[:-1] + scp_list["path"][id_],
        title=scp_list["title"][id_]
        )

def post_to_slack(
    text_parts,
    url_to_post=URL_TO_POST,
    channel=CHANNEL_ID,
    sender=NAME_OF_BOT
    ):

    if isinstance(text_parts, list):
        key_of_text_parts = "blocks"
    elif isinstance(text_parts, str):
        key_of_text_parts = "text"
    else:
        print("Unknown type of *text_parts*")
        key_of_text_parts = "text"
        text_parts = str(text_parts)

    properties = {
        # Required args
        "channel": channel,

        key_of_text_parts: text_parts,

        # Optionals
        # "as_user": False,
        # "username": sender,
        # "icon_emoji": ":python:",

        # "parse": "full",
        # "unfurl_links": True,
        # "unfurl_media": True,
        }

    # res =
    requests.post(
        url=url_to_post,
        headers={
            "Authorization": "Bearer {token}".format(
                token=SLACK_API_TOKEN,
            )
        },
        json=properties,
        )

    # print(res.status_code, res.content)

def test_initialization():
    text = "Initialized on {}".format(datetime.datetime.now())
    print(text)
    post_to_slack(text_parts=text, url_to_post=URL_TO_POST, sender=NAME_OF_BOT)

def post_one_scp(scp_list):
    text = (
        ":scp: {title} \n{url}"
        + ((
            "\n"
            "Description: {description}"
            ) if False else ""
        )
        ).format(**get_scp_info(scp_list))

    print(text)

    parts = [{
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": text
            },
        "accessory": {
            "type": "image",
            "image_url": (
                "http://scp-wiki.wdfiles.com/"
                "local--files/component%3Atheme/"
                "logo.png"
                ),
            "alt_text": "SCP Foundation Logo"
            }
        }]

    post_to_slack(
        text_parts=parts,
        url_to_post=URL_TO_POST,
        sender=NAME_OF_BOT,
        )

def test_posting():
    post_one_scp(load_scp_list())

def main():
    scp_list = load_scp_list()

    while True:
        post_one_scp(scp_list)

        # Wait 1 day
        waiting_secs = 24*60*60
        time.sleep(waiting_secs)


if __name__ == "__main__":
    # main()
    test_posting()
    # test_initialization()


# %%
