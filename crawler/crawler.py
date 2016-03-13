#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    crawler/crawler.py
    ~~~~~~~~~~~~~~~~~~

    Yeah, I'm a crawler. I can crawl a songlist, or one page of songlists or
    crawl all the songlist. I'm at your service.
"""


from __future__ import absolute_import

import re

import requests
from lxml import html

from crawler import config
from crawler import logger
from crawler.celery import celery_app


class Songlist(object):
    def __init__(self, url):
        self.url = url
        self.tree = html.fromstring(requests.get(url).text)

    def _get_num(self, css_expression):
        text_in_tag = self.tree.cssselect(css_expression)[0].text_content()
        matched_num = re.search(r'\d+', text_in_tag)
        if matched_num is None:
            return 0
        num = int(matched_num.group())
        return num

    @property
    def name(self):
        return self.tree.cssselect('h2')[0].text

    @property
    def songlist_id(self):
        return int(re.search(r'(?<=id=)\d+$', self.url).group())

    @property
    def plays(self):
        return int(self.tree.cssselect('#play-count')[0].text)

    @property
    def comments(self):
        text_in_tag = self.tree.cssselect('.u-btni-cmmt i')[0].text_content()
        matched_num = re.search(r'\d+', text_in_tag)
        if matched_num is None:
            return 0
        num = int(matched_num.group())
        return num

    @property
    def shares(self):
        return int(self.tree.cssselect('.u-btni-share')[0].get('data-count'))

    @property
    def favourites(self):
        return int(self.tree.cssselect('.u-btni-fav')[0].get('data-count'))

    @property
    def tags(self):
        if self.tree.cssselect('.tags'):
            tags = [tag.text for tag in self.tree.cssselect('.u-tag i')]
            return ', '.join(tags)
        else:
            return ''

    @property
    def meta(self):
        songlist_meta = {
            'name': self.name,
            'id': self.songlist_id,
            'url': self.url,
            'plays': self.plays,
            'comments': self.comments,
            'shares': self.shares,
            'favourites': self.favourites,
            'tags': self.tags
        }
        return songlist_meta


REDIS_SERVER = config.redis_server
LOGGER = logger.create_logger('crawler')


@celery_app.task
def crawl_one_songlist(songlist_url):
    songlist = Songlist(songlist_url)

    key = 'wangyi:songlist:{0}'.format(songlist.songlist_id)
    REDIS_SERVER.hmset(key, songlist.meta)
    LOGGER.info('Crawled songlist: {0}'.format(songlist_url))

    if key not in REDIS_SERVER.lrange('wangyi:songlists', 0, -1):
        REDIS_SERVER.lpush('wangyi:songlists', key)


def crawl_one_page(page_url):
    LOGGER.info('Start to crawl the page: {0}'.format(page_url))
    tree = html.fromstring(requests.get(page_url).text)
    songlists = tree.cssselect('.u-cover > a')
    for songlist in songlists:
        crawl_one_songlist.delay('http://music.163.com' + songlist.get('href'))
    LOGGER.info('The page: {0} has been crawled'.format(page_url))

    next_page = tree.cssselect('.znxt')[0].get('href')
    if next_page == 'javascript:void(0)':
        return None
    else:
        return 'http://music.163.com' + next_page


def crawl_the_site(start_url):
    LOGGER.info('Start to crawl the site from: {0}'.format(start_url))
    next_page = crawl_one_page(start_url)
    while next_page is not None:
        next_page = crawl_one_page(next_page)
    LOGGER.info(
        'Finish crawling the site from: {0}'.format(start_url))
