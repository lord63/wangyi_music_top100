#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    crawler/config.py
    ~~~~~~~~~~~~~~~~~

    some configurations for the crawler, e.g. the redis server
"""

from __future__ import absolute_import

import redis


redis_server = redis.StrictRedis(host='localhost', port=6379, db=1)
