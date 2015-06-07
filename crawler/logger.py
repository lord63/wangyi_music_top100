#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import logging
import logging.config
from os import path

import yaml


with open(path.join(path.abspath(path.dirname(__file__)),
          'logging.yaml')) as f:
    logging_config = yaml.load(f)
logging.config.dictConfig(logging_config)
logger = logging.getLogger('crawler')
