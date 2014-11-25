#!/usr/bin/env python
# coding: utf-8

import unittest

import feed2maildir.reader

class ReaderTestCase(unittest.TestCase):
    def test_read_no_feeds(self):
        testfeed = {}
        reader = feed2maildir.reader.Reader(testfeed)
        self.assertEqual(reader.feeds, {})

    def test_read_some_raw_data(self):
        testfeed = {'Blog': """<rss version="2.0">
                               <channel>
                               <title>Toast</title>
                               </channel>
                               </rss>"""}
        reader = feed2maildir.reader.Reader(testfeed)
        self.assertEqual(reader.feeds['Blog']['feed']['title'], 'Toast')

if __name__ == '__main__':
    unittest.main()

