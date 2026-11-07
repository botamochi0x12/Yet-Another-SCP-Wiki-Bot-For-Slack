# SCP Wiki Bot For Slack

This bot is yet another Slack bot, picking up SCP objects everyday.
It posts one article per run to Slack, to a Discord incoming webhook, or to both,
so a single `python scp_bot.py` is all a cron job needs.

## Usage

1. `cp .env.example .env` and fill in the destinations you use:
   - Slack: both `SLACK_API_TOKEN` and `CHANNEL_ID`
   - Discord: `DISCORD_WEBHOOK_URL` (Server Settings → Integrations → Webhooks)

   Remove or leave empty the lines of a destination you do not use.
2. `uv sync`
3. `uv run python scp_bot.py` — posts one SCP article and exits.

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
