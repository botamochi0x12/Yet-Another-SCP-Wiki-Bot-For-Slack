# Separate SCP data from application history

## Background and purpose

Refreshing the SCP catalog should not advance the application repository's HEAD.
Store catalog snapshots in an independent Git repository and exchange files by
path, without a submodule or a pinned data commit in the application repository.

## Data contract

- The data repository has `scraped/` for per-series CSV snapshots and `posting/`
  for merged CSV and JSON catalogs.
- Preserve existing snapshot contents, filenames, and the JSON `path` / `title`
  column mappings during migration.
- Set `SCP_DATA_DIR` to the data checkout when running the collector.
- Set `SCP_LIST_PATH` to the Japanese posting JSON when running the bot.
- Keep the collector, bot, tests, and logo assets in the application repository.
- Data acquisition and updates are explicit operations; posting does not fetch
  data or resolve Git revisions.

## Acceptance criteria

- No catalog CSV or JSON is tracked in the application repository.
- The bot reads an external JSON, including when invoked from another directory.
- Missing configuration or data fails before any Slack or Discord post.
- The collector reads and writes only the configured data directories without
  changing the process's working directory.
- Data updates leave the application HEAD and working tree unchanged.
- Existing posting tests pass with mocked destinations; migration preserves all
  snapshot bytes.

## Scope

Document setup, migration, and manual updates. Do not change article selection,
posting payloads, scrape filters, or existing snapshot contents. Do not remove
the unrelated existing `pyscp` submodule.
