"""REST client handling, including saasopticsStream base class."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Callable

import requests

from singer_sdk.authenticators import APIKeyAuthenticator
from singer_sdk.pagination import BasePageNumberPaginator
from singer_sdk.streams import RESTStream
from singer_sdk.helpers._flattening import get_flattening_options
from singer_sdk.mapper import SameRecordTransform, StreamMap

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
    _convert_to_float = None

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
    
    @property
    def convert_to_float(self):
        """Extracts the list of columns which should be converted to floats."""
        if self._convert_to_float is None:
            self._convert_to_float = list()
            schema_properties = self.schema.get('properties', {})
            for col, attributes in schema_properties.items():
                # We don't care about complex data types
                if 'type' not in attributes.keys():
                    continue
                if 'number' in attributes.get('type'):
                    self._convert_to_float.append(col)
        return self._convert_to_float

    @property
    def schema(self) -> dict:
        """Overwrites self._schema with additional custom_fields."""
        # Return object is self._schema
        _schema = super().schema
        if not self._is_schema_updated and self.config.get('custom_fields'):
            self._update_schema_with_custom_fields()
        return _schema
    
    @property
    def stream_maps(self) -> list[StreamMap]:
        """Get stream transformation maps.

        The 0th item is the primary stream map. List should not be empty.

        Returns:
            A list of one or more map transformations for this stream.
        """
        if self._stream_maps:
            return self._stream_maps

        self.logger.info(
            "No custom mapper provided for '%s'. Using SameRecordTransform.",
            self.name,
        )
        self._stream_maps = [
            SameRecordTransform(
                stream_alias=self.name,
                raw_schema=self.schema,
                key_properties=self.primary_keys,
                flattening_options=get_flattening_options(self.config),
            ),
        ]
        return self._stream_maps
    
    def _update_schema_with_custom_fields(self):
        for stream in self.config.get('custom_fields'):
            if self.name == stream['name']:
                for field in stream['fields']:
                    # Tweak with internal variable for schema property
                    # TODO: add custom data type mapping
                    self._schema['properties'].update({field: {'type': ['string', 'null']}})
        self._is_schema_updated = True

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
        return params

    def post_process(
        self,
        row: dict,
        context: dict | None = None,  # noqa: ARG002
    ) -> dict | None:
        """Transform string decimals to float.

        Args:
            row: An individual record from the stream.
            context: The stream context.

        Returns:
            The updated record dictionary, or ``None`` to skip the record.
        """
        # Do an transformation of string to float
        for col_name, value in row.items():
            if col_name in self.convert_to_float:
                try:
                    row[col_name] = float(value)
                # Handling None
                except TypeError:
                    pass
        return row
