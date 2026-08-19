# TODO

Known improvement ideas not yet actioned.

- **`browse()` doesn't handle launch failures.** `search.py:33-39` — if `browser_path` (WSL) is misconfigured or the binary's missing, or `webbrowser.open()` fails on non-WSL, the user gets a raw traceback instead of a clear error message.

- **Dead fallback default for `browser_path`.** `search.py:24` — `self.settings.get("browser", "google-chrome")` falls back to `"google-chrome"`, a Linux binary name, but `browser_path` is only ever used on the WSL branch (`browse()`), where it needs to be a Windows path/executable. The fallback is misleading and would fail if it were ever actually hit; `browser` is always set in `searchIt.toml` today so this hasn't bitten anyone yet.

- **`search.sh` assumes a venv exists with no check.** `search.sh:6` — `source $SCRIPT_DIR/env/bin/activate` will fail ungracefully if `<script_dir>/env` doesn't exist. Only matters if this wrapper is actually used (`search.py` itself has no venv dependency).
