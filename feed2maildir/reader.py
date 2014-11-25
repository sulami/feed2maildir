import feedparser

class Reader:
    """Get updates on the feeds supplied"""

    def __init__(self, feeds):
        self.feeds = {}
        for feed in feeds:
            self.feeds[feed] = feedparser.parse(feeds[feed])

