#!/usr/bin/env python3
# ~/S/g/g/Pfingstrose
# Copyright(C) 2019 Christoph Görn
#
# This program is free software: you can redistribute it and / or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""~/S/g/g/Pfingstrose is an async twitter bot talking to some AI."""

import typing

import os
import sys
import logging

import asyncio

import daiquiri
import daiquiri.formatter

import peony
from peony import PeonyClient

from configuration import Configuration


__version__ = "0.1.0"


daiquiri.setup(
    level=logging.INFO,
    outputs=(
        daiquiri.output.Stream(
            formatter=daiquiri.formatter.ColorFormatter(
                fmt="%(asctime)s [%(process)d] %(color)s%(levelname)-8.8s %(name)s:"
                "%(lineno)d: %(message)s%(color_stop)s"
            )
        ),
    ),
)

_LOGGER = logging.getLogger("gpfingstrose")
_LOGGER.setLevel(logging.DEBUG if bool(int(os.getenv("DEBUG", 0))) else logging.INFO)


loop = asyncio.get_event_loop()

# create the client using the api keys
client = PeonyClient(
    consumer_key=Configuration.CONSUMER_KEY,
    consumer_secret=Configuration.CONSUMER_SECRET,
    access_token=Configuration.ACCESS_TOKEN,
    access_token_secret=Configuration.ACCESS_TOKEN_SECRET,
)


async def getting_started():
    """This is just a demo of an async API call."""
    user = await client.user
    _LOGGER.info("I am @%s" % user.screen_name)


async def track(keywords: typing.Set[str]):
    """track will open a Stream vom twitter an track the given set of keywords."""
    req = client.stream.statuses.filter.post(track=",".join(keywords))

    async with req as stream:
        async for tweet in stream:
            if peony.events.tweet(tweet):
                user_id = tweet["user"]["id"]
                username = tweet.user.screen_name
                medium_url = None

                if "media" in tweet.entities.keys():
                    _LOGGER.debug(tweet.entities)

                    for medium in tweet.entities.media:
                        _LOGGER.debug(medium.media_url)
                        medium_url = medium.media_url

                _LOGGER.info(f"{username}, {user_id}, {medium_url}, {tweet.text}")


# TODO create a class for handling a stream
# TODO handle stream disruptions like disconnect

if __name__ == "__main__":
    _LOGGER.info(f"This is ~/S/g/g/Pfingstrose v{__version__}")
    _LOGGER.debug("DEBUG mode is enabled!")

    loop.run_until_complete(getting_started())

    loop = asyncio.get_event_loop()
    loop.run_until_complete(track(["redhat", "red hat", "rhat", "fedora"]))
