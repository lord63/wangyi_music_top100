#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from flask import Flask, render_template
import redis


app = Flask(__name__)
redis_server = redis.StrictRedis(host='localhost', port=6379,
                                 decode_responses=True)


@app.route('/')
@app.route('/sortby/<sorted_key>')
def index(sorted_key='played'):
    songlists = redis_server.lrange(sorted_key+"_rank", 0, -1)
    last_update = redis_server.get('last_update')
    top100 = []
    for songlist in songlists:
        top100.append(redis_server.hgetall(songlist))
    return render_template('index.html', top100=top100,
                           last_update=last_update)


if __name__ == '__main__':
    app.run(debug=True, port=5001)