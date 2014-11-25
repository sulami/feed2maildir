import feedparser

class Reader:
    """Get updates on the feeds supplied"""

    def __init__(self, feeds):
        self.feeds = {}
        for feed in feeds:
            try:
                self.feeds[feed] = feedparser.parse(feeds[feed])
            except:
                self.output('WARNING: could not parse feed {}'.format(feed))
                continue

