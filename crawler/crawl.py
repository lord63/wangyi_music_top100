#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import re
import time
from functools import reduce

import requests
from lxml import html
import redis

from crawler.logger import logger


redis_server = redis.StrictRedis(host='localhost', port=6379)


def extract_num(raw):
    """Extract num from the unicode string."""
    matched = re.search(r'\d+', raw).group()
    return matched


def update_toplist():
    """Upadate songlists in the toplist."""
    for index, songlist in enumerate(redis_server.lrange('toplist', 0, -1)):
        if index % 35 == 0:
            time.sleep(5)
        crawl_detailed_page(redis_server.hget(songlist, 'url'))
        logger.info('Update songlist: {0}'.format(songlist))


def crawl_detailed_page(url):
    """Get info from the songlist page."""
    response = requests.get(url)
    tree = html.fromstring(response.text)

    played = extract_num(tree.cssselect('strong')[0].text)
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

    if key not in redis_server.lrange('songlists', 0, -1):
        redis_server.lpush('songlists', key)
    redis_server.hmset(key, result)


def crawl_the_page(url):
    """Crawl all the songlists in one page."""
    logger.info('Start crawl the page: {0}'.format(url))
    base_url = 'http://music.163.com'
    tree = html.fromstring(requests.get(url).text)

    for songlist in tree.cssselect('.u-cover > a'):
        crawl_detailed_page(base_url + songlist.get('href'))
        logger.info('Crawled one songlist: {0}'.format(songlist.get('href')))

    # Take a rest, to avoid being banned.
    time.sleep(5)

    next_page = tree.cssselect('.znxt')[0].get('href')
    if next_page != 'javascript:void(0)':
        logger.info('Crawl next page: {0}'.format(next_page))
        crawl_the_page(base_url + next_page)


def generate_ranklists():
    # Generate 4 top rank lists.
    redis_server.sort('songlists', start=0, num=100, by='*->played',
                      desc=True, store='played_rank')
    redis_server.sort('songlists', start=0, num=100, by='*->comments',
                      desc=True, store='comments_rank')
    redis_server.sort('songlists', start=0, num=100, by='*->favourites',
                      desc=True, store='favourites_rank')
    redis_server.sort('songlists', start=0, num=100, by='*->shares',
                      desc=True, store='shares_rank')
    logger.info('Generate four ranklists.')
    # Union four top rank lists to get final toplist we will maintain
    # to update regularly.
    toplist = reduce(lambda a, b: set(a).union(b), [
        redis_server.lrange('played_rank', 0, -1),
        redis_server.lrange('comments_rank', 0, -1),
        redis_server.lrange('favourites_rank', 0, -1),
        redis_server.lrange('shares_rank', 0, -1)])
    redis_server.delete('toplist')  # Clear the old toplist.
    redis_server.lpush('toplist', *toplist)
    logger.info('Generate the toplist.')

    # Clean up, remove unused songlist.
    for songlist in set(redis_server.lrange('songlists', 0, -1)).difference(
            redis_server.lrange('toplist', 0, -1)):
        redis_server.delete(songlist)
    # Remove ununsed songlist in "songlists" list.
    redis_server.sort('toplist', alpha=True, store='songlists')
    logger.info('Clean up, remove unused songlists.')
