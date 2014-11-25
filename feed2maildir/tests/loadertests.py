#!/usr/bin/env python
# coding: utf-8

import json
import unittest

import feed2maildir.loader

class LoaderTestCase(unittest.TestCase):
    def test_loader_reads_file(self):
        testfile = '/tmp/f2mrc'
        testfeeds = {'feeds': {'Feed #1': 'someurl', 'Feed #2': 'anotherurl'}}
        with open(testfile, 'w') as f:
            f.write(json.dumps(testfeeds))
        loader = feed2maildir.loader.Loader(config=testfile)
        self.assertEqual(loader.config['feeds']['Feed #1'], 'someurl')
        self.assertEqual(loader.config['feeds']['Feed #2'], 'anotherurl')

    def test_loader_uses_default_config(self):
        loader = feed2maildir.loader.Loader(config='/tmp/nothing', silent=True)
        self.assertEqual(loader.config['feeds'], {})

if __name__ == '__main__':
    unittest.main()

