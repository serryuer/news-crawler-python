# -*- coding: utf-8 -*-
import scrapy

from news.tools.timeconvert import DateFormat
from news.items import NewsItem

from news.tools.pybloom import ScalableBloomFilter, BloomFilter

import os


def filter_str(str):
    return str.replace(' ', '').replace('\n', '').replace('\t', '').replace('\xa0', '').replace('\u3000', '').replace(
        '\r', '') \
        .replace('[]', '')


def combine_contents_list(lst):
    if len(lst) == 0:
        return None
    string = ""
    for e in lst:
        if e:
            string += e
    return filter_str(string)


# 中国新闻网
class BaseSpider(scrapy.Spider):
    name = ""

    filter = ScalableBloomFilter(initial_capacity=100000, error_rate=0.00001)
    filter_path = ""

    def __init__(self):
        self.is_home_page = True
        if os.path.exists(self.filter_path):
            with open(self.filter_path, 'rb') as f:
                self.filter = ScalableBloomFilter.fromfile(f)
        super(BaseSpider, self).__init__()

    def save_filter(self):
        with open(self.filter_path, 'wb') as f:
            self.filter.tofile(f)

    def parse_home_page(self, response):
        pass

    def parse_article_page(self, response):
        pass

    def parse(self, response):
        if self.is_home_page:
            self.is_home_page = False
            for link in self.parse_home_page(response):
                yield scrapy.Request(link, dont_filter=True)
        else:
            item = self.parse_article_page(response)
            if item["url"] is None or item["title"] is None or\
                item["content"] is None or item["title"] is None or\
                    item["publish_time"] is None:
                pass
            yield item
    
    # 爬虫结束时的回调函数
    def closed(self, reason):
        self.save_filter()
