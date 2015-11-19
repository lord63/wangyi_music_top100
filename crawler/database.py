#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    crawler/database.py
    ~~~~~~~~~~~~~~~~~~~

    provide some convenient ways to get data and communicate with
    the redis server
"""

from __future__ import absolute_import

import datetime

from crawler import config


class Database(object):
    def __init__(self):
        self.redis = config.redis_server

    def set_update_time(self):
        self.redis.set('wangyi:latest_update',
                       datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'))

    @property
    def songlists(self):
        return self.redis.lrange('wangyi:songlists', 0, -1)

    @property
    def comments_ranklist(self):
        return self.redis.lrange('wangyi:ranklist:comments', 0, -1)

    @property
    def palys_ranklist(self):
        return self.redis.lrange('wangyi:ranklist:plays', 0, -1)

    @property
    def favourites_ranklist(self):
        return self.redis.lrange('wangyi:ranklist:favourites', 0, -1)

    @property
    def shares_ranklist(self):
        return self.redis.lrange('wangyi:ranklist:shares', 0, -1)
