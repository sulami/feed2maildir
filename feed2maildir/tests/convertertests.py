#!/usr/bin/env python
# coding: utf-8

import json
import os
import shutil
import unittest

from feed2maildir.converter import Converter, HTMLStripper

class AttrDict(dict):
    """This is a dict that can be accessed via attributes, just like the
    Feedparser Dict"""

    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self

class ConverterTestCase(unittest.TestCase):
    def setUp(self):
        self.testfeed = AttrDict(
            feed=AttrDict(
                title=u'testblog',
                link=u'http://example.org',
                description=u'nothing to see here',
                updated=u'Sun, 08 Sep 2002 00:00:01 GMT',
                updated_parsed=(2002, 9, 7, 0, 0, 1, 5, 250, 0),
            ),
            entries=[
                AttrDict(
                    title=u'post',
                    author=u'sulami',
                    link=u'http://example.org',
                    updated=u'Sat, 07 Sep 2002 00:00:01 GMT',
                    published_parsed=(2002, 9, 7, 0, 0, 1, 5, 250, 0),
                    description=u'this is a post',
                ),
                AttrDict(
                    title=u'another post',
                    author=u'sulami',
                    link=u'http://example.org',
                    updated=u'Sun, 08 Sep 2002 00:00:01 GMT',
                    published_parsed=(2002, 9, 8, 0, 0, 1, 5, 250, 0),
                    description=u'this is another post',
                ),
            ],
        )
        self.test = [self.testfeed, ]

    def test_read_nonexistent_db(self):
        converter = Converter(db='/nothing')
        self.assertIsNone(converter.dbdata)

    def test_read_invalid_db(self):
        with open('/tmp/gibber', 'w') as f:
            f.write('gibberish')
        converter = Converter(db='/tmp/gibber', silent=True)
        self.assertIsNone(converter.dbdata)

    def test_read_valid_db(self):
        with open('/tmp/db', 'w') as f:
            f.write('{"somefeed": "1970-01-01 00:00:01 UTC"}')
        converter = Converter(db='/tmp/db')
        self.assertIsNotNone(converter.dbdata)

    def test_convert_valid_input(self):
        converter = Converter(db='/tmp/db')
        converter.load(self.test)
        self.assertEqual(len(converter.feeds), 1)
        self.assertEqual(len(converter.feeds[0]), 2)

    def test_fail_to_make_maildir(self):
        converter = Converter(maildir='/maildir', db='/tmp/db', silent=True)
        with self.assertRaises(SystemExit):
            converter.check_maildir('/maildir')
        self.assertFalse(os.access('/maildir', os.F_OK))

    def test_make_maildir(self):
        converter = Converter(maildir='/tmp/maildir', db='/tmp/db')
        self.assertFalse(os.access('/tmp/maildir', os.F_OK))
        converter.check_maildir('/tmp/maildir')
        self.assertTrue(os.access('/tmp/maildir', os.W_OK))
        self.assertTrue(os.access('/tmp/maildir/tmp', os.W_OK))
        self.assertTrue(os.access('/tmp/maildir/new', os.W_OK))
        self.assertTrue(os.access('/tmp/maildir/cur', os.W_OK))
        shutil.rmtree('/tmp/maildir') # Clean up
        self.assertFalse(os.access('/tmp/maildir', os.F_OK))

    def test_composer(self):
        converter = Converter(maildir='/tmp/maildir', db='/tmp/db')
        self.assertEqual(converter.compose(u'testblog',
            self.testfeed.entries[0]),
            (u'MIME-Version: 1.0\nDate: Sat, 07 Sep 2002 00:00:01 GMT\n'
            'Subject: post\nFrom: testblog\nContent-Type: text/plain\n'
            '\n[Feed2Maildir] Read the update here:\nhttp://example.org\n\n'
            'this is a post\n'))

    def test_mktime(self):
        from datetime import datetime, tzinfo
        converter = Converter(maildir='/tmp/maildir', db='/tmp/db')
        t = converter.mktime(u'Sun, 08 Sep 2002 00:00:01 GMT').replace(
            tzinfo=None) # datetime can't handle tzinfo
        tt = datetime.strptime('2002-09-08 00:00:01', '%Y-%m-%d %H:%M:%S')
        self.assertEqual(t, tt)

    def test_find_new_posts(self):
        converter = Converter(maildir='/tmp/maildir', db='/tmp/db')
        fauxdbdata = {u'testblog': u'Sun, 08 Sep 2002 00:00:04 GMT'}
        new = converter.find_new(self.test, fauxdbdata, writedb=False)
        self.assertEqual(len(new), 0)
        fauxdbdata = {u'testblog': u'Sat, 07 Sep 2002 00:00:01 GMT'}
        new = converter.find_new(self.test, fauxdbdata, writedb=False)
        self.assertEqual(len(new), 1)
        self.assertEqual(len(new[u'testblog']), 1)
        fauxdbdata = {u'testblog': u'Fri, 06 Sep 2002 00:00:01 GMT'}
        new = converter.find_new(self.test, fauxdbdata, writedb=False)
        self.assertEqual(len(new), 1)
        self.assertEqual(len(new[u'testblog']), 2)

    def test_find_update_time(self):
        from datetime import datetime
        converter = Converter(maildir='/tmp/maildir', db='/tmp/db')
        t = converter.find_update_time(self.testfeed).replace(tzinfo=None)
        tt = datetime.strptime('2002-09-08 00:00:01', '%Y-%m-%d %H:%M:%S')
        self.assertEqual(t, tt)

    def test_write_db(self):
        converter = Converter(maildir='/tmp/maildir', db='/tmp/db')
        try: # to delete what we are about to make
            os.remove('/tmp/fauxdb')
        except: # it is not there
            pass
        finally: # make sure is is not there
            self.assertFalse(os.access('/tmp/fauxdb', os.F_OK))
        fauxdbdata = {u'testblog': u'Sun, 08 Sep 2002 00:00:01 GMT'}
        converter.find_new(self.test, fauxdbdata, writedb=True,
                           dbfile='/tmp/fauxdb')
        with open('/tmp/fauxdb', 'r') as f:
            written = json.loads(f.read())
        desire = {u'testblog': u'2002-09-08 00:00:01 UTC'}
        self.assertEqual(written, desire)
        os.remove('/tmp/fauxdb')

    def test_html_stripper(self):
        teststring = """<!DOCTYPE html><html><head><title>test</title></head>
<body><h1>Header</h1>
<span class="foobar">content</span>
<img src="https://www.google.de//images/srpr/logo11w.png" /></body> </html>"""
        desire = """test\nHeader\ncontent
[Image]: https://www.google.de//images/srpr/logo11w.png\n """
        stripper = HTMLStripper()
        stripper.feed(teststring)
        out = stripper.get_data()
        self.assertEqual(out, desire)

if __name__ == '__main__':
    unittest.main()

