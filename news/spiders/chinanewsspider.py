# -*- coding: utf-8 -*-
import scrapy
import re

from news.tools.timeconvert import DateFormat
from news.items import NewsItem


def filter_str(str):
    return str.replace(' ', '').replace('\n', '').replace('\t', '').replace('\xa0', '').replace('\u3000', '').replace('\r', '') \
        .replace('[]', '')


def ListCombine(lst):
    if len(lst) == 0:
        return None
    string = ""
    for e in lst:
        if e:
            string += e
    return filter_str(string)


# 中国新闻网
class ChinaNewsSpider(scrapy.Spider):
    name = "ChinaNews"
    start_urls = [
        'http://www.chinanews.com/scroll-news/news1.html',
    ]

    def __init__(self):
        self.is_home_page = True
        super(ChinaNewsSpider, self).__init__()

    def parse(self, response):
        if self.is_home_page:
            self.is_home_page = False
            content_list = response.xpath("//*[@id='content_right']/div[3]/ul")
            for li in content_list.xpath(".//li"):
                news_link = ""
                try:
                    category = li.xpath(".//div[1]/a/text()").extract()[0]
                    if category.find("视频") >= 0 or category.find("图片") >= 0:
                        continue
                    news_link = li.xpath(".//div[2]/a/@href").extract()
                    news_link = "http://" + news_link[0][2:]
                except BaseException:
                    continue
                else:
                    yield scrapy.Request(news_link)
        else:
            item = NewsItem()
            if len(response.xpath("//*[@id='cont_1_1_2']/div[4]/div[2]/text()").extract()) == 0:
                print("ye")
            time_str = response.xpath("//*[@id='cont_1_1_2']/div[4]/div[2]/text()").extract()[0]
            time = DateFormat.convertStandardDateFormat(time_str)
            if time is None:
                return
            item['url'] = response.url
            item['publish_time'] = time
            item['source'] = 'ChinaNews'
            contents = ListCombine(response.xpath('//*[@id="cont_1_1_2"]/div[6]/p/text()').extract())
            if not contents:
                contents = ListCombine(response.xpath('//*[@id="cont_1_1_2"]/div[8]/p/text()').extract())
            item['contents'] = contents
            title = filter_str(response.xpath("//*[@id='cont_1_1_2']/h1/text()").extract()[0])
            item['title'] = title
            yield item


if __name__ == "__main__":
    from twisted.internet import reactor
    from scrapy.crawler import CrawlerRunner
    from scrapy.utils.log import configure_logging

    configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
    runner = CrawlerRunner()

    d = runner.crawl(ChinaNewsSpider)
    d.addBoth(lambda _: reactor.stop())
    reactor.run() # the script will block here until the crawling is finished


