#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import time

from crawler.crawl import crawl_the_page, generate_ranklists
from crawler.logger import logger


def main():
    start = time.time()
    crawl_the_page('http://music.163.com/discover/playlist/')
    generate_ranklists()
    finish = time.time()
    logger.info('Update the site: use {0} seconds.'.format(finish - start))


if __name__ == '__main__':
    main()
