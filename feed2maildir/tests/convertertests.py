#!/usr/bin/env python
# coding: utf-8

import json
import os
import shutil
import unittest

from feed2maildir.converter import Converter

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
            converter.writeout()
        self.assertFalse(os.access('/maildir', os.F_OK))

    def test_make_maildir(self):
        converter = Converter(maildir='/tmp/maildir', db='/tmp/db')
        converter.writeout()
        self.assertTrue(os.access('/tmp/maildir', os.F_OK))
        self.assertTrue(os.access('/tmp/maildir/tmp', os.F_OK))
        self.assertTrue(os.access('/tmp/maildir/new', os.F_OK))
        self.assertTrue(os.access('/tmp/maildir/cur', os.F_OK))
        shutil.rmtree('/tmp/maildir')

    def test_composer(self):
        converter = Converter(maildir='/tmp/maildir', db='/tmp/db')
        self.assertEqual(converter.compose(u'testblog',
            self.testfeed.entries[0]),
            (u'MIME-Version: 1.0\nDate: Sat, 07 Sep 2002 00:00:01 GMT\n'
            'Subject: post\nFrom: testblog\nContent-Type: text/plain\n'
            '\n[Feed2Maildir] Read the update here:\nhttp://example.org\n\n'
            'this is a post\n'))

    def test_find_new_posts(self):
        converter = Converter(maildir='/tmp/maildir', db='/tmp/db')
        new = converter.find_new([], [])
        self.assertEqual(new, None)

if __name__ == '__main__':
    unittest.main()

