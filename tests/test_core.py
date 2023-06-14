"""Tests standard tap features using the built-in SDK tests library."""

import datetime

from singer_sdk.testing import get_tap_test_class

from tap_saasoptics.tap import Tapsaasoptics

SAMPLE_CONFIG = {
    "api_token": "secret",
    "account_name": "my_company",
    "server_subdomain": "m13",
    "start_date": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d"),
}


# Run standard built-in tap tests from the SDK:
# 0 tests to be run
TestTapsaasoptics = get_tap_test_class(
    tap_class=Tapsaasoptics,
    config=SAMPLE_CONFIG,
    include_tap_tests=False,
    include_stream_tests=False,
    include_stream_attribute_tests=False,
)


# TODO: Create additional tests as appropriate for your tap.
