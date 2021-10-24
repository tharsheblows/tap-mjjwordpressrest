"""MJJWordPressREST tap class."""

import re

from typing import List

from singer_sdk import Tap, Stream
from singer_sdk import typing as th  # JSON schema typing helpers

# Import your custom stream types here:
from tap_mjjwordpressrest.streams import (
    MJJWordPressRESTStream,
    UsersStream,
    CommentsStream,
)
# Compile a list of custom stream types here
#       OR rewrite discover_streams() below with your custom logic.
STREAM_TYPES = [
    UsersStream,
    CommentsStream,
]


class TapMJJWordPressREST(Tap):
    """MJJWordPressREST tap class."""
    name = "tap-mjjwordpressrest"
    avatar_key = "avatar_urls"

    # Update this section with the actual config values you expect:
    config_jsonschema = th.PropertiesList(
        th.Property(
            "api_url",
            th.StringType,
            required=True,
            description="The url for the API service"
        ),
        th.Property(
            "max_pages",
            th.IntegerType,
            default=10,
            description="The maximum number of pages you'd like to get. If you'd like to get them all use a very high number."
        ),
        th.Property(
            "per_page",
            th.IntegerType,
            default=100,
            description="How many entries per page. The WP REST API max is a hard 100."
        ),
        th.Property(
            "start_date",
            th.StringType,
            default='2021-01-23T23:39:33',
            description="Limit response to whatever published after a given ISO8601 compliant date (eg 2021-01-23T23:39:33). Only used for Post objects of any type and Comments."
        ),
    ).to_dict()

    def discover_streams(self) -> List[Stream]:
        """Return a list of discovered streams."""
        return [stream_class(tap=self) for stream_class in STREAM_TYPES]
