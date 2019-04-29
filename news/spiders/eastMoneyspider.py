# -*- coding: utf-8 -*-

from news.spiders.basespider import *


# 东方财富网
class EastMoneySpider(BaseSpider):
    name = "EastMoney"
    start_urls = [
        'http://roll.eastmoney.com/',
    ]

    filter_path = "bloom-filter-backup/eastmoney.bloom"

    def parse_home_page(self, response):
        content_list = response.xpath("//div[@id='artList']/ul")
        links = []
        for ul in content_list:
            for li in ul.xpath(".//li"):
                news_link = ""
                try:
                    news_link = li.xpath(".//a[2]/@href").extract()[0]
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
        time_str = response.xpath("//div[@class='time']/text()").extract()
        time = DateFormat.convertStandardDateFormat(time_str[0])
        if time is None:
            return
        item['url'] = response.url
        item['publish_time'] = time
        item['source'] = 'XinHuaNet'
        contents = combine_contents_list(response.xpath('//div[@id="ContentBody"]/p/text()').extract())
        item['contents'] = contents
        title_str = response.xpath("//div[@class='newsContent']/h1/text()").extract()
        title = filter_str(title_str[0])
        item['title'] = title
        return item


if __name__ == "__main__":
    from twisted.internet import reactor
    from scrapy.crawler import CrawlerRunner
    from scrapy.utils.log import configure_logging

    configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
    runner = CrawlerRunner()

    d = runner.crawl(EastMoneySpider)
    d.addBoth(lambda _: reactor.stop())
    reactor.run()  # the script will block here until the crawling is finished
