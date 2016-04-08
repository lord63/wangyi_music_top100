#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

from flask import render_template, Blueprint

from wangyi_music.configs import Config
from wangyi_music.cache import cache


wangyi = Blueprint('wangyi', __name__)
redis_server = Config.redis_server


@wangyi.route('/')
@wangyi.route('/sortby/<any(plays, favourites, shares, comments):sorted_key>')
@cache.cached(timeout=3600)
def index(sorted_key='plays'):
    ranklist = "wangyi:ranklist:{0}".format(sorted_key)
    songlists = redis_server.lrange(ranklist, 0, -1)
    latest_update = redis_server.get('wangyi:latest_update')
    top100 = [redis_server.hgetall(songlist) for songlist in songlists]
    return render_template('index.html', top100=top100,
                           latest_update=latest_update)
