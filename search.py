#!/usr/bin/env python3
'''Quick searching from command line'''

import webbrowser
import os
import fire
import pyperclip
import toml

class WebSearch:
    """Simple Websearch CLI"""

    def __init__(self, engine='default'):
        """Init"""
        script_path = os.path.dirname(os.path.abspath(__file__))
        self.settings = toml.load(os.path.join(script_path, "searchIt.toml"))

        if engine == 'default':
            self.engine = self.settings[engine]
        else:
            self.engine = engine
        self.search_url = self.settings[self.engine]

    def search(self, term=pyperclip.paste()):
        """Search"""
        webbrowser.open(self.search_url + term)

    def engines(self):
        """Output Engines"""
        for name in self.settings:
            print(name)


if __name__ == '__main__':

    fire.Fire(WebSearch)
