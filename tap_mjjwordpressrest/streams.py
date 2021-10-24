"""Stream type classes for tap-mjjwordpressrest."""

from pathlib import Path
from typing import Any, Dict, Optional, Union, List, Iterable

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_mjjwordpressrest.client import MJJWordPressRESTStream

# Delete this is if not using json files for schema definition
# SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")

# I'm currently keeping this all here for this one because this is how it is out of the box.


class UsersStream(MJJWordPressRESTStream):
    """Define custom stream."""
    name = "users"
    path = "/users"
    primary_keys = ["id"]
    replication_key = None
    avatar_key = "avatar_urls"
    can_use_start = False
    # Optionally, you may also use `schema_filepath` in place of `schema`:
    # schema_filepath = SCHEMAS_DIR / "users.json"
    schema = th.PropertiesList(
        th.Property(
            "id",
            th.IntegerType,
            description="The user's system ID"
        ),
        th.Property(
            "display_name",
            th.StringType,
            description="The user's display name"
        ),
        th.Property(
            "username",
            th.StringType,
            description="The user's username"
        ),
        th.Property(
            "email_hash",
            th.StringType,
            description="The user's email address hash"
        )
    ).to_dict()

    def post_process(self, row: dict, context: Optional[dict]) -> dict:
        """As needed, append or transform raw data to match expected structure."""
        # TODO: Delete this method if not needed.
        # print("Users whooo")
        # print(row)
        g = self.get_email_hash(row)

        user = {
            "id": row['id'],
            "display_name": row['name'],
            "username": row['slug'],
            "email_hash": g
        }

        # print(user)
        return user


class CommentsStream(MJJWordPressRESTStream):
    """Define custom stream."""
    name = "comments"
    path = "/comments"
    primary_keys = ["id"]
    replication_key = "date"
    avatar_key = "author_avatar_urls"
    can_use_start = True
    schema = th.PropertiesList(
        th.Property(
            "id",
            th.IntegerType,
            description="The comment ID"
        ),
        th.Property(
            "commenter_id",
            th.IntegerType,
            description="The commenter's user id if there is one."
        ),
        th.Property(
            "commenter_name",
            th.StringType,
            description="The commenter's user name if there is one."
        ),
        th.Property(
            "commenter_url",
            th.StringType,
            description="The commenter's url if there is one."
        ),
        th.Property(
            "date",
            th.StringType,
            description="The date the comment was posted."
        ),
        th.Property(
            "email_hash",
            th.StringType,
            description="The commenter's email address hash"
        ),
        th.Property(
            "content",
            th.StringType,
            description="The comment content"
        ),
        th.Property(
            "post_id",
            th.IntegerType,
            description="The post id"
        )
    ).to_dict()

    def post_process(self, row: dict, context: Optional[dict]) -> dict:
        """As needed, append or transform raw data to match expected structure."""

        g = self.get_email_hash(row)

        comment = {
            "id": row['id'],
            "commenter_id": row['author'],
            "commenter_name": row['author_name'],
            "commenter_url": row['author_url'],
            "date": row['date_gmt'],
            "email_hash": g,
            "content": row['content']['rendered'],
            "post_id": row['post']
        }

        return comment
