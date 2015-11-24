#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import logging
import logging.config
from os import path

import yaml


def create_logger(logger_name):
    directory_root = path.dirname(path.realpath(__file__))
    with open(path.join(directory_root, 'logging.yaml')) as f:
        logging_config = yaml.load(f)
    logging.config.dictConfig(logging_config)
    logger = logging.getLogger(logger_name)
    return logger
