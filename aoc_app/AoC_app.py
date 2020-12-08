import requests
import urllib, json
import urllib.request
from flask import Flask

app = Flask(__name__)
from datetime import datetime

LEADERBOARD_URL = "https://adventofcode.com/2018/leaderboard/private/view/206422"
SESSION_ID = ""


@app.route("/")
def hello():
    return "Hello World!"


def parseMembers(members_json):
    overview = []
    for m in members_json.values():
        for d, val in m["completion_day_level"].items():
            if "1" in val:
                overview.append((m["name"], d, "1", int(val["1"]["get_star_ts"])))
            if "2" in val:
                overview.append((m["name"], d, "2", int(val["2"]["get_star_ts"])))

    # sort members by time, decending
    overview.sort(key=lambda s: (-s[3]))

    overview = [(n, d, p, datetime.fromtimestamp(ts)) for n, d, p, ts in overview]
    return overview


def leaderboard():
    # retrieve leaderboard
    r = requests.get("{}.json".format(LEADERBOARD_URL), cookies={"session": SESSION_ID})
    if r.status_code != requests.codes.ok:
        print("Error retrieving leaderboard")
        exit(1)
    # get members from json
    members = parseMembers(r.json()["members"])

    # generate message to send to slack
    message = formatLeaderMessage(members)

    overview = parseMembers2(r.json()["members"])

    print(message)


if __name__ == "__main__":
    leaderboard()
    # app.run()
