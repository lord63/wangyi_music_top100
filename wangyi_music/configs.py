#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import redis


class Config(object):
    redis_server = redis.StrictRedis(host='localhost', port=6379,
                                     decode_responses=True)


class DevelopConfig(Config):
    DEBUG = True
    CACHE_TYPE = 'null'


class ProductionConfig(Config):
    DEBUG = False
    CACHE_TYPE = 'redis'
