Feed2Maildir
============

Read RSS/Atom feeds in your favourite, maildir-compatible email client.

Requirements
------------

- Python 2.7+ / 3.2+
- ``feedparser``
- ``python-dateutil``

Usage
-----

Just run ``feed2maildir``, which should be placed in your $PATH by setup.py.
You will need a JSON configuration file at ``$HOME/.f2mrc`` that looks like
this:

.. code-block:: json

    {
        "db": "~/.f2mdb",
        "maildir": "~/mail/feeds",
        "feeds": {
            "Coding Horror": "http://feeds.feedburner.com/codinghorror/",
            "Commit Strip": "http://www.commitstrip.com/en/feed/",
            "XKCD": "http://xkcd.com/rss.xml",
            "What If?": "http://what-if.xkcd.com/feed.atom",
            "Dilbert": "http://feed.dilbert.com/dilbert/daily_strip?format=xml",
            "BSDNow": "http://feeds.feedburner.com/BsdNowOgg"
        }
    }

Note that the last element in a dict may not be followed by a comma, because
Python's json.loads() says so.

There are a bunch of command-line arguments to overwrite the config file:

::

    optional arguments:
        -h, --help  show this help message and exit
        -c <file>   override the config file location (~/.f2mrc)
        -d <file>   override the database file location (~/.f2mdb)
        -m <dir>    override the maildir location (None)

To check for updates regularly, just toss it into cron to run once every hour
or so.

Currently, there are a bunch of features missing, most prominently HTML
parsing, that are planned to be added in the near future.

