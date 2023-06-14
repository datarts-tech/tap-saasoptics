"""Stream type classes for tap-saasoptics."""

from __future__ import annotations

from pathlib import Path
from typing import Optional, Any, Dict

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_saasoptics.client import SaaSOpticsStream

SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")


class ContractsStream(SaaSOpticsStream):
    """Define Contracts stream."""

    name = "contracts"
    path = "/contracts"
    primary_keys = ["id"]
    replication_key = "INCREMENTAL"
    replication_key = "modified"
    schema_filepath = SCHEMAS_DIR / "contracts.json"