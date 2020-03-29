# SCP Wiki Bot For Slack

This bot is yet another Slack bot, picking up SCP objects everyday.

## TODO

- [x] Get existing URLs from the SCP servers
- [ ] Pick up SCP objects
  - [x] Randomly
  - [ ] With statistic such as [the random-page](http://ja.scp-wiki.net/random:random-page)
- [ ] Reply if someone mention an emoji
- [ ] List up all the authors as contributors
- [x] Use `.env` to extract a Slack API token for channels in a workspace
- [x] Use [`slackclient`](https://github.com/slackapi/python-slackclient) package
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
