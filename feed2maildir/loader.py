import json
import os.path

class Loader:
    """Loads the config/list of feeds from a file"""

    def __init__(self, config='~/.f2mrc', silent=False):
        self.silent = silent

        try:
            with open(os.path.expanduser(config), 'r') as f:
                self.config = json.loads(f.read())
        except: # Use default config
            self.output('WARNING: could not open config "{}"'.format(config))
            self.config = {'feeds': {}, 'db': None, 'maildir': None}

    def output(self, arg):
        if not self.silent:
            print(arg)

