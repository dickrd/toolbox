#!/bin/env python3
import random

import requests, json


url = "https://www.reddit.com/r/showerthoughts/top.json?sort=top&t=day&limit=50"
headers = {
    "User-Agent": "linux:com.hehehey.toolbox:v1.0 (by /u/DickRD)"
}
chosen = random.randint(0,49)

# noinspection PyBroadException
try:
    r = requests.get(url, headers=headers, timeout=3)
    posts = json.loads(r)
    the_post = posts["data"]["children"][chosen]["data"]

    with open("/tmp/motd.content") as content:
        content.write(the_post["title"])
    with open("/tmp/motd.source") as source:
        source.write("source: reddit.com/r/showerthoughts/{0}".format(the_post["id"]))
except Exception:
    pass
