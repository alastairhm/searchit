# Changelog

All notable changes to this project are documented in this file.

## [Unreleased]

### Fixed
- **Security:** removed a shell-injection vector in `browse()` — the WSL browser launch used `subprocess.Popen(..., shell=True)` with an unescaped URL built from the raw search term, so a term containing `"`, backticks, or `$()` could run arbitrary shell commands. It now passes the browser path and URL as separate argv entries with no shell involved.
- Search terms are now percent-encoded (`urllib.parse.quote_plus`) before being appended to the search URL, so terms containing `&`, `#`, or spaces no longer corrupt the resulting query string.
- `all()` no longer treats the `browser` config key as a search engine (it only excluded `default` before), and now goes through `browse()` so it launches correctly under WSL like `search()` does.
