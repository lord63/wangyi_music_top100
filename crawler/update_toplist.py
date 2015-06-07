#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import time

from crawler.crawl import update_toplist, generate_ranklists
from crawler.logger import logger


def main():
    start = time.time()
    update_toplist()
    generate_ranklists()
    finish = time.time()
    logger.info('Update toplist: use {0} seconds.'.format(finish - start))


if __name__ == '__main__':
    main()
