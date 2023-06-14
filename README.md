# tap-saasoptics

`tap-saasoptics` is a Singer tap for saasoptics.

Built with the [Meltano Tap SDK](https://sdk.meltano.com) for Singer Taps.

This Tap:
- Pulls raw data from the SaaSOptics v1.0 API
- Extracts the following resources:
  - Customers
  - Contracts
  - Invoices
  - Items
  - Transactions
  - Billing Desriptions
  - Accounts
  - Auto Renewal Profiles
  - Billing Methods
  - Country Codes
  - Currency Codes
  - Payment Terms
  - Registers
  - Revenue Entries
  - Revenue Recognition Methods
  - Sales Orders
- Outputs the schema for each resource
- Incrementally pulls data based on the input state

<!--

Developer TODO: Update the below as needed to correctly describe the install procedure. For instance, if you do not have a PyPi repo, or if you want users to directly install from your git repo, you can modify this step as appropriate.



## Installation

Install from PyPi:

```bash
pipx install tap-saasoptics
```

-->
## Installation

Install from GitHub:

```bash
pipx install git+https://github.com/datarts-tech/tap-saasoptics.git@master
```

## Capabilities

* `catalog`
* `state`
* `discover`
* `about`
* `stream-maps`
* `schema-flattening`
* `batch`

## Settings

| Setting             | Required | Default | Description |
|:--------------------|:--------:|:-------:|:------------|
| api_token           | True     | None    | Your API token. |
| account_name        | True     | None    | The account_name is everything between `.saasoptics.com.` and `api` in the SaaSOptics URL. |
| server_subdomain    | True     | None    | The server_subdomain is everything before `.saasoptics.com.`. |
| start_date          | False    | None    | Start date for date-filtered endpoints. |
| user_agent          | False    | None    | tap-saasoptics <api_user_email@your_company.com>. |
| custom_field_prefix | False    | None    | If added, all fields with these prefixes are included into the output. |
| stream_maps         | False    | None    | Config object for stream maps capability. For more information check out [Stream Maps](https://sdk.meltano.com/en/latest/stream_maps.html). |
| stream_map_config   | False    | None    | User-defined config values to be used within map expressions. |
| flattening_enabled  | False    | None    | 'True' to enable schema flattening and automatically expand nested properties. |
| flattening_max_depth| False    | None    | The max depth to flatten schemas. |
| batch_config        | False    | None    |             |

<!--
Developer TODO: Provide a list of config options accepted by the tap.

This section can be created by copy-pasting the CLI output from:

```None
tap-saasoptics --about --format=markdown
```
-->

A full list of supported settings and capabilities for this
tap is available by running:

```bash
tap-saasoptics --about
```

### Configure using environment variables

This Singer tap will automatically import any environment variables within the working directory's
`.env` if the `--config=ENV` is provided, such that config values will be considered if a matching
environment variable is set either in the terminal context or in the `.env` file.

### Source Authentication and Authorization

<!--
Developer TODO: If your tap requires special access on the source system, or any special authentication requirements, provide those here.
-->

## Usage

You can easily run `tap-saasoptics` by itself or in a pipeline using [Meltano](https://meltano.com/).

### Executing the Tap Directly

```bash
tap-saasoptics --version
tap-saasoptics --help
tap-saasoptics --config CONFIG --discover > ./catalog.json
```

## Developer Resources

Follow these instructions to contribute to this project.

### Initialize your Development Environment

```bash
pipx install poetry
poetry install
```

### Create and Run Tests

Create tests within the `tests` subfolder and
  then run:

```bash
poetry run pytest
```

You can also test the `tap-saasoptics` CLI interface directly using `poetry run`:

```bash
poetry run tap-saasoptics --help
```

### Testing with [Meltano](https://www.meltano.com)

_**Note:** This tap will work in any Singer environment and does not require Meltano.
Examples here are for convenience and to streamline end-to-end orchestration scenarios._

<!--
Developer TODO:
Your project comes with a custom `meltano.yml` project file already created. Open the `meltano.yml` and follow any "TODO" items listed in
the file.
-->

Next, install Meltano (if you haven't already) and any needed plugins:

```bash
# Install meltano
pipx install meltano
# Initialize meltano within this directory
cd tap-saasoptics
meltano install
```

Now you can test and orchestrate using Meltano:

```bash
# Test invocation:
meltano invoke tap-saasoptics --version
# OR run a test `elt` pipeline:
meltano elt tap-saasoptics target-jsonl
```

### SDK Dev Guide

See the [dev guide](https://sdk.meltano.com/en/latest/dev_guide.html) for more instructions on how to use the SDK to
develop your own taps and targets.
