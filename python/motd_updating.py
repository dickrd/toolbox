#!/bin/env python3
import random, requests


url = "https://www.reddit.com/r/showerthoughts/top.json?sort=top&t=day&limit=50"
headers = {
    "User-Agent": "linux:com.hehehey.toolbox:v1.0 (by /u/DickRD)"
}
chosen = random.randint(0,49)

# noinspection PyBroadException
try:
    r = requests.get(url, headers=headers, timeout=3)
    posts = r.json()
    the_post = posts["data"]["children"][chosen]["data"]

    with open("/tmp/motd.content", 'w') as content:
        content.write("{0}\n".format(the_post["title"]))
    with open("/tmp/motd.source", 'w') as source:
        source.write("source: reddit.com/r/showerthoughts/{0}\n".format(the_post["id"]))
except Exception as e:
    print("Update failed: {0}".format(repr(e)))
