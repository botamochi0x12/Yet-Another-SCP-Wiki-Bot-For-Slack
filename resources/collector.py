# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% Data checkout, independent of the application's Git history.
import os
from pathlib import Path

data_dir = os.getenv("SCP_DATA_DIR")
if not data_dir:
    raise RuntimeError("Set SCP_DATA_DIR to the external SCP data checkout.")
scraped_dir = Path(data_dir).expanduser() / "scraped"
posting_dir = Path(data_dir).expanduser() / "posting"
scraped_dir.mkdir(parents=True, exist_ok=True)
posting_dir.mkdir(parents=True, exist_ok=True)

# %%
import re

import pandas as pd
import requests
from bs4 import BeautifulSoup
from IPython.display import display

# %%
pagepaths = {"en": r"scp-series", "jp": r"scp-series-jp"}
pagepath = pagepaths["en"] + r"-9"
domains = {"en": r"http://scp-wiki.net/", "jp": r"http://ja.scp-wiki.net/"}
domain = domains["en"]


# %%
response = requests.get(domain + pagepath)
soup = BeautifulSoup(response.content, "lxml")
# NOTE: "lxml" is faster than "html.parser"


# %%
patterns = {"en": r"\[ACCESS DENIED\]", "jp": r"\[アクセス拒否\]"}
empty_pattern = patterns["en"]

l = []
scp_article_container = soup.select_one("div.content-panel.standalone.series")
if scp_article_container is None:
    raise RuntimeError("No SCP Objects found.")
for ul in scp_article_container.find_all("ul")[1:]:
    for item in ul.find_all("li"):
        if item.a is None:
            continue
        title = item.text
        if empty_pattern in title:
            continue
        if item.ul:
            id_ = item.a.text
            title = id_ + " - " + item.ul.get_text(strip=True)
        path = item.a.get("href")
        m = {"path": path, "title": title}
        # print(m)
        l.append(m)

df = pd.DataFrame(l)
display(df)


# %%
df.to_csv(scraped_dir / (pagepath + r".csv"), index=False)


# %%
pagebasepath = "scp-series" + ("" if "en" == "en" else "-jp")
p = re.compile(pagebasepath + r"-\d+?.csv")
filenames = [scraped_dir / (pagebasepath + r".csv")] + [
    item for item in scraped_dir.iterdir() if p.match(item.name)
]
print(filenames)
df = pd.DataFrame()
for filename in filenames:
    df = pd.concat(
        [df, pd.read_csv(filename)[["path", "title"]]],
        axis=0,
        join="outer",
        ignore_index=True,
    )


# %%
display(df)

if (
    False
    and input(
        "Are sure to save the above data into"
        "a pair of csv and json files? (yes/no) > "
    )
    != "yes"
):
    raise RuntimeError("Not saving to csv and json files.")

df.to_csv(posting_dir / (pagebasepath + "-list.csv"), index=False)
print("Saving to csv has done!")

df.to_json(posting_dir / (pagebasepath + "-list.json"))
print("Saving to json has done!")
