#!/usr/bin/env python
# coding: utf-8

import unittest

import feed2maildir.loader

class LoaderTestCase(unittest.TestCase):
    def test_loader_reads_file(self):
        testfile = '/tmp/f2mrc'
        with open(testfile, 'w') as f:
            f.write('toast')
        loader = feed2maildir.loader.Loader(config=testfile)
        self.assertEqual(loader.config, 'toast')

if __name__ == '__main__':
    unittest.main()

