# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from news.spiders.basespider import filter_str, combine_contents_list
from news.spiders.basespider import BaseSpider
from news.tools.pybloom import ScalableBloomFilter, BloomFilter
from news.items import NewsItem
from news.tools.timeconvert import DateFormat
import scrapy



# 中国新闻网
class ChinaNewsSpider(BaseSpider):
    name = "ChinaNews"
    start_urls = [
        'http://www.chinanews.com/scroll-news/news1.html',
    ]

    filter_path = "bloom-filter-backup/chinanews.bloom"

    def parse_home_page(self, response):
        content_list = response.xpath("//*[@id='content_right']/div[3]/ul")
        links = []
        for li in content_list.xpath(".//li"):
            try:
                category = li.xpath(".//div[1]/a/text()").extract()[0]
                if category.find("视频") >= 0 or category.find("图片") >= 0:
                    continue
                news_link = li.xpath(".//div[2]/a/@href").extract()
                news_link = "http://" + news_link[0][2:]
                if self.filter.add(news_link):
                    continue
            except BaseException:
                continue
            else:
                links.append(news_link)
        return links

    def parse_article_page(self, response):
        item = NewsItem()
        if len(response.xpath("//*[@id='cont_1_1_2']/div[4]/div[2]/text()").extract()) == 0:
            print("ye")
        time_str = response.xpath(
            "//*[@id='cont_1_1_2']/div[4]/div[2]/text()").extract()[0]
        time = DateFormat.convertStandardDateFormat(time_str)
        if time is None:
            return
        item['url'] = response.url
        item['publish_time'] = time
        item['source'] = 'ChinaNews'
        contents = combine_contents_list(response.xpath(
            '//*[@id="cont_1_1_2"]/div[6]/p/text()').extract())
        if not contents:
            contents = combine_contents_list(response.xpath(
                '//*[@id="cont_1_1_2"]/div[8]/p/text()').extract())
        item['contents'] = contents
        title = filter_str(response.xpath(
            "//*[@id='cont_1_1_2']/h1/text()").extract()[0])
        item['title'] = title
        return item


if __name__ == "__main__":
    from twisted.internet import reactor
    from scrapy.crawler import CrawlerRunner
    from scrapy.utils.log import configure_logging

    configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
    runner = CrawlerRunner()

    d = runner.crawl(ChinaNewsSpider)
    d.addBoth(lambda _: reactor.stop())
    reactor.run()  # the script will block here until the crawling is finished
