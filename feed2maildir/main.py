#!/usr/bin/env python
# coding: utf-8

from feed2maildir.loader import Loader
from feed2maildir.reader import Reader

def main():
    loader = Loader()
    config = loader.config
    reader = Reader(config['feeds'])
    return 0

if __name__ == '__main__':
    main()

