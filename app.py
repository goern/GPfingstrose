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

import os
import logging

import asyncio

import daiquiri
import daiquiri.formatter

import peony
from peony import PeonyClient

import six

from configuration import Configuration
import tf_connect


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
_LOGGER.setLevel(logging.DEBUG if bool(int(os.getenv("FLT_DEBUG_MODE", "1"))) else logging.INFO)

LOOP = asyncio.get_event_loop()

# create the client using the api keys
CLIENT = PeonyClient(
    consumer_key=Configuration.CONSUMER_KEY,
    consumer_secret=Configuration.CONSUMER_SECRET,
    access_token=Configuration.ACCESS_TOKEN,
    access_token_secret=Configuration.ACCESS_TOKEN_SECRET,
)


async def post_tweet_reply(to_tweet_id, reply_string):
    """ Post a reply to the specified tweet """
    if reply_string:
        post_response = await CLIENT.api.statuses.update.post(
            status=str(reply_string),
            in_reply_to_status_id=to_tweet_id,
            auto_populate_reply_metadata="true",
        )
        _LOGGER.debug("Response: %s", str(post_response))


async def getting_started():
    """This is just a demo of an async API call."""
    user = await CLIENT.user
    _LOGGER.info("I am @%s", user.screen_name)
    return str(user.screen_name)


async def track(bot_name: str):
    """track will open a Stream vom twitter an track the given set of keywords."""
    _LOGGER.info("Please tweet with %s in your post to interact with this bot", bot_name)
    req = CLIENT.stream.statuses.filter.post(track="{0}".format(bot_name))
    async with req as stream:
        async for tweet in stream:
            if peony.events.tweet(tweet):
                user_id = tweet["user"]["id"]
                username = tweet.user.screen_name
                medium_url = None

                # uncomment this if statement, if we want to reply to
                # only base tweets and not tweet replies
                # if not tweet.in_reply_to_status_id:

                # Ignore if it is a retweet     # check for media in the tweet, ignore if no media
                if ("retweeted_status" not in tweet) and ("media" in tweet.entities.keys()):
                    _LOGGER.debug(tweet.entities)
                    for medium in tweet.entities.media:
                        _LOGGER.debug(medium.media_url)
                        medium_url = medium.media_url
                        # ignore if uploaded media is not a photo
                        if medium.type == "photo":

                            try:
                                prediction_values_list = tf_connect.tf_request(
                                    Configuration.TF_SERVER_URL, medium_url
                                )
                                reply_string = tf_connect.process_output(prediction_values_list)
                            except Exception as ex:
                                # requests.exceptions.HTTPError: 400 Client Error:
                                _LOGGER.error("%s: while processing image (%s)", ex, medium_url)
                                reply_string = None

                                # Don't raise when in production, raising will kill the bot
                                if bool(int(os.getenv("FLT_DEBUG_MODE", "1"))):
                                    raise ex
                            break

                    tweet_id = tweet.id
                    content = tweet.text
                    if isinstance(content, six.binary_type):
                        content = content.decode("utf-8")
                    _LOGGER.info(
                        "%s, %s, %s, %s, Tweet Id: %s",
                        username,
                        user_id,
                        medium_url,
                        content,
                        tweet_id,
                    )

                    await post_tweet_reply(tweet_id, reply_string)


if __name__ == "__main__":
    _LOGGER.info("This is ~/S/g/g/Pfingstrose v%s", str(__version__))
    _LOGGER.debug("DEBUG mode is enabled!")

    BOT_NAME = LOOP.run_until_complete(getting_started())

    LOOP = asyncio.get_event_loop()
    LOOP.run_until_complete(track("@{0}".format(BOT_NAME)))
