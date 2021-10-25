"""Stream type classes for tap-mjjwordpressrest."""

from pathlib import Path
from typing import Any, Dict, Optional, Union, List, Iterable

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_mjjwordpressrest.client import MJJWordPressRESTStream

SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")

class UsersStream(MJJWordPressRESTStream):
    """The users stream."""
    name = "users"
    path = "/users"
    primary_keys = ["user_id"]
    replication_key = "id"
    avatar_key = "avatar_urls"
    can_use_start = False

    # TODO: make sure we can get all the users if needed. maybe a "get_all" config param? with a list of all the things you want to get all of.

    schema_filepath = SCHEMAS_DIR / "users.json"

    def post_process(self, row: dict, context: Optional[dict]) -> dict:
        """As needed, append or transform raw data to match expected structure."""

        g = self.get_email_hash(row)

        user = {
            "user_id": row['id'],
            "display_name": row['name'],
            "username": row['slug'],
            "email_hash": g
        }

        return user


class CommentsStream(MJJWordPressRESTStream):
    """The comments stream."""
    name = "comments"
    path = "/comments"
    primary_keys = ["comment_id"]
    replication_key = "date"
    avatar_key = "author_avatar_urls"
    can_use_start = True

    schema_filepath = SCHEMAS_DIR / "comments.json"

    def post_process(self, row: dict, context: Optional[dict]) -> dict:
        """As needed, append or transform raw data to match expected structure."""

        g = self.get_email_hash(row)

        comment = {
            "comment_id": row['id'],
            "commenter_id": row['author'],
            "commenter_name": row['author_name'],
            "commenter_url": row['author_url'],
            "date": row['date_gmt'],
            "email_hash": g,
            "content": row['content']['rendered'],
            "post_id": row['post']
        }

        return comment

class PostsStream(MJJWordPressRESTStream):
    """The posts stream."""
    name = "posts"
    path = "/posts"
    primary_keys = ["post_id"]
    replication_key = "date"
    can_use_start = True

    schema_filepath = SCHEMAS_DIR / "posts.json"

    def post_process(self, row: dict, context: Optional[dict]) -> dict:
        """As needed, append or transform raw data to match expected structure."""


        post = {
            "post_id": row['id'],
            "author_id": row['author'],
            "title": row['title']['rendered'],
            "link": row['link'],
            "date": row['date_gmt'],
            "content": row['content']['rendered'],
        }

        return post
