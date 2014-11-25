#!/usr/bin/env python
# coding: utf-8

import json
import unittest

import feed2maildir.converter

class ConverterTestCase(unittest.TestCase):
    def test_db_does_not_exist(self):
        converter = feed2maildir.converter.Converter('fds', db='/nothing')
        self.assertIsNone(converter.db)

    def test_db_is_gibberish(self):
        with open('/tmp/toast', 'w') as f:
            f.write('gibberish')
        converter = feed2maildir.converter.Converter('fds', db='/tmp/toast',
                                                     silent=True)
        self.assertIsNone(converter.db)

    def test_convert_data(self):
        test = {'test': {
                    'feed': {
                        'title': u'blog',
                        'link': u'http://example.org',
                        'description': 'nothing to see here',
                        'published': 'Sat, 07 Sep 2002 00:00:01 GMT',
                        'published_parsed': (2002, 9, 7, 0, 0, 1, 5, 250, 0),
                    }
                } }
        with open('/tmp/toast', 'w') as f:
            f.write(json.dumps(test))
        converter = feed2maildir.converter.Converter('fds', db='/tmp/toast')
        self.assertIsNotNone(converter.db)

if __name__ == '__main__':
    unittest.main()

