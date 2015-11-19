#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import click

from crawler import worker


@click.group()
def cli():
    """Simple CLI for manage the crawler.

    \b
    - crawl all the songlists
        $ python fetch.py crawl
    - update the top list(a union of the four rank lists)
        $ python fetch.py update

    get more detailed info for each subcommand via <subcommand --help>
    """
    pass


@cli.command()
def update():
    """Update the top list."""
    worker.update_top_list()


@cli.command()
@click.option('--url', default='http://music.163.com/discover/playlist',
              help='Start crawl from the given url')
def crawl(url):
    """Crawl all the hot songlists."""
    worker.update_all_songlists(url)
    worker.generate_rank_lists()
    worker.generate_top_list()


if __name__ == '__main__':
    worker = worker.Worker()
    cli()

