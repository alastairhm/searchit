"""Tests for search.py's WebSearch CLI."""

import urllib.parse

import pytest

import search as search_module
from search import WebSearch


@pytest.fixture
def ws():
    return WebSearch()


def test_default_engine_resolves_to_configured_default(ws):
    assert ws.engine == ws.settings["default"]
    assert ws.search_url == ws.settings[ws.settings["default"]]


def test_named_engine_resolves_to_its_url():
    w = WebSearch(engine="startpage")
    assert w.search_url == w.settings["startpage"]


def test_unknown_engine_falls_back_to_default_url():
    w = WebSearch(engine="not-a-real-engine")
    assert w.search_url == w.default_url


def test_search_percent_encodes_term_before_browsing(ws, monkeypatch):
    seen = {}
    monkeypatch.setattr(ws, "browse", lambda url: seen.setdefault("url", url))

    ws.search("a & b#c")

    assert seen["url"] == ws.search_url + urllib.parse.quote_plus("a & b#c")


def test_all_excludes_reserved_keys_and_uses_browse(ws, monkeypatch):
    opened = []
    monkeypatch.setattr(ws, "browse", lambda url: opened.append(url))

    ws.all("term")

    engine_keys = [k for k in ws.settings if k not in ("default", "browser")]
    assert len(opened) == len(engine_keys)
    encoded = urllib.parse.quote_plus("term")
    for key in engine_keys:
        assert ws.settings[key] + encoded in opened
    # the browser executable path must never be treated as a search URL
    assert not any(ws.settings["browser"] in url for url in opened)


def test_browse_uses_argv_list_not_shell_on_wsl(ws, monkeypatch):
    calls = []
    monkeypatch.setattr(
        search_module.subprocess, "Popen", lambda args, **kw: calls.append((args, kw))
    )
    ws.wsl = True

    ws.browse("https://example.com/?q=term")

    assert len(calls) == 1
    args, kwargs = calls[0]
    assert args == [ws.browser_path, "https://example.com/?q=term"]
    assert kwargs.get("shell") is not True


def test_browse_uses_webbrowser_when_not_wsl(ws, monkeypatch):
    opened = []
    monkeypatch.setattr(search_module.webbrowser, "open", lambda url: opened.append(url))
    ws.wsl = False

    ws.browse("https://example.com/?q=term")

    assert opened == ["https://example.com/?q=term"]
