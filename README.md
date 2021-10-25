# tap-mjjwordpressrest

`tap-mjjwordpressrest` is a Singer tap which currently gets data from the users, comments and posts endpoints on a WordPress site which uses the WordPress REST API.

It is a test tap for playing around with and should not be used in production environments.

It does not (yet) save state.

Built with the [Meltano Tap SDK](https://sdk.meltano.com) for Singer Taps.

## Installation


```bash
pipx install git+https://github.com/tharsheblows/tap-mjjwordpressrest.git
```

## Configuration

### Accepted Config Options

A full list of supported settings and capabilities for this
tap is available by running:

```bash
tap-mjjwordpressrest --about
```

Config options:
- **api_url**: Required. The full domain of the WordPress site without a final backslash. Please note that not all WordPress sites will work, they must have an open REST API.
- **per_page**: The number of objects returned per page. WordPress has a hard limit of 100.
- **max_pages**: The maximum number of pages to return.
- **start_date**: Limits response to objects published after a given ISO8601 compliant date. Only for Posts, Post Types and Comments. Well, it would be for Posts and Post Types had I added them in but I didn't. So only for Comments.

Please not that comments and posts are queried in an ascending order by date so that keeping state will be possible in the future.

Update `config-sample.json` and save as `config.json` to use as a standalone tap.

A sample config.json file :

```json
{
	"api_url": "https://yourdomain.com",
	"per_page": 21,
	"max_pages": 3,
	"start_date": "2020-12-31T23:59:59"
}
```

### Source Authentication and Authorization

Currently this only works for open endpoints.

## Usage

You can easily run `tap-mjjwordpressrest` by itself or in a pipeline using [Meltano](https://meltano.com/).

### Executing the Tap Directly

```bash
tap-mjjwordpressrest --version
tap-mjjwordpressrest --help
tap-mjjwordpressrest --config config.json
```

## Developer Resources

### Initialize your Development Environment

```bash
pipx install poetry
poetry install
```

### Create and Run Tests

Currently no tests, I'm so sorry. I'm leaving the rest in for the future though.

Create tests within the `tap_mjjwordpressrest/tests` subfolder and
  then run:

```bash
poetry run pytest
```

You can also test the `tap-mjjwordpressrest` CLI interface directly using `poetry run`:

```bash
poetry run tap-mjjwordpressrest --help
```

### Testing with [Meltano](https://www.meltano.com)

_**Note:** This tap will work in any Singer environment and does not require Meltano.
Examples here are for convenience and to streamline end-to-end orchestration scenarios._

Your project comes with a custom `meltano.yml` project file already created. Open the `meltano.yml` and follow any _"TODO"_ items listed in
the file.

Next, install Meltano (if you haven't already) and any needed plugins:

```bash
# Install meltano
pipx install meltano
# Initialize meltano within this directory
cd tap-mjjwordpressrest
meltano install
```

Now you can test and orchestrate using Meltano:

```bash
# Test invocation:
meltano invoke tap-mjjwordpressrest --version
# OR run a test `elt` pipeline:
meltano elt tap-mjjwordpressrest target-jsonl
```

### SDK Dev Guide

See the [dev guide](https://sdk.meltano.com/en/latest/dev_guide.html) for more instructions on how to use the SDK to
develop your own taps and targets.
