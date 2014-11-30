import datetime
import json
import os
import random
import sys

import dateutil.parser

# Python 2.x compabitlity
if sys.version[0] == '2':
    FileNotFoundError = IOError

class Converter:
    """Compares the already parsed feeds and converts new ones to maildir"""

    TEMPLATE = u"""MIME-Version: 1.0
Date: {}
Subject: {}
From: {}
Content-Type: text/plain

[Feed2Maildir] Read the update here:
{}

{}
"""

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

    def run(self):
        """Do a full run"""
        if self.feeds:
            self.check_maildir(self.maildir)
            self.news = self.find_new(self.feeds, self.dbdata)
            for newfeed in self.news:
                for newpost in newfeed:
                    self.write(self.compose(newfeed, newpost))

    def load(self, feeds):
        """Load a list of feeds in feedparser-dict form"""
        self.feeds = feeds

    def find_new(self, feeds, db, writedb=True, dbfile=None):
        """Find the new posts by comparing them to the db, by default
        refreshing the db"""
        new = {}
        newtimes = {}
        for feed in feeds:
            feedname = feed.feed.title
            try: # to get the update time from the feed itself
                feedup = self.mktime(feed.feed.updated)
            except: # there is no info, then find it in the posts
                feedup = self.find_update_time(feed)
            try: # to localize the timezone
                feedup = feedup.astimezone(dateutil.tz.tzutc())
            except: # it is naive, force UTC
                feedup = feedup.replace(tzinfo=dateutil.tz.tzutc())
            try: # to find the old update time in the db
                oldtime = self.mktime(db[feedname]).astimezone(
                            dateutil.tz.tzutc())
            except: # it is not there
                oldtime = None
            if oldtime and not oldtime.tzinfo: # force UTC
                oldtime = oldtime.replace(tzinfo=dateutil.tz.tzutc())
            # print(feedname, feedup.tzinfo)
            if not oldtime or oldtime < feedup:
                for post in feed.entries:
                    feedtime = self.mktime(post.updated)
                    try: # to localize the timezone
                        feedtime = feedtime.astimezone(dateutil.tz.tzutc())
                    except: # it is naive
                        feedtime = feedtime.replace(tzinfo=dateutil.tz.tzutc())
                    if not oldtime or oldtime < feedtime:
                        try: # to append the post the the feed-list
                            new[feedname].append(post)
                        except: # it is the first one, make a new list
                            new[feedname] = [post, ]
            if writedb:
                newtimes[feedname] = feedup.strftime('%Y-%m-%d %H:%M:%S %Z')

        if writedb:
            if not dbfile: # use own dbfile as default
                dbfile = self.db
            try: # to write the new database
                with open(dbfile, 'w') as f:
                    f.write(json.dumps(newtimes))
            except:
                self.output('WARNING: failed to write the new database')

        return new

    def find_update_time(self, feed):
        """Find the last updated post in a feed"""
        times = []
        for post in feed.entries:
            times.append(self.mktime(post.updated))
        return sorted(times)[-1]

    def check_maildir(self, maildir):
        """Check access to the maildir and try to create it if not present"""
        mdirs = ('', '/tmp', '/new', '/cur')
        for mdir in mdirs:
            fullname = maildir + mdir
            if not os.access(fullname, os.W_OK):
                try: # to make the maildirs
                    os.mkdir(fullname)
                except:
                    sys.exit('ERROR: accessing "{}" failed'.format(fullname))

    def compose(self, title, post):
        """Compose the mail using the tempate"""
        try: # to get the update/publish time from the post
            updated = post.updated
        except: # the property is not set, use now()
            updated = datetime.datetime.now()
        return self.TEMPLATE.format(updated, post.title, title, post.link,
                                    post.description)

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

