"""REST client handling, including saasopticsStream base class."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Callable, Iterable

import json
import requests
from collections.abc import MutableMapping

from singer_sdk.authenticators import APIKeyAuthenticator
from singer_sdk.pagination import BasePageNumberPaginator
from singer_sdk.streams import RESTStream
from singer_sdk import typing as th  # JSON schema typing helpers

_Auth = Callable[[requests.PreparedRequest], requests.PreparedRequest]
SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")

API_VERSION = 'v1.0'
    

class SaaSOpticsNumberPaginator(BasePageNumberPaginator):
    """SaaSOptics paginator class."""

    def has_more(self, response: requests.Response) -> bool:
        """Checking if the `next` key is available in the response."""
        data = response.json()
        return data.get('next') is not None


class SaaSOpticsStream(RESTStream):
    """SaaSOptics stream class."""

    records_jsonpath = "$.results[*]"

    _is_schema_updated = False
    _incremental_key = None

    @property
    def url_base(self) -> str:
        """Return the API URL root, configurable via tap settings."""
        return f'https://{self.config.get("server_subdomain")}.saasoptics.com/{self.config.get("account_name")}/api/{API_VERSION}'

    @property
    def authenticator(self) -> APIKeyAuthenticator:
        """Return a new authenticator object.

        Returns:
            An authenticator instance.
        """
        return APIKeyAuthenticator.create_for_stream(
            self,
            key="Authorization",
            value=f'Token {self.config.get("api_token")}',
            location="header",
        )
    
    @property
    def incremental_key(self):
        """Custom handler of the key which is used for incremental replication."""
        if self._incremental_key is None:
            if self.name == 'transactions':
                self._incremental_key = 'auditentry__modified__gte'
            else:
                self._incremental_key = f"{self.replication_key}__gte"
        return self._incremental_key

    def get_new_paginator(self):
        """Method for handling the pagination."""
        return SaaSOpticsNumberPaginator(start_value=1)

    def get_url_params(
        self,
        context: dict | None,  # noqa: ARG002
        next_page_token: Any | None,
    ) -> dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization.

        Args:
            context: The stream context.
            next_page_token: The next page index or value.

        Returns:
            A dictionary of URL query parameters.
        """
        params: dict = {}
        if next_page_token:
            params["page"] = next_page_token
        if self.replication_key:
            params["sort"] = "asc"
            params["order_by"] = self.incremental_key
            params[self.incremental_key] = self.get_starting_replication_key_value(context)
        self.logger.info(f'params - {params}')
        return params

    def _update_schema_with_custom_fields(self, keys):
        for prefix in self.config.get('custom_field_prefix'):
            for key in keys:
                if key.startswith(prefix) and key not in self._schema['properties']:
                    # Tweak with internal variable for schema property
                    # TODO: add custom data type mapping
                    self._schema['properties'].update({key: {'type': ['string', 'null']}})
        self._is_schema_updated = True

    def post_process(
        self,
        row: dict,
        context: dict | None = None,  # noqa: ARG002
    ) -> dict | None:
        """Use a single record to update schema with custom fields.

        Args:
            row: An individual record from the stream.
            context: The stream context.

        Returns:
            The updated record dictionary, or ``None`` to skip the record.
        """
        if not self._is_schema_updated and self.config.get('custom_field_prefix'):
            self._update_schema_with_custom_fields(row.keys())
        return row
