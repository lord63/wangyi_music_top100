#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

import requests
from lxml import html


def extract_num(raw):
    """Extract num from the unicode string."""
    matched = re.search(r'\d+', raw).group()
    return matched


def update_toplist():
    """Upadate songlists in the toplist."""
    pass


def crawl_detailed_page(url):
    """Get info from the songlist page."""
    response = requests.get(url)
    tree = html.fromstring(response.text)

    title = tree.cssselect('h2')[0].text
    played = extract_num(tree.cssselect('strong')[0].text)
    comments = extract_num(tree.cssselect('.u-btni-cmmt i')[0].text)
    shares = extract_num(tree.cssselect('.u-btni-share i')[0].text)
    favourites = extract_num(tree.cssselect('.u-btni-fav i')[0].text)
    if tree.cssselect('.tags'):
        tags = [item.text for item in tree.cssselect('.u-tag i')]
    else:
        tags = []

    return {"title": title,
            "url": url,
            "played": played,
            "comments": comments,
            "shares": shares,
            "favourites": favourites,
            "tags": tags}


def crawl_the_site(url):
    """Crawl all the songlists in the site."""
    pass
