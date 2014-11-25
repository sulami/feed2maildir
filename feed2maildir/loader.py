class Loader:
    """Loads the config/list of feeds from a file"""

    def __init__(self, config='~/.f2mrc'):
        with file(config, 'r') as f:
            self.config = f.read()

