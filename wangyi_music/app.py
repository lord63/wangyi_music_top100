#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

from flask import Flask

from wangyi_music.cache import cache
from wangyi_music.index import wangyi


def create_app(config):
    app = Flask('wangyi_music')

    app.config.from_object(config)
    cache.init_app(app)
    app.register_blueprint(wangyi)

    return app
