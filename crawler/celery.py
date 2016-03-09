#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

from celery import Celery


celery_app = Celery('crawler')
celery_app.config_from_object('crawler.celeryconfig')
