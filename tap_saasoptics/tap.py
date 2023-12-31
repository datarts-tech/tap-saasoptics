"""saasoptics tap class."""

from __future__ import annotations

from singer_sdk import Tap
from singer_sdk import typing as th  # JSON schema typing helpers

from tap_saasoptics import streams

STREAM_TYPES = [
    streams.AccountsStream,
    streams.AutoRenewalProfilesStream,
    streams.BillingDescriptionsStream,
    streams.BillingMethodsStream,
    streams.ContractsStream,
    streams.CountryCodeStream,
    streams.CurrencyCodesStream,
    streams.CustomersStream,
    streams.DeletedContractsStream,
    streams.DeletedInvoicesStream,
    streams.DeletedRevenueEntriesStream,
    streams.DeletedTransactionsStream,
    streams.InvoicesStream,
    streams.ItemsStream,
    streams.PaymentTermsStream,
    streams.RegistersStream,
    streams.RevenueEntriesStream,
    streams.RevenueRecognitionMethodsStream,
    streams.SalesOrdersStream,
    streams.TransactionsStream
]


class Tapsaasoptics(Tap):
    """SaaSOptics tap class."""

    name = "tap-saasoptics"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "api_token",
            th.StringType,
            required=True,
            secret=True,  # Flag config as protected.
            description="Your API token.",
        ),
        th.Property(
            "account_name",
            th.StringType,
            required=True,
            description="The account_name is everything between `.saasoptics.com.` and `api` in the SaaSOptics URL.",
        ),
        th.Property(
            "server_subdomain",
            th.StringType,
            required=True,
            description="The server_subdomain is everything before `.saasoptics.com.`.",
        ),
        th.Property(
            "start_date",
            th.DateTimeType,
            description="Start date for date-filtered endpoints.",
        ),
        th.Property(
            "user_agent",
            th.StringType,
            description="tap-saasoptics <api_user_email@your_company.com>.",
        ),
        th.Property(
            "custom_fields",
            th.ArrayType(
                th.ObjectType(
                    th.Property("name", th.StringType),
                    th.Property("fields", th.ArrayType(th.StringType))
                )
            ),
            description="All listed fields are included into specific stream."
        )
    ).to_dict()

    def discover_streams(self) -> list[streams.SaaSOpticsStream]:
        """Return a list of discovered streams.

        Returns:
            A list of discovered streams.
        """
        return [stream(tap=self) for stream in STREAM_TYPES]


if __name__ == "__main__":
    Tapsaasoptics.cli()
