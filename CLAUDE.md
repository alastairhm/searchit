# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

`searchit` is a tiny single-file Python CLI (`search.py`) that opens a web search in the browser for a given search engine. All CLI plumbing comes from `python-fire`, which auto-generates the command interface from the `WebSearch` class's public methods — there is no argparse/click layer to maintain.

## Running

```bash
pip install -r requirements.txt

./search.py --help
./search.py search "terraform templates"
./search.py search "terraform templates" --engine=startpage
./search.py engines          # list configured engine names
./search.py all "term"       # open the search in every configured engine at once
```

`search.sh` is a wrapper that activates a local `env/` virtualenv and calls `search.py search "$1"` — it assumes a venv at `<script_dir>/env`, which is not part of this repo (create it locally if you use this wrapper).

There is no linter or build step in this repo.

## Tests

```bash
pip install -r requirements-dev.txt
pytest
```

`test_search.py` covers `WebSearch`'s engine resolution, URL encoding, the `all()` reserved-key filtering, and the WSL vs. non-WSL branches of `browse()`, using `monkeypatch` to stub out `browse()`/`subprocess.Popen`/`webbrowser.open` so tests never actually launch a browser.

## Architecture

- **`search.py`** — the entire application. The `WebSearch` class:
  - Loads engine definitions from `searchIt.toml` (same directory as the script) on init; raises `FileNotFoundError` if missing.
  - Resolves the `--engine` flag against the TOML keys, falling back to `default_url` if the named engine isn't found.
  - Builds the search URL via `search_url + urllib.parse.quote_plus(term)` — the term is percent-encoded before being appended, so `&`, `#`, and spaces in a search term can't corrupt the query string.
  - `browse()` branches on WSL detection (`'microsoft-standard' in platform.uname().release`): under WSL it launches the Windows browser binary configured via `browser` in the TOML as `subprocess.Popen([browser_path, url])` (argv list, no shell — `webbrowser.open` can't reach a Windows browser from WSL); otherwise it uses Python's standard `webbrowser` module.

- **`searchIt.toml`** — the engine registry and config, structured as a flat TOML table:
  - `default` — the key of the engine to use when none is specified.
  - `browser` — path to the browser executable used in the WSL code path.
  - every other key is `engine_name = "https://...?q="`, a URL prefix that the search term is appended to.

  Adding a new search engine means adding one `name = "url_prefix"` line here — no code changes needed. `default` and `browser` are reserved keys: `all()` excludes both of them (via its `reserved_keys` tuple) when iterating the TOML to search every engine, so a new top-level config key that isn't meant to be a search engine needs to be added to that tuple too.
