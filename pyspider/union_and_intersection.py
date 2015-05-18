#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals, print_function

import re

import requests
from lxml import html


def get_all_the_id(url):
    """Get all the song_list ids."""
    r = requests.get(url)
    tree = html.fromstring(r.text)
    songlist_urls = tree.xpath('//tr/td/a/@href')[4:]
    ids = [re.search(r'(?<=id=)\d+$', url).group() for url in songlist_urls]
    return ids


def main():
    base_url = 'http://wangyi_music_top100.lord63.com/'
    sort_by_played = base_url + 'sortby/played'
    sort_by_favourites = base_url + 'sortby/favourites'
    sort_by_comments = base_url + 'sortby/comments'
    sort_by_shares = base_url + 'sortby/shares'

    # Get song_list ids in four rank lists.
    by_played_ids = get_all_the_id(sort_by_played)
    by_favourites_ids = get_all_the_id(sort_by_favourites)
    by_comments_ids = get_all_the_id(sort_by_comments)
    by_shares_ids = get_all_the_id(sort_by_shares)

    print('Intersection:')
    # In_two: ids in the set are in two rank lists.
    in_two = set(by_played_ids).intersection(by_favourites_ids)
    print("Number of ids in **two** rank lists: {0}".format(len(in_two)))
    in_three = set(in_two).intersection(by_comments_ids)
    print("Number of ids in **three** rank lists: {0}".format(len(in_three)))
    in_four = set(in_three).intersection(by_shares_ids)
    print("Number of ids in **four** rank lists: {0}".format(len(in_four)))

    print("Union:")
    # Has_two: a set that has all the ids in two lists.
    has_two= set(sort_by_played).union(by_favourites_ids)
    print("**Two** rank lists totally have {0} ids".format(len(has_two)))
    has_three = set(has_two).union(by_comments_ids)
    print("**Three** rank lists totally have {0} ids".format(len(has_three)))
    has_four = set(has_three).union(by_shares_ids)
    print("**Four** rank lists totally have {0} ids".format(len(has_four)))


if __name__ == '__main__':
    main()
