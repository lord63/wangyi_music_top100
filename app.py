#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals


from os import path
import json

from flask import Flask, g, render_template
from peewee import Model, SqliteDatabase, CharField, FloatField


app = Flask(__name__)
# TODO: override on_result(self, result) method to manage the result yourself.
database_path = path.join(path.abspath(path.dirname(__file__)), 'result.db')
database = SqliteDatabase(database_path)


class BaseModel(Model):
    class Meta:
        database = database


class Resultdb_top100_version_3(BaseModel):
    taskid = CharField(primary_key=True)
    result = CharField()
    updatetime = FloatField()
    url = CharField()


@app.before_request
def before_request():
    g.db = database
    g.db.connect()


@app.after_request
def after_request(response):
    g.db.close()
    return response


@app.route('/')
def index():
    top100 = []
    for record in Resultdb_top100_version_3.select():
        top100.append((record.url, json.loads(record.result)))
    top100 = sorted(top100, key=lambda t: t[1]['played'], reverse=True)[:100]
    return render_template('index.html', top100=top100)


if __name__ == '__main__':
    app.run(debug=True, port=5001)
