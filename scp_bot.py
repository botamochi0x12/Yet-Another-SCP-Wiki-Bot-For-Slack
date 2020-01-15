# %%
"""The main part of SCP bot system

Almost half of this code is from https://github.com/naototachibana/memento_mori_bot
"""

import datetime
import json
import random
import time

import requests

import settings


URL_TO_POST = settings.WEBHOOK
NAME_OF_BOT = "SCP-bot"

# NOTE: list of the jp SCPs: http://ja.scp-wiki.net/scp-series-jp
SCP_DOMAIN = "http://ja.scp-wiki.net/"
SCP_LIST_PATH = "scp-series-jp-list.json"


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

def post_to_slack(text, url_to_post=URL_TO_POST, sender=NAME_OF_BOT):
    requests.post(
        url=url_to_post,
        data=json.dumps({
            "text": text,
            "username": sender,
            "icon_emoji": ":python:",
            })
        )

def test_initialization():
    text = "Initialized on {}".format(datetime.datetime.now())
    print(text)
    post_to_slack(text=text, url_to_post=URL_TO_POST, sender=NAME_OF_BOT)

def post_one_scp(scp_list):
    text = ":scp: {url} \n{title}".format(**get_scp_info(scp_list))
    print(text)
    post_to_slack(
        text=text,
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


# %%
