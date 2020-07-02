Feed2Maildir
============

Read RSS/Atom feeds in your favourite, maildir-compatible email client.

.. image:: https://img.shields.io/pypi/v/feed2maildir.svg?style=flat-square
    :target: https://pypi.python.org/pypi/feed2maildir

.. image:: https://img.shields.io/pypi/dm/feed2maildir.svg?style=flat-square
    :target: https://pypi.python.org/pypi/feed2maildir

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

Note that the last element in a dict must not be followed by a comma, because
Python's json.loads() says so.

There are a bunch of command-line arguments to overwrite the config file:

::

    optional arguments:
        -h, --help  show this help message and exit
        -c <file>   override the config file location (~/.f2mrc)
        -d <file>   override the database file location (~/.f2mdb)
        -m <dir>    override the maildir location (None)
        -s          strip HTML from the feeds
        -S <prog>   strip HTML from the feeds using an external program
        -l          just write the links without the update

To check for updates regularly, just toss it into cron to run once every hour
or so.

Strip HTML
----------

``feed2maildir`` can strip the HTML tags from the feed using a built-in HTML
stripper (option ``-s``) or using an external program (option ``-S <prog>``)

In this last case, the program must read the HTML from it standard input and
return it stripped via the standard output.

The ``<prog>`` can be the name of a program or it can be a full shell command.
In that case don't forget to quote the full command.

Here is an example of using ``pandoc`` to convert HTML to Markdown

::

    feed2maildir -S 'pandoc --from html --to markdown_strict'

