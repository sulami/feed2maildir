import datetime
import json
import os
import random
import sys

# Python 2.x compabitlity
if sys.version[0] == '2':
    FileNotFoundError = IOError

TEMPLATE = u"""MIME-Version: 1.0
Date: {}
Subject: [{}] {}
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

        inval = []
        for feed, content in self.feeds.items():
            try: # to validate the feeds, access some essential keys
                content['feed']['title']
                content['feed']['link']
                content['feed']['updated']
            except:
                self.output('WARNING: feed {} seems to be broken'.format(feed))
                inval.append(feed)
        for i in inval: # pop invalid feeds
            self.feeds.pop(i)

    def writeout(self):
        """Check which updates need to be written to the maildir"""
        if not os.access(self.maildir, os.W_OK):
            try: # to make the maildir
                os.mkdir(self.maildir)
                os.mkdir('{}/tmp'.format(self.maildir))
                os.mkdir('{}/new'.format(self.maildir))
                os.mkdir('{}/cur'.format(self.maildir))
            except:
                sys.exit('ERROR: accessing "{}" failed'.format(self.maildir))

        newtimes = {}
        for feed, content in self.feeds.items():
            try: # to find the last update time for the feed in the db
                pubdate = self.mktime(self.dbdata[feed])
            except: # there is no record, mail all entries
                pubdate = None
            for entry in content['entries']:
                time = self.mktime(entry['published'])
                if not pubdate or time > pubdate:
                    mail = TEMPLATE.format(entry['published'],
                    entry['author'], entry['title'], feed, entry['link'],
                    entry['description'])
                    self.write(mail)
                if feed not in newtimes or time > self.mktime(newtimes[feed]):
                    newtimes[feed] = entry['published']

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
        # This is due to the fantastic built-in strptime >.<
        return datetime.datetime.strptime(' '.join(arg.split(' ')[0:5]),
                                          '%a, %d %b %Y %X')

    def output(self, arg):
        if not self.silent:
            print(arg)

