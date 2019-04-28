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

# 新华网
class XinHuaSpider(scrapy.Spider):
    name = "XinHuaNet"
    start_urls = [
        'http://m.xinhuanet.com/gdxw/index.htm',
    ]

    def __init__(self):
        self.is_home_page = True
        super(XinHuaSpider, self).__init__()

    def parse(self, response):
        if self.is_home_page:
            self.is_home_page = False
            content_list = response.xpath("//*[@id='data']/li")
            for li in content_list:
                news_link = ""
                try:
                    news_link = li.xpath(".//div[2]/h3/a/@href").extract()[0]
                    # news_link = "http://" + news_link[0][2:]
                except BaseException:
                    continue
                else:
                    yield scrapy.Request(news_link)
        else:
            item = NewsItem()
            time_str = response.xpath("/html/body/div[4]/div[2]/div[4]/div[2]/div/div[2]/span[1]/span/text()").extract()
            if len(time_str) == 0:
                time_str = response.xpath("/html/body/div[3]/div[2]/div/div[2]/span[1]/span/text()").extract()
            if len(time_str) == 0:
                time_str = response.xpath("/html/body/div[2]/div[3]/div/div[2]/span[1]/text()").extract()
            if len(time_str) == 0:
                time_str = response.xpath("/html/body/div[2]/div[3]/div/div[2]/span[1]/text()").extract()
            time = DateFormat.convertStandardDateFormat(time_str[0])
            if time is None:
                return
            item['url'] = response.url
            item['publish_time'] = time
            item['source'] = 'XinHuaNet'
            contents = ListCombine(response.xpath('//*[@id="p-detail"]/p/text()').extract())
            if not contents:
                contents = ListCombine(response.xpath('//*[@id="p-detail"]/div[1]/p/text()').extract())
            item['contents'] = contents
            title_str = response.xpath("/html/body/div[2]/div[3]/div/div[1]/text()").extract()
            if len(title_str) == 0:
                title_str = response.xpath("/html/body/div[4]/div[2]/div[4]/div[2]/div/div[1]/text()").extract()
            if len(title_str) == 0:
                title_str = response.xpath("/html/body/div[3]/div[2]/div/div[1]/text()").extract()
            if len(title_str) == 0:
                title_str = response.xpath("/html/body/div[3]/div[2]/div/div[1]/text()").extract()
            title = filter_str(title_str[0])
            item['title'] = title
            yield item


if __name__ == "__main__":
    from twisted.internet import reactor
    from scrapy.crawler import CrawlerRunner
    from scrapy.utils.log import configure_logging

    configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
    runner = CrawlerRunner()

    d = runner.crawl(XinHuaSpider)
    d.addBoth(lambda _: reactor.stop())
    reactor.run() # the script will block here until the crawling is finished


