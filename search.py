#!/usr/bin/env python3
"""Quick searching from command line"""

import os
import fire
import subprocess
import toml
import webbrowser
import platform
import urllib.parse


class WebSearch:
    """Simple Websearch CLI"""

    def __init__(self, engine="default"):
        """Init"""
        script_path = os.path.dirname(os.path.abspath(__file__))
        settings_path = os.path.join(script_path, "searchIt.toml")
        if not os.path.exists(settings_path):
            raise FileNotFoundError(f"Configuration file not found: {settings_path}")
        self.settings = toml.load(settings_path)
        self.default_url = self.settings[self.settings["default"]]
        self.browser_path = self.settings.get("browser", "google-chrome")

        if engine == "default":
            self.engine = self.settings[engine]
        else:
            self.engine = engine
        self.search_url = self.settings.get(self.engine, self.default_url)
        self.wsl = 'microsoft-standard' in platform.uname().release

    def browse(self, url):
        if self.wsl:
            # Pass the browser and URL as separate argv entries (no shell=True)
            # so a search term can never be interpreted as shell syntax.
            subprocess.Popen([self.browser_path, url])
        else:
            webbrowser.open(url)

    #def search(self, term=pyperclip.paste()):
    def search(self, term):
        """Search passed term"""
        url = self.search_url + urllib.parse.quote_plus(term)
        self.browse(url)

    def engines(self):
        """Output Engines"""
        for name in self.settings:
            print(name)

    def all(self, term):
        """Search using all defined search engines"""
        encoded_term = urllib.parse.quote_plus(term)
        reserved_keys = ("default", "browser")
        for key, values in self.settings.items():
            if key not in reserved_keys:
                self.browse(values + encoded_term)


if __name__ == "__main__":

    fire.Fire(WebSearch)
