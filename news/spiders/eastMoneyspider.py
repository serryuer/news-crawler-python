# -*- coding: utf-8 -*-
import scrapy
import re

from news.tools.timeconvert import DateFormat
from news.items import NewsItem


def filter_str(str):
    return str.replace(' ', '').replace('\n', '').replace('\t', '').replace('\xa0', '').replace('\u3000', '').replace(
        '\r', '') \
        .replace('[]', '')


def ListCombine(lst):
    if len(lst) == 0:
        return None
    string = ""
    for e in lst:
        if e:
            string += e
    return filter_str(string)

# 东方财富网
class EastMoneySpider(scrapy.Spider):
    name = "EastMoney"
    start_urls = [
        'http://roll.eastmoney.com/',
    ]

    def __init__(self):
        self.is_home_page = True
        super(EastMoneySpider, self).__init__()

    def parse(self, response):
        if self.is_home_page:
            self.is_home_page = False
            content_list = response.xpath("//div[@id='artList']/ul")
            for ul in content_list:
                for li in ul.xpath(".//li"):
                    news_link = ""
                    try:
                        news_link = li.xpath(".//a[2]/@href").extract()[0]
                        # news_link = "http://" + news_link[0][2:]
                        if news_link.find("/photo/") >= 0 or news_link.find("/video/") >= 0:
                            continue
                    except BaseException:
                        continue
                    else:
                        yield scrapy.Request(news_link)
        else:
            item = NewsItem()
            time_str = response.xpath("//div[@class='time']/text()").extract()
            time = DateFormat.convertStandardDateFormat(time_str[0])
            if time is None:
                return
            item['url'] = response.url
            item['publish_time'] = time
            item['source'] = 'XinHuaNet'
            contents = ListCombine(response.xpath('//div[@id="ContentBody"]/p/text()').extract())
            item['contents'] = contents
            title_str = response.xpath("//div[@class='newsContent']/h1/text()").extract()
            title = filter_str(title_str[0])
            item['title'] = title
            yield item


if __name__ == "__main__":
    from twisted.internet import reactor
    from scrapy.crawler import CrawlerRunner
    from scrapy.utils.log import configure_logging

    configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
    runner = CrawlerRunner()

    d = runner.crawl(EastMoneySpider)
    d.addBoth(lambda _: reactor.stop())
    reactor.run()  # the script will block here until the crawling is finished
