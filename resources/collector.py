# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% Change working directory from the workspace root to the ipynb file location. Turn this addition off with the DataScience.changeDirOnImportExport setting
# ms-python.python added
import os
try:
	os.chdir(os.path.join(os.getcwd(), 'resources'))
	print(os.getcwd())
except:
	pass

# %%
import os.path
import re
import requests
import bs4 as bs
from bs4 import BeautifulSoup
import pandas as pd


# %%
pagepaths = {"en": r"scp-series", "jp": r"scp-series-jp"}
pagepath = pagepaths["en"] + r"-5"
domains = {"en": r"http://scp-wiki.net/", "jp": r"http://ja.scp-wiki.net/"}
domain = domains["en"]


# %%
response = requests.get(domain + pagepath)
soup = BeautifulSoup(response.content, "lxml")
# NOTE: "lxml" is faster than "html.parser"


# %%
l = []
patterns = {"en": r"\[ACCESS DENIED\]", "jp": r"\[アクセス拒否\]"}
empty_pattern = re.compile(patterns["en"])  # empty pages
title_pattern = re.compile(r"SCP-\d+" + ("" if "en" == "en" else "-jp"))
for ul in soup.select_one("div.content-panel.standalone.series").find_all("ul")[1:]:
    for item in ul.find_all("li"):
        if item.a is None: continue
        path = item.a.get("href")
        title = (item.text)
        if empty_pattern.search(title): continue
        id_ = item.a.text
        if item.ul:
            title = id_ + " - " + item.ul.get_text(strip=True)
        m = {"path": path, "title": title}
        # print(m)
        l.append(m)
df = pd.DataFrame(l)
display(df)


# %%
df.to_csv(pagepath + r".csv", index=False)


# %%
pagebasepath = "scp-series-jp"
p = re.compile(pagebasepath+r"(|-\d).csv")
filenames = [item for item in os.listdir() if p.match(item)]
filenames = [filenames[-1]] + filenames[:-1]
print(filenames)
df = pd.DataFrame()
for filename in filenames:
    df = pd.concat([df, pd.read_csv(filename)[["path", "title"]]], axis=0, join="outer", ignore_index=True)
# (pd.concat([pd.read_csv(r"scp-series.csv"), pd.read_csv(r"scp-series-jp.csv")], axis=0, join="outer")[["path", "title"]])
# df.to_csv("scp-series-jp-list.csv", index=False, quotechar="'")


# %%
display(df)
if True or input("Are sure to save this into a csv file? (yes/no) > ") == "yes":
    df.to_csv(pagebasepath + "-list.csv", index=False)
    print("Saving to csv was successed!")


# %%
# pagebasepath = "scp-series"
# df = pd.read_csv(pagebasepath + "-list.csv")
if True or input("Are sure to save this into a json file? (yes/no) > ") == "yes":
    df.to_json(pagebasepath + "-list.json")
    print("Saving to json was successed!")


# %%



