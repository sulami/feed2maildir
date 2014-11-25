#!/usr/bin/env python
# coding: utf-8

import unittest

import feed2maildir

class mainTestCase(unittest.TestCase):
    def test_returns_zero(self):
        self.assertEqual(feed2maildir.main(), 0)

if __name__ == '__main__':
    unittest.main()

