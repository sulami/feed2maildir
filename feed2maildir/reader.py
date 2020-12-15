import feedparser
from multiprocessing.pool import ThreadPool

def fetch_and_parse_feed(args):
    name, feed = args
    return (name, feedparser.parse(feed))

class Reader:
    """Get updates on the feeds supplied"""

    def __init__(self, feeds, silent=False, njobs=4):
        self.feeds = []
        self.silent = silent
        with ThreadPool(processes=njobs) as pool:
            for feed, f in pool.imap_unordered(fetch_and_parse_feed, feeds.items()):
                if f.bozo:
                    self.output('WARNING: could not parse feed {}'.format(feed))
                else:
                    f.feed_alias_name = feed # user provided text
                    self.feeds.append(f)

    def output(self, arg):
        if not self.silent:
            print(arg)

