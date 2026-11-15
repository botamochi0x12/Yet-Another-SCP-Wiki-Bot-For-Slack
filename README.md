# SCP Wiki Bot For Slack

This bot is yet another Slack bot, picking up SCP objects everyday.
It posts one article per run to Slack, to a Discord incoming webhook, or to both,
so a single `python scp_bot.py` is all a cron job needs.

## Usage

1. `cp .env.example .env` and fill in the destinations you use:
   - Slack: both `SLACK_API_TOKEN` and `CHANNEL_ID`
   - Discord: `DISCORD_WEBHOOK_URL` (Server Settings → Integrations → Webhooks)

   Remove or leave empty the lines of a destination you do not use.
2. Obtain an independent SCP data checkout (see below) and set `SCP_LIST_PATH`
   in `.env` to the **absolute path** of its `posting/scp-series-jp-list.json`.
3. `uv sync`
4. `uv run python scp_bot.py` — posts one SCP article and exits.

### Data checkout and updates

Catalog snapshots belong in a separate Git repository, with this layout:

```text
scp-wiki-data/
  scraped/scp-series*.csv
  posting/scp-series-list.csv
  posting/scp-series-list.json
  posting/scp-series-jp-list.csv
  posting/scp-series-jp-list.json
```

Clone your data repository to a location outside this application checkout.
`SCP_LIST_PATH` is a file reference: the application does not pin a data commit,
use a submodule for the catalog, or fetch data while posting. Updating the data
checkout does not require an application commit. JSON catalogs retain the
`{"path": {"0": "/scp-..."}, "title": {"0": "..."}}` format with matching,
consecutive indices starting at zero. The bot uses the Japanese catalog.

To refresh snapshots from the application checkout:

```console
$ uv sync --extra crawler
$ SCP_DATA_DIR=/absolute/path/to/scp-wiki-data uv run --extra crawler python resources/collector.py
```

The collector is a manually configured, cell-style script. Before running it,
select the target series in `pagepath`, and set `domain`, `empty_pattern`, and
`pagebasepath` for the same language. Its checked-in configuration targets
English series 9; it does not refresh every series automatically. The base
series CSV must already exist in `scraped/`. Individual series CSVs are read
and written in `scraped/`; merged catalogs are written in `posting/`.
`SCP_DATA_DIR` must be exported in the shell or set on the command line; the
collector does not read `.env`.

Review and commit changed catalogs **in the data repository**. On a posting
machine, update that checkout separately and keep `SCP_LIST_PATH` pointing to
its Japanese posting JSON. Record `git -C /absolute/path/to/scp-wiki-data rev-parse HEAD`
when you need the data revision used for a run. No data revision is stored in
the application repository.

For an existing installation, preserve your current CSV and JSON files in the
layout above before updating the application, then add `SCP_LIST_PATH` to
`.env`. The old bundled catalog path is no longer used. A missing configuration
or file stops a normal posting run before any message is sent. Existing
snapshots are migrated without refreshing their contents.

### Checking the Discord post locally

Point the webhook URL at a local listener to see the exact payload that would be
sent. The empty Slack variables keep the run from also posting to Slack:

```console
$ printf 'HTTP/1.1 204 No Content\r\n\r\n' | ncat -l 127.0.0.1 8099   # another terminal
$ SLACK_API_TOKEN= CHANNEL_ID= DISCORD_WEBHOOK_URL=http://127.0.0.1:8099/ uv run python scp_bot.py
```

## TODO

- [x] Get existing URLs from the SCP servers
- [ ] Pick up SCP objects
  - [x] Randomly
  - [ ] With statistic such as [the random-page](http://ja.scp-wiki.net/random:random-page)
- [ ] Reply if someone mentions an emoji
- [ ] List up all the authors as contributors
- [x] Use `.env` to extract a Slack API token for channels in a workspace
- [x] Use [`slack_sdk`](https://github.com/slackapi/python-slack-sdk) package
- [x] Post to a Discord incoming webhook with [`requests`](https://requests.readthedocs.io/)
- [ ] Show description of each SCP
  - [ ] Use scraped data
  - [ ] Use Google Search

## License For SCP Materials

Shield: [![CC BY-SA 4.0][cc-by-sa-shield]][cc-by-sa]

- `scp-logo-jp` (日の丸SCPロゴ): Copyright by NanimonoDemonai, [JP-HUB - International Translation Archive](http://scp-int.wikidot.com/jp-hub), CC BY-SA 3.0
- The **SCP**s: Copyright by *each author*, CC BY-SA 3.0

These materials are licensed under a [Creative Commons Attribution-ShareAlike 4.0
International License][cc-by-sa].

[![CC BY-SA 4.0][cc-by-sa-image]][cc-by-sa]

[cc-by-sa]: http://creativecommons.org/licenses/by-sa/4.0/
[cc-by-sa-image]: https://licensebuttons.net/l/by-sa/4.0/88x31.png
[cc-by-sa-shield]: https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg
