#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    crawler/worker.py
    ~~~~~~~~~~~~~~~~

    I work hard and help maintain the songlists. The mianly tasks are:

    * fetch new songlists by travelling all over the songlists in the site
    * update the songlists everyday to keep them healthy and fresh
"""

from __future__ import absolute_import

from functools import reduce

from crawler import config
from crawler import crawler
from crawler import database


class Worker(object):
    def __init__(self):
        self.redis = config.redis_server
        self.crawler = crawler.Crawler()
        self.database = database.Database()

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
            [self.database.comments_ranklist,
             self.database.palys_ranklist,
             self.database.favourites_ranklist,
             self.database.shares_ranklist]
        )

        for songlist in self.database.songlists:
            if songlist not in toplist:
                self.redis.delete(songlist)

        self.redis.delete('wangyi:songlists')
        self.redis.lpuash('wangyi:songlists', *toplist)

    def update_all_songlists(self):
        self.crawler.crawl_the_site()
        self.database.set_update_time()

    def update_top_list(self):
        for songlist in self.database.songlists:
            url = self.redis.hget(songlist, 'url')
            self.crawler.crawl_one_songlist(url)
        self.database.set_update_time()
