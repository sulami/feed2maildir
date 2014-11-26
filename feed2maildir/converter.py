import datetime
import json
import os
import random
import sys

import dateutil.parser

# Python 2.x compabitlity
if sys.version[0] == '2':
    FileNotFoundError = IOError

TEMPLATE = u"""MIME-Version: 1.0
Date: {}
Subject: {}
From: {}
Content-Type: text/plain

[Feed2Maildir] Read the update here:
{}

{}
"""

class Converter:
    """Compares the already parsed feeds and converts new ones to maildir"""

    def __init__(self, feeds, db='~/.f2mdb', maildir='~/mail/feeds',
                 silent=False):
        self.silent = silent
        self.feeds = feeds
        self.maildir = os.path.expanduser(maildir)
        self.db = os.path.expanduser(db)

        try: # to read the database
            with open(self.db, 'r') as f:
                self.dbdata = json.loads(f.read())
        except FileNotFoundError:
            self.dbdata = None
        except ValueError:
            self.output('WARNING: database is malformed and will be ignored')
            self.dbdata = None

    def writeout(self):
        """Check which updates need to be written to the maildir"""
        if (not os.access(self.maildir, os.W_OK)
            or not os.access(self.maildir + '/tmp', os.W_OK)
            or not os.access(self.maildir + '/new', os.W_OK)
            or not os.access(self.maildir + '/cur', os.W_OK)):
            try: # to make the maildir
                os.mkdir(self.maildir)
                os.mkdir('{}/tmp'.format(self.maildir))
                os.mkdir('{}/new'.format(self.maildir))
                os.mkdir('{}/cur'.format(self.maildir))
            except:
                sys.exit('ERROR: accessing "{}" failed'.format(self.maildir))

        newtimes = {}
        for feed in self.feeds:
            title = feed.feed.title
            try: # to find the last update time for the feed in the db
                pubdate = self.mktime(self.dbdata[title])
            except: # there is no record, mail all entries
                pubdate = None
            for entry in feed.entries:
                try:
                    time = entry.updated
                except:
                    try:
                        time = entry.published
                    except:
                        pass
                if time:
                    dtime = self.mktime(time)
                if not pubdate or dtime > pubdate:
                    mail = ''
                    try:
                        mail = TEMPLATE.format(time, entry.title,
                        feed, entry.link, entry.description)
                    except:
                        print(feed, entry)
                    self.write(mail)
                if (feed not in newtimes
                    or dtime > self.mktime(newtimes[title])):
                    newtimes[title] = time

        try: # to write the new database
            with open(self.db, 'w') as f:
                f.write(json.dumps(newtimes))
        except:
            self.output('WARNING: failed to write the new database')

    def write(self, message):
        """Take a message and write it to a mail"""
        rand = str(random.randint(10000, 99999))
        dt = str(datetime.datetime.now())
        pid = str(os.getpid())
        host = os.uname()[1]
        name = u'{}/new/{}{}{}{}'.format(self.maildir, rand, dt, pid, host)
        try: # to write out the message
            with open(name, 'w') as f:
                # We can thank the P2/P3 unicode madness for this...
                if sys.version[0] == '2':
                    f.write(str(message.encode('utf8')))
                else:
                    f.write(message)
        except:
            self.output('WARNING: failed to write message to file')

    def mktime(self, arg):
        """Make a datetime object from a time string"""
        return dateutil.parser.parse(arg)

    def output(self, arg):
        if not self.silent:
            print(arg)

