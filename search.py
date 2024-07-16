#!/usr/bin/env python3
"""Quick searching from command line"""

import os
import fire
import subprocess
import toml


class WebSearch:
    """Simple Websearch CLI"""

    def __init__(self, engine="default"):
        """Init"""
        script_path = os.path.dirname(os.path.abspath(__file__))
        self.settings = toml.load(os.path.join(script_path, "searchIt.toml"))
        self.default_url = self.settings[self.settings["default"]]

        if engine == "default":
            self.engine = self.settings[engine]
        else:
            self.engine = engine
        self.search_url = self.settings.get(self.engine, self.default_url)
        self.wsl = os.path.exists("/etc/wsl.conf")
        self.wslBrowser = "/mnt/c/Program Files/Mozilla Firefox/firefox.exe"

    def browse(self, url):
        if self.wsl:
            command = "\""+ self.wslBrowser + "\" \"" + url + "\""
            subprocess.Popen(command, shell=True)
        else:
            webbrowser.open(url)

    #def search(self, term=pyperclip.paste()):
    def search(self, term):
        """Search passed term"""
        url = self.search_url + term
        self.browse(url)

    def engines(self):
        """Output Engines"""
        for name in self.settings:
            print(name)

    def all(self, term):
        """Search using all defined search engines"""
        for key, values in self.settings.items():
            if key != "default":
                webbrowser.open(values + term)


if __name__ == "__main__":

    fire.Fire(WebSearch)
