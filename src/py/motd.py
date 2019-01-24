#!/bin/env python
# coding=utf-8
import os, random, requests

FISH = "/home/dickzhou/.config/fish"

headers = {
    "User-Agent": "linux:com.hehehey.toolbox:v1.1 (by /u/DickRD)"
}
url = "https://api.hehehey.com/r/showerthoughts/top.json?sort=top&t=day&limit=50"
chosen = random.randint(0,49)

# noinspection PyBroadException
try:
    r = requests.get(url, headers=headers, timeout=3)
    posts = r.json()
    the_post = posts["data"]["children"][chosen]["data"]

    with open(os.path.join(FISH, "motd.content"), 'wb') as content:
        content.write(the_post["title"].encode("utf-8"))
    with open(os.path.join(FISH, "motd.source"), 'w') as source:
        source.write("source: reddit.com/r/showerthoughts/comments/{0}\n".format(the_post["id"]))
except Exception as e:
    print("update error: {0}".format(repr(e)))
    exit(1)
