#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from pyspider.libs.base_handler import *


def get_number(raw):
    return int(re.search(r'\d+', raw).group())


class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://music.163.com/discover/playlist',
                   callback=self.index_page)

    @config(age=60 * 60)
    def index_page(self, response):
        for each in response.doc('a[href^="http://music.163.com/playlist?id="]').items():
            if '$' not in each.attr.href:
                self.crawl(each.attr.href, callback=self.detail_page)
        self.crawl(response.doc('.znxt').attr.href, callback=self.index_page)

    @config(priority=2)
    def detail_page(self, response):
        return {
            "url": response.url,
            "title": response.doc('h2').text(),
            "played": int(response.doc('strong').text()),
            "comments": get_number(response.doc('.j-cmt > i').text()),
            "shares": get_number(response.doc('.j-shr > i').text()),
            "favourites": get_number(response.doc('.j-fav > i').text()),
            "tags": response.doc('.u-tag > i').text().split()
        }
