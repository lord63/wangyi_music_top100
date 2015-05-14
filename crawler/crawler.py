#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

import requests
from lxml import html
import redis

redis_server = redis.StrictRedis(host='localhost', port=6379)


def extract_num(raw):
    """Extract num from the unicode string."""
    matched = re.search(r'\d+', raw).group()
    return matched


def update_toplist():
    """Upadate songlists in the toplist."""
    for songlist in redis_server.lrange('toplist', 0, -1):
        crawl_detailed_page(redis_server.hget(songlist, 'url'))


def crawl_detailed_page(url):
    """Get info from the songlist page."""
    response = requests.get(url)
    tree = html.fromstring(response.text)
    filter_num = int(redis_server.get('filter_num')) or 0

    played = extract_num(tree.cssselect('strong')[0].text)
    if played < filter_num:
        return
    key = 'wangyi:' + re.search(r'(?<=id=)\d+$', url).group()
    title = tree.cssselect('h2')[0].text
    comments = extract_num(tree.cssselect('.u-btni-cmmt i')[0].text)
    shares = extract_num(tree.cssselect('.u-btni-share i')[0].text)
    favourites = extract_num(tree.cssselect('.u-btni-fav i')[0].text)
    if tree.cssselect('.tags'):
        tags = ' '.join([item.text for item in tree.cssselect('.u-tag i')])
    else:
        tags = ''

    result = {"title": title,
              "url": url,
              "played": played,
              "comments": comments,
              "shares": shares,
              "favourites": favourites,
              "tags": tags}

    redis_server.rpush('songlists', key)
    redis_server.hmset(key, result)


def crawl_the_page(url):
    """Crawl all the songlists in one page."""
    base_url = 'http://music.163.com'
    tree = html.fromstring(requests.get(url).text)
    for item in tree.cssselect('.u-cover > a'):
        crawl_detailed_page(base_url + item.get('href'))

    next_page = tree.cssselect('.znxt')[0].get('href')
    if next_page != 'javascript:void(0)':
        crawl_the_page(base_url + next_page)

    redis_server.sort('songlists', start=0, num=400, by='*->played',
                      desc=True, store='toplist')
    filter_num = redis_server.hget(redis_server.lindex('toplist', -1),
                                   'played')
    redis_server.set('filter_num', filter_num)
    for songlist in set.difference(
        set(redis_server.lrange('songlists', 0, -1)),
        set(redis_server.lrange('toplist', 0, -1))):
            redis_server.delete(songlist)
            redis_server.lrem('songlists', 0, songlist)
