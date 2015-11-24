#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import os

from flask_script import Manager

from wangyi_music.app import create_app
from wangyi_music.configs import DevelopConfig, ProductionConfig


if os.environ.get('Flask_APP') == 'production':
    app = create_app(ProductionConfig)
else:
    app = create_app(DevelopConfig)

manager = Manager(app)


if __name__ == '__main__':
    manager.run()
