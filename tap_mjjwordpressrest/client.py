"""REST client handling, including MJJWordPressRESTStream base class."""

import requests
import re
import base64
import logging
from typing import Any, Dict, Optional, Iterable

from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.streams import RESTStream
from singer_sdk import typing as th  # JSON Schema typing helpers

class MJJWordPressRESTStream(RESTStream):
    """MJJWordPressREST stream class."""

    @property
    def per_page(self) -> int:
        """Get the per page with default"""
        if "per_page" in self.config:
            p = self.config["per_page"]
        else:
            p = 100
        return p

    @property
    def max_pages(self) -> int:
        """Get the max pages with default"""
        if "max_pages" in self.config:
            p = self.config["max_pages"]
        else:
            p = 5
        return p

    @property
    def url_base(self) -> str:
        """Return the API URL root, configurable via tap settings."""
        return self.config["api_url"] + '/wp-json/wp/v2'

    records_jsonpath = "$[*]"  # Or override `parse_response`.
    next_page_token_jsonpath = "$.next_page"  # Or override `get_next_page_token`.

    @property
    def http_headers(self) -> dict:
        """Return the http headers needed."""
        headers = {}
        if "user_agent" in self.config:
            headers["User-Agent"] = self.config.get("user_agent")
        # If not using an authenticator, you may also provide inline auth headers:
        if "application_password" in self.config and "username" in self.config:
            userpass = self.config.get("username") + ":" + \
                self.config.get("application_password")
            userpass_bytes = userpass.encode('ascii')
            base64_bytes = base64.b64encode(userpass_bytes)
            base64_userpass = base64_bytes.decode('ascii')
            headers["Authorization"] = "Basic " + base64_userpass
        return headers

    def get_next_page_token(
        self, response: requests.Response, previous_token: Optional[Any]
    ) -> Optional[Any]:
        """Return a token for identifying next page or None if no more pages. The maximum number of pages is configurable via tap settings."""
        total_pages = int( response.headers['X-WP-TotalPages'] or 1 )

        # If pagination is required, return a token which can be used to get the
        #       next page. If this is the final page, return "None" to end the
        #       pagination loop.

        no_more_responses = int( previous_token or 1 ) >= total_pages
        has_max_pages = ( previous_token and previous_token == self.max_pages )

        if no_more_responses or has_max_pages:
            # stop if we've done the max number of pages or if there are no more reponses.
            next_page_token = None
        elif not previous_token:
            # if there's no previous token, we're on page 2.
            next_page_token = 2
        else:
            # otherwise, keep on going.
            next_page_token = previous_token + 1

        return next_page_token

    def get_url_params(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization."""
        params: dict = {}
        params["per_page"] = self.per_page
        if next_page_token:
            params["page"] = next_page_token
        if self.replication_key:
            params["order"] = "asc"
            params["order_by"] = self.replication_key
            if self.get_starting_replication_key_value(context) is not None:
                params["after"] = self.get_starting_replication_key_value(context)
                logging.info("AFTER")
                logging.info(params["after"])
        logging.info(params)
        return params

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result rows."""
        yield from extract_jsonpath(self.records_jsonpath, input=response.json())

    def get_email_hash( self, row: dict ) -> th.StringType:
        """Return the email hash if the site has Gravatar enabled"""
        if self.avatar_key in row:
            ga = re.search('https://secure.gravatar.com/avatar/(.+?)\?s',
                row[self.avatar_key]['24'])
            g = ga.group(1)
        else:
            g = None
        return g
