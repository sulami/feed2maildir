import feedparser

class Reader:
    """Get updates on the feeds supplied"""

    def __init__(self, feeds, silent=False):
        self.feeds = []
        self.silent = silent
        for feed in feeds:
            f = feedparser.parse(feeds[feed])
            if f.bozo:
                self.output('WARNING: could not parse feed {}'.format(feed))
            else:
                f.feed_alias_name = feed # user provided text
                self.feeds.append(f)

    def output(self, arg):
        if not self.silent:
            print(arg)

