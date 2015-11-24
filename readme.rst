网易云音乐歌单排行
==================

网易云音乐歌单排行 top 100，TRY IT NOW: http://163music.lord63.com/。

主要功能
--------

* 支持四种关键词排序(播放数，评论数，分享数，收藏数)
* 支持标签过滤，点击选择某标签则显示的歌单都带有该标签，并且支持多个标签选择。

开发相关
--------

安装依赖
^^^^^^^^

推荐配合使用 virtualenv

::

    $ virtualenv venv
    $ . venv/bin/activate
    (venv)$ pip install -r dev-requirments.txt

运行爬虫
^^^^^^^^

网页的展示依赖于我们爬取的数据，所以我们首先要爬取数据。由于我们存储数据使用的
是 redis，所以首先启动 redis。

::

    $ redis-server

运行我们的爬虫。默认是从首页开始爬的，我们可以手动指定开始地址

::

    (venv)$ python fetch.py crawl --url http://music.163.com/discover/playlist/?order=hot&cat=%E5%85%A8%E9%83%A8&limit=35&offset=1330

爬虫的日志存储在当前目录下的 `crawler.log` 中，你可以开个 `tail -f crawler.log` 查看爬虫状态。

运行网站
^^^^^^^^

当爬虫爬完以后，我们就可以启动我们的网站啦。

::

    (venv)$ python manager.py runserver

打开浏览器输入 `http://localhost:5000` 应该就可以看到成果了。

License
-------

MIT.
