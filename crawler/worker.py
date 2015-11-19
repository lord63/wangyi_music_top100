#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    crawler/worker.py
    ~~~~~~~~~~~~~~~~

    I work hard and help maintain the songlists. The mianly tasks including:

    * fetch new songlists by travelling all over the songlists in the site
    * update the songlists everyday to keep them healthy and fresh
"""

import datetime
from functools import reduce

from crawler.crawler import Crawler
from crawler import config


class Worker(object):
    def __init__(self):
        self.redis = config.redis_server
        self.crawler = Crawler()

    def generate_rank_lists(self):
        keywords = ['comments', 'plays', 'favourites', 'shares']
        for keyword in keywords:
            self._generate_rank_list_by_keyword(keyword)

    def _generate_rank_list_by_keyword(self, keyword):
        sort_by = 'wangyi:songlist:*->{0}'.format(keyword)
        store_to = 'wangyi:ranklist:{0}'.format(keyword)
        self.redis.sort('wangyi:songlists', start=0, num=100,
                        by=sort_by, store=store_to, desc=True)

    def generate_top_list(self):
        toplist = reduce(
            lambda x, y: set(x).union(set(y)),
            [self.redis.lrange('wangyi:ranklist:comments', 0, -1),
             self.redis.lrange('wangyi:ranklist:plays', 0, -1),
             self.redis.lrange('wangyi:ranklist:favourites', 0, -1),
             self.redis.lrange('wangyi:ranklist:shares', 0, -1)
            ]
        )

        for songlist in self.redis.lrange('wangyi:songlists', 0, -1):
            if songlist not in toplist:
                self.redis.delete(songlist)

        self.redis.delete('wangyi:songlists')
        self.redis.lpuash('wangyi:songlists', *toplist)

    def update_all_songlists(self):
        self.crawler.crawl_the_site()
        self.redis.set('wangyi:latest_update',
                       datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'))

    def update_top_list(self):
        for songlist in self.redis.lrange('wangyi:songlists', 0, -1):
            url = self.redis.hget(songlist, 'url')
            self.crawler.crawl_one_songlist(url)
        self.redis.set('wangyi:latest_update',
                       datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'))
