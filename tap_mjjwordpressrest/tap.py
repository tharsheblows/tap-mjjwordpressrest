"""MJJWordPressREST tap class."""

import re

from typing import List
from pathlib import Path

from singer_sdk import Tap, Stream

# Import your custom stream types here:
from tap_mjjwordpressrest.streams import (
    PostsStream,
    UsersStream,
    CommentsStream,
)
# Compile a list of custom stream types here
#       OR rewrite discover_streams() below with your custom logic.
STREAM_TYPES = [
    UsersStream,
    CommentsStream,
    PostsStream
]

SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")

class TapMJJWordPressREST(Tap):
    """MJJWordPressREST tap class."""
    name = "tap-mjjwordpressrest"
    avatar_key = "avatar_urls"

    # Update this section with the actual config values you expect:
    config_jsonschema_filepath = SCHEMAS_DIR / "configschema.json"

    def discover_streams(self) -> List[Stream]:
        """Return a list of discovered streams."""
        return [stream_class(tap=self) for stream_class in STREAM_TYPES]
