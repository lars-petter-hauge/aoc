import logging
import os
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

import click
import requests
import yaml
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

logger = logging.getLogger("AoC")

AOC_BASE_URL = "https://adventofcode.com"
SLACK_BASE_URL = "https://hooks.slack.com/services"


def load_config(fname):
    with open(fname) as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)


@dataclass
class AocClient:
    leaderboard: str
    session: str
    year: str

    def get_members(self):
        url = f"{AOC_BASE_URL}/{self.year}/leaderboard/private/view/{self.leaderboard}"
        # Preferably one would want to add "Accept": "application/json"
        # in the header to specify content type, but it does not look
        # like that is possible. Specify type by appending .json to url

        # Author of AoC specifically asked to be personal in the request
        # (i.e. adding contact information to developer), as he could
        # potentially restrict anonymous IPs (likely if they misbehaved).
        response = requests.get(
            f"{url}.json",
            headers={
                "User-Agent": "https://github.com/lars-petter-hauge/aoc",
                "From": "larsenhauge@gmail.com",
            },
            cookies={"session": self.session},
        )
        response.raise_for_status()
        logger.debug(f"Advent of code server response: {response}")

        return response.json()["members"]


@dataclass
class SlackBotClient:
    """Client that can post messages to a slack channel

    User can provide a url specific to the channel given which must also contain a secret
    The format is of T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX and will be prefixed with
    https://hooks.slack.com/services/.

    It is also possible to connect using a token and a channel, where their format are:
    channel: C05002EAE
    token: "xoxb-XXXXXXXX-XXXXXXXX-XXXXX",
    """

    channel: Optional[str] = None
    token: Optional[str] = None
    url: Optional[str] = None
    _slack_client: WebClient = field(init=False)

    def __post_init__(self):
        if self.token is None and self.url is None:
            raise ValueError("Must provide either token or url")
        if self.token is not None and self.channel is None:
            raise ValueError("Must provide channel id if token is used")
        if self.token is not None and self.url is not None:
            raise ValueError("Either provide token or url")

        self._slack_client = None
        if self.token:
            self._slack_client = WebClient(self.token)

    def post(self, content):
        if self._slack_client is not None:
            try:
                result = self._slack_client.chat_postMessage(
                    channel=self.channel, attachments=[content], text=content["text"]
                )
                logger.debug(result)

            except SlackApiError as e:
                logger.error(f"Error posting message: {e}")
        else:
            response = requests.post(url=f"{SLACK_BASE_URL}/{self.url}", json=content)
            response.raise_for_status()
            logger.debug(f"Slack bot response: {response}")


class LeaderBoard:
    def __init__(self, content=None):
        self._content = content

    def update_board(self, content):
        if self._content is None:
            self._content = content
            return {}
        diff = self._diff_content(content)
        self._content = content
        return diff

    def _diff_content(self, new_content):
        new_entries = {}
        for id, data in new_content.items():
            last_progress = self._content[id]  # Could be new user
            user_name = last_progress["name"]
            if data["last_star_ts"] == last_progress["last_star_ts"]:
                continue
            days = list(data["completion_day_level"].keys())
            for day in days:
                if day not in last_progress["completion_day_level"]:
                    for star in data["completion_day_level"][day]:
                        new_entries[
                            datetime.fromtimestamp(
                                data["completion_day_level"][day][star]["get_star_ts"]
                            )
                        ] = {"name": user_name, "day": day, "star": star}
                    continue
                for star in data["completion_day_level"][day]:
                    if star not in last_progress["completion_day_level"][day]:
                        new_entries[
                            datetime.fromtimestamp(
                                data["completion_day_level"][day][star]["get_star_ts"]
                            )
                        ] = {"name": user_name, "day": day, "star": star}

        return new_entries


def format_slack_message(content):
    timestamp, data = content
    msg = f":christmas_tree: At {str(timestamp)}, *{data['name']}* gained {''.join([':star:']*int(data['star']))} for day *{data['day']}* :christmas_tree:"
    return {"text": msg}


def monitor_and_post(aoc_client, slack_client, update_interval=60 * 5):
    logger.debug("Retrieving members")
    members = aoc_client.get_members()
    leader_board = LeaderBoard(members)

    while True:
        logger.info("Retrieving info from AoC...")
        members = aoc_client.get_members()
        logger.info("Info retrieved")

        update_since_last = leader_board.update_board(members)
        if update_since_last:
            update_since_last = dict(sorted(update_since_last.items()))
            logger.info(
                f"{len(update_since_last)} updates received - Posting info to slack..."
            )
            for update in dict(sorted(update_since_last.items())).items():
                logger.debug(f"Posting the following update {update}")
                slack_client.post(format_slack_message(update))
                time.sleep(0.3)
            logger.info("Info posted")
        else:
            logger.info("No new progress")

        time.sleep(update_interval)


def setup_logger(verbosity):
    if verbosity == 0:
        level = logging.WARNING
    elif verbosity == 1:
        level = logging.INFO
    elif verbosity >= 2:
        level = logging.DEBUG

    handler = logging.StreamHandler(sys.stdout)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    handler.setLevel(level)
    logger.setLevel(level)


def retrieve_value(config, name, err_msg=None, exit_on_failure=False):
    value = os.environ.get(name)
    if value is None:
        value = config.get(name)
    if value is None and exit_on_failure:
        sys.exit(err_msg)
    return value


@click.command()
@click.option("--config_file", required=True, help="File path to config file")
@click.option("--year", required=True, help="The year the leaderboard will be tracked")
@click.option(
    "-v",
    "--verbose",
    help="Sets the logger level. Default is warning. Adding multiple flags increases verbosity. I.e -v=info, -vv=debug",
    count=True,
)
def aoc_tracker(config_file, year, verbose):
    """Advent of Code leaderboard tracker

    Allows for tracking a leaderboard and posting to a slack bot"""
    setup_logger(verbose)
    logger.info("Initiating Advent of Code Leaderboard Tracker")
    config = load_config(config_file)

    session = retrieve_value(
        config,
        "AOC_SESSION",
        "The AOC session must be provided. Please set AOC_SESSION either as environment variable, or in config file, and try again",
        exit_on_failure=True,
    )
    aoc_client = AocClient(
        leaderboard=config["LEADER_BOARD"],
        session=session,
        year=year,
    )

    slack_token = retrieve_value(
        config,
        "SLACK_TOKEN",
    )
    slack_channel_id = retrieve_value(
        config,
        "SLACK_CHANNEL",
    )
    slack_client = None
    if slack_token is not None:
        if slack_channel_id is None:
            sys.exit(
                "Slack token provided, but did not find channel. Please provide SLACK_CHANNEL in config or as an environment variable"
            )
        slack_client = SlackBotClient(token=slack_token, channel=slack_channel_id)
    else:
        logger.info("Slack token not provided, falling back on SLACK_BOT_ENTRY")
        slack_bot_url = retrieve_value(
            config,
            "SLACK_BOT_ENTRY",
            "The slack bot url must be provided. Please set SLACK_BOT_ENTRY either as environment variable, or in config file, and try again",
            exit_on_failure=True,
        )
        slack_client = SlackBotClient(url=slack_bot_url)

    slack_client.post(
        {
            "text": " :christmas_tree: Hello, I am an Advent of Code leaderboard tracker - I'll be keeping you lot up to date :christmas_tree:",
            "type": "mrkdwn",
        }
    )

    try:
        monitor_and_post(aoc_client, slack_client)
    except KeyboardInterrupt:
        sys.exit("Advent of Code tracker completed")


if __name__ == "__main__":
    aoc_tracker()
