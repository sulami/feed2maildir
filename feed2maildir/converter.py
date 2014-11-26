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

    def __init__(self, db='~/.f2mdb', maildir='~/mail/feeds',
                 silent=False):
        self.silent = silent
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

    def load(self, feeds):
        """Load a list of feeds in feedparser-dict form"""
        self.feeds = feeds

    def find_new(self):
        """Find the new posts from within self.feeds by comparing to the db"""
        self.news = []
        newtimes = {}
        for feed in self.feeds:
            title = feed.feed.title
            try: # to find the last update time for the feed in the db
                oldtime = self.mktime(self.dbdata[title])
            except: # there is no record, mail all entries
                oldtime = None
            for entry in feed.entries:
                try: # to find the last update time for the post
                    time = entry.updated
                except:
                    try:
                        time = entry.published
                    except:
                        time = None
                dtime = self.mktime(time) if time else None
                if dtime > oldtime:
                    mail = TEMPLATE.format(time, entry.title,
                    title, entry.link, entry.description)
                    self.write(mail)
            newtimes[title] = feed.entries[-1].updated

        try: # to write the new database
            with open(self.db, 'w') as f:
                f.write(json.dumps(newtimes))
        except:
            self.output('WARNING: failed to write the new database')

    def writeout(self):
        """Write out self.news to a maildir"""
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

        # for feed in self.news:
        #     message = self.compose()
        #     self.write()

    def compose(self, post):
        """Compose the mail using the tempate"""
        return ''

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

