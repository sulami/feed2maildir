import json
import os.path
import sys

# Python 2.x compabitlity
if sys.version[0] == '2':
    FileNotFoundError = IOError

class Converter:
    """Compares the already parsed feeds and converts new ones to maildir"""

    def __init__(self, feeds, db='~/.f2mdb', silent=False):
        self.silent = silent
        self.feeds = feeds

        try:
            with open(os.path.expanduser(db), 'r') as f:
                self.db = json.loads(f.read())
        except FileNotFoundError:
            self.db = None
        except ValueError:
            self.output('WARNING: database is malformed and will be ignored')
            self.db = None

        inval = []
        for feed, content in self.feeds.items():
            try: # validation, access some essential keys
                content['feed']['title']
                content['feed']['link']
                content['feed']['published']
            except:
                self.output('WARNING: feed {} seems to be broken'.format(feed))
                inval.append(feed)
        for i in inval: # pop invalid feeds
            self.feeds.pop(i)

    def output(self, arg):
        if not self.silent:
            print(arg)

