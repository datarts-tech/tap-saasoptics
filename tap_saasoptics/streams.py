"""Stream type classes for tap-saasoptics."""

from __future__ import annotations

from pathlib import Path
from typing import Optional, Any, Dict

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_saasoptics.client import SaaSOpticsStream

SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")


class CustomersStream(SaaSOpticsStream):
    """Define Customers stream."""

    name = "customers"
    path = "/customers"
    primary_keys = ["id"]
    replication_method = "INCREMENTAL"
    replication_key = "modified"
    schema_filepath = SCHEMAS_DIR / "customers.json"


class ContractsStream(SaaSOpticsStream):
    """Define Contracts stream."""

    name = "contracts"
    path = "/contracts"
    primary_keys = ["id"]
    replication_method = "INCREMENTAL"
    replication_key = "modified"
    schema_filepath = SCHEMAS_DIR / "contracts.json"


class InvoicesStream(SaaSOpticsStream):
    """Define Invoices stream."""

    name = "invoices"
    path = "/invoices"
    primary_keys = ["id"]
    replication_method = "FULL_TABLE"
    # TODO: Add necessary transformations so INCREMENTAL could be used
    # Replication key with auditentry_modified not working because some records do not have the field
    # replication_key = "auditentry_modified"
    schema_filepath = SCHEMAS_DIR / "invoices.json"


class ItemsStream(SaaSOpticsStream):
    """Define Items stream."""

    name = "items"
    path = "/items"
    primary_keys = ["id"]
    replication_method = "INCREMENTAL"
    replication_key = "modified"
    schema_filepath = SCHEMAS_DIR / "items.json"


class TransactionsStream(SaaSOpticsStream):
    """Define Transactions stream."""

    name = "transactions"
    path = "/transactions"
    primary_keys = ["id"]
    replication_method = "INCREMENTAL"
    replication_key = "modified"
    schema_filepath = SCHEMAS_DIR / "transactions.json"


class BillingDescriptionsStream(SaaSOpticsStream):
    """Define Billing Descriptions stream."""

    name = "billing_descriptions"
    path = "/billing_descriptions"
    primary_keys = ["id"]
    replication_method = "FULL_TABLE"
    schema_filepath = SCHEMAS_DIR / "billing_descriptions.json"


class AccountsStream(SaaSOpticsStream):
    """Define Accounts stream."""

    name = "accounts"
    path = "/accounts"
    primary_keys = ["id"]
    replication_method = "FULL_TABLE"
    schema_filepath = SCHEMAS_DIR / "accounts.json"


class AutoRenewalProfilesStream(SaaSOpticsStream):
    """Define Auto Renewal Profiles stream."""

    name = "auto_renewal_profiles"
    path = "/auto_renewal_profiles"
    primary_keys = ["id"]
    replication_method = "FULL_TABLE"
    schema_filepath = SCHEMAS_DIR / "auto_renewal_profiles.json"


class BillingMethodsStream(SaaSOpticsStream):
    """Define Billing Methods stream."""

    name = "billing_methods"
    path = "/billing_methods"
    primary_keys = ["id"]
    replication_method = "FULL_TABLE"
    schema_filepath = SCHEMAS_DIR / "billing_methods.json"


class CountryCodeStream(SaaSOpticsStream):
    """Define Country Codes stream."""

    name = "country_codes"
    path = "/country_codes"
    primary_keys = ["id"]
    replication_method = "FULL_TABLE"
    schema_filepath = SCHEMAS_DIR / "country_codes.json"


class CurrencyCodesStream(SaaSOpticsStream):
    """Define Currency Codes stream."""

    name = "currency_codes"
    path = "/currency_codes"
    primary_keys = ["id"]
    replication_method = "FULL_TABLE"
    schema_filepath = SCHEMAS_DIR / "currency_codes.json"


class PaymentTermsStream(SaaSOpticsStream):
    """Define Payment Terms stream."""

    name = "payment_terms"
    path = "/payment_terms"
    primary_keys = ["id"]
    replication_method = "FULL_TABLE"
    schema_filepath = SCHEMAS_DIR / "payment_terms.json"


class RegistersStream(SaaSOpticsStream):
    """Define Registers stream."""

    name = "registers"
    path = "/registers"
    primary_keys = ["id"]
    replication_method = "INCREMENTAL"
    replication_key = "modified"
    schema_filepath = SCHEMAS_DIR / "registers.json"


class RevenueEntriesStream(SaaSOpticsStream):
    """Define Revenue Entries stream."""

    name = "revenue_entries"
    path = "/revenue_entries"
    primary_keys = ["id"]
    replication_key = "INCREMENTAL"
    replication_key = "modified"
    schema_filepath = SCHEMAS_DIR / "revenue_entries.json"


class RevenueRecognitionMethodsStream(SaaSOpticsStream):
    """Define Revenue Recognition Methods stream."""

    name = "revenue_recognition_methods"
    path = "/revenue_recognition_methods"
    primary_keys = ["id"]
    replication_method = "FULL_TABLE"
    schema_filepath = SCHEMAS_DIR / "revenue_recognition_methods.json"


class SalesOrdersStream(SaaSOpticsStream):
    """Define Sales Orders stream."""

    name = "sales_orders"
    path = "/sales_orders"
    primary_keys = ["id"]
    replication_method = "FULL_TABLE"
    schema_filepath = SCHEMAS_DIR / "sales_orders.json"


class DeletedContractsStream(SaaSOpticsStream):
    """Define Deleted Contracts stream."""

    name = "deleted_contracts"
    path = "/contracts/deleted"
    primary_keys = ["id"]
    replication_method = "INCREMENTAL"
    replication_key = "deleted"
    schema_filepath = SCHEMAS_DIR / "deleted_contracts.json"


class DeletedTransactionsStream(SaaSOpticsStream):
    """Define Deleted Transactions stream."""

    name = "deleted_transactions"
    path = "/transactions/deleted"
    primary_keys = ["id"]
    replication_method = "INCREMENTAL"
    replication_key = "deleted"
    schema_filepath = SCHEMAS_DIR / "deleted_transactions.json"


class DeletedInvoicesStream(SaaSOpticsStream):
    """Define Deleted Invoices stream."""

    name = "deleted_invoices"
    path = "/invoices/deleted"
    primary_keys = ["id"]
    replication_method = "INCREMENTAL"
    replication_key = "deleted"
    schema_filepath = SCHEMAS_DIR / "deleted_invoices.json"


class DeletedRevenueEntriesStream(SaaSOpticsStream):
    """Define Deleted Revenue Entries stream."""

    name = "deleted_revenue_entries"
    path = "/revenue_entries/deleted"
    primary_keys = ["id"]
    replication_method = "INCREMENTAL"
    replication_key = "deleted"
    schema_filepath = SCHEMAS_DIR / "deleted_revenue_entries.json"
