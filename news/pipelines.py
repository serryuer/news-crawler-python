# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
from scrapy.conf import settings

from news.tools.index import Index

import os
import datetime


class NewsPipeline(object):

    def __init__(self):
        self.db = pymysql.connect(settings.get("DB_IP"), settings.get("DB_USERNAME"), settings.get("DB_PASSWD"),
                                  settings.get("DB_DATABASE"), charset='utf8')
        self.cursor = self.db.cursor()
        self.date_format = "%Y-%m-%d %H:%M:%S"
        self.index = Index()

    # 添加新闻到索引
    def add_to_index(self, item):
        self.index.add_document(item)

    def insert_into_db(self, item):
        try:
            sql = "insert into articles(title, url, body, publish_time, source_site) \
                    value ('%s', '%s', '%s', '%s', '%s')" \
                  % (item['title'], item['url'], item['contents'], item['publish_time'], item['source'])
            self.cursor.execute(sql)
            self.db.commit()
        except Exception:
            self.db.rollback()

    def process_item(self, item, spider):
        self.insert_into_db(dict(item))
        self.add_to_index(dict(item))
        return item
