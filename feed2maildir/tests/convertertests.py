#!/usr/bin/env python
# coding: utf-8

import json
import unittest

from feed2maildir.converter import Converter

class ConverterTestCase(unittest.TestCase):
    def setUp(self):
        # Construct something the reader is expected to spit out
        self.test = {
            'testblog': {
                'feed': {
                    'title': u'testblog',
                    'link': u'http://example.org',
                    'description': u'nothing to see here',
                    'published': u'Sat, 07 Sep 2002 00:00:01 GMT',
                    'published_parsed': (2002, 9, 7, 0, 0, 1, 5, 250, 0),
                },
                'entries': [
                    {
                        'title': u'post',
                        'author': u'sulami',
                        'link': u'http://example.org',
                        'published': u'Sat, 07 Sep 2002 00:00:01 GMT',
                        'published_parsed': (2002, 9, 7, 0, 0, 1, 5, 250, 0),
                        'description': u'this is a post',
                    },
                    {
                        'title': u'another post',
                        'author': u'sulami',
                        'link': u'http://example.org',
                        'published': u'Sun, 08 Sep 2002 00:00:01 GMT',
                        'published_parsed': (2002, 9, 8, 0, 0, 1, 5, 250, 0),
                        'description': u'this is another post',
                    },
                ],
            }
        }
        # Write it into a test db to compare against
        with open('/tmp/f2mtest', 'w') as f:
            f.write(json.dumps(self.test))

    def test_read_nonexistent_db(self):
        converter = Converter({}, db='/nothing')
        self.assertIsNone(converter.db)

    def test_read_invalid_db(self):
        with open('/tmp/gibber', 'w') as f:
            f.write('gibberish')
        converter = Converter({}, db='/tmp/gibber', silent=True)
        self.assertIsNone(converter.db)

    def test_read_valid_db(self):
        converter = Converter({}, db='/tmp/f2mtest')
        self.assertIsNotNone(converter.db)

    def test_convert_invalid_input(self):
        converter = Converter({'feed': 'gibberish'}, db='/tmp/f2mtest',
                              silent=True)
        self.assertEqual(len(converter.feeds), 0)

    def test_convert_valid_input(self):
        converter = Converter(self.test)
        self.assertEqual(len(converter.feeds), 1)
        self.assertEqual(len(converter.feeds['testblog']), 2)

if __name__ == '__main__':
    unittest.main()

