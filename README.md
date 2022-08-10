# tap-mjjwordpressrest

`tap-mjjwordpressrest` is a Singer tap which currently gets data from the users, comments and posts endpoints on a WordPress site which uses the WordPress REST API.

It is a test tap for playing around with and should not be used in production environments.

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
- **per_page**: The number of objects returned per page. WordPress has a hard limit of 100. *Default: 10*
- **max_pages**: The maximum number of pages to return. *Default: 5*
- **start_date**: Limits response to objects published after a given ISO8601 compliant date. Only for Posts, Post Types and Comments. Well, it would be for Posts and Post Types had I added them in but I didn't. So only for Comments. *Default: 2020-12-31T23:59:59*
- **user_agent**: Some APIs return a 403 error without a useragent. This value is used in the headers of the request. *Default: none*


Please not that comments and posts are queried in an ascending order by date so that keeping state will be possible in the future. Kind of that is. Currently the "after" query param could be used to get those objects from a specific second in time but there will be collisions with this so that comments and posts could be missed if they happen at the same second but not all objects were gotten during the previous run.

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

### NOTE ON USERS

I'm still not quite sure how to handle state with users. It would ideally be by user id (ie `id` in the `wp_users` table) but this isn't possible out of the box.

### Source Authentication and Authorization

If you are using source authentication and authorization, please use WordPress's application passwords and store your config as environment variables with using the nomeclature TAP_MJJWORDPRESSREST_<capitalised key name>. I use this with Meltano and the instructions for setting these is here: [https://meltano.com/docs/configuration.html#configuration-layers](https://meltano.com/docs/configuration.html#configuration-layers)

- **username**: Set the username as the TAP_MJJWORDPRESSREST_USERNAME environment variable. For protected endpoints, use an application password for a user. This is the username.  *Default: none*
- **application_password**: Set the application password as the TAP_MJJWORDPRESSREST_APPLICATION_PASSWORD environment variable.For protected endpoints, use an application password for a user. This is that password. *Default: none*


## Usage

You can easily run `tap-mjjwordpressrest` by itself or in a pipeline using [Meltano](https://meltano.com/).

### Executing the Tap Directly

#### Using config.json

```bash
tap-mjjwordpressrest --version
tap-mjjwordpressrest --help
tap-mjjwordpressrest --config config.json
```

#### Using environment variables
```bash
tap-mjjwordpressrest --config ENV
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
