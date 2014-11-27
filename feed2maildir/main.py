#!/usr/bin/env python
# coding: utf-8

from feed2maildir.converter import Converter
from feed2maildir.loader import Loader
from feed2maildir.reader import Reader

def main():
    loader = Loader()
    config = loader.config
    reader = Reader(config['feeds'])
    converter = Converter(db=config['db'], maildir=config['maildir'])
    converter.load(reader.feeds)
    converter.run()

if __name__ == '__main__':
    main()

