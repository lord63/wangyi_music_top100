#!/usr/bin/env python
# -*- coding: utf-8 -*-


from __future__ import absolute_import

import re

import requests
from lxml import html
import redis


class Songlist(object):
    def __init__(self, url):
        self.url = url
        self.tree = html.fromstring(requests.get(url).text)

    def _get_num(self, css_expression):
        text_in_tag = self.tree.cssselect(css_expression)[0].text
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
        return self._get_num('.u-btni-cmmt i')

    @property
    def shares(self):
        return self._get_num('.u-btni-share i')

    @property
    def favourites(self):
        return self._get_num('.u-btni-fav i')

    @property
    def tags(self):
        if self.tree.cssselect('.tags'):
            tags = [tag.text for tag in self.tree.cssselect('.u-tag i')]
            return tags
        else:
            return []

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


class Crawler(object):
    def __init__(self):
        self.redis_server = redis.StrictRedis(host='localhost', port=6379)
        self.base_url = 'http://music.163.com'

    def crawl_one_songlist(self, songlist_url):
        songlist = Songlist(songlist_url)
        key = 'wangyi:songlist:{0}'.format(songlist.songlist_id)
        self.redis_server.hmset(key, songlist.meta)
        if key not in self.redis_server.lrange('wangyi:songlists', 0, -1):
            self.redis_server.lpush('wangyi:songlists', key)

    def crawl_one_page(self, page_url):
        tree = html.fromstring(requests.get(page_url).text)
        songlists = tree.cssselect('.u-cover > a')
        for songlist in songlists:
            self.crawl_one_songlist(self.base_url + songlist.get('href'))
        next_page = tree.cssselect('.znxt')[0].get('href')
        if next_page == 'javascript:void(0)':
            return None
        else:
            return self.base_url + next_page

    def crawl_the_site(self,
                       start_url='http://music.163.com/discover/playlist'):
        next_page = self.crawl_one_page(start_url)
        while next_page is not None:
            next_page = self.crawl_one_page(next_page)


    def update(self):
        pass
