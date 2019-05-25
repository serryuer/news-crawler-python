# -*- coding: utf-8 -*-
import sys, os
sys.path.append(os.path.dirname(os.path.abspath('/Users/zhezhouli/Repository/news-crawler-python/news')))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath('/Users/zhezhouli/Repository/news-crawler-python/news'))))

from news.spiders.basespider import *


# 环球新闻
class HuanQiuSpider(BaseSpider):
    name = "HuanQiu"
    start_urls = [
        'http://china.huanqiu.com/roll.html',
    ]
    filter_path = "bloom-filter-backup/huanqiu.bloom"
    def parse_home_page(self, response):
        content_list = response.xpath("//*[@id='panesT']/div[1]/div[1]/ul")
        links = []
        for ul in content_list:
            for li in ul.xpath(".//li"):
                news_link = ""
                try:
                    news_link = li.xpath(".//a/@href").extract()[1]
                    # news_link = "http://" + news_link[0][2:]
                    if news_link.find("/photo/") >= 0 or news_link.find("/video/") >= 0:
                        continue

                    if self.filter.add(news_link):
                        continue
                except BaseException:
                    continue
                else:
                    links.append(news_link)
        return links

    def parse_article_page(self, response):
        item = NewsItem()
        time_str = response.xpath("//span[@class='la_t_a']/text()").extract()
        time = DateFormat.convertStandardDateFormat(time_str[0])
        if time is None:
            return
        item['url'] = response.url.strip()
        item['publish_time'] = time
        item['source'] = 'XinHuaNet'
        contents = combine_contents_list(response.xpath('//div[@class="la_con"]/p/text()').extract())
        item['content'] = contents.strip()
        title_str = response.xpath("//h1[@class='tle']/text()").extract()
        title = filter_str(title_str[0])
        item['title'] = title.strip()
        return item


if __name__ == "__main__":
    from twisted.internet import reactor
    from scrapy.crawler import CrawlerRunner
    from scrapy.utils.log import configure_logging

    configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
    runner = CrawlerRunner()

    d = runner.crawl(HuanQiuSpider)
    d.addBoth(lambda _: reactor.stop())
    reactor.run()  # the script will block here until the crawling is finished
