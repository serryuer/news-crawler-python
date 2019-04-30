# -*- coding: utf-8 -*-

from news.spiders.basespider import *


# 新华网
class XinHuaSpider(BaseSpider):
    name = "XinHuaNet"
    start_urls = [
        'http://m.xinhuanet.com/gdxw/index.htm',
    ]
    filter_path = "bloom-filter-backup/xinhua.bloom"

    def parse_home_page(self, response):
        content_list = response.xpath("//*[@id='data']/li")
        links = []
        for li in content_list:
            news_link = ""
            try:
                news_link = li.xpath(".//div[2]/h3/a/@href").extract()[0]
                if self.filter.add(news_link):
                    continue
            except BaseException:
                continue
            else:
                links.append(news_link)
        return links

    def parse_article_page(self, response):
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
        item['url'] = response.url.strip()
        item['publish_time'] = time
        item['source'] = 'XinHuaNet'
        contents = combine_contents_list(response.xpath('//*[@id="p-detail"]/p/text()').extract())
        if not contents:
            contents = combine_contents_list(response.xpath('//*[@id="p-detail"]/div[1]/p/text()').extract())
        item['content'] = contents.strip()
        title_str = response.xpath("/html/body/div[2]/div[3]/div/div[1]/text()").extract()
        if len(title_str) == 0:
            title_str = response.xpath("/html/body/div[4]/div[2]/div[4]/div[2]/div/div[1]/text()").extract()
        if len(title_str) == 0:
            title_str = response.xpath("/html/body/div[3]/div[2]/div/div[1]/text()").extract()
        if len(title_str) == 0:
            title_str = response.xpath("/html/body/div[3]/div[2]/div/div[1]/text()").extract()
        title = filter_str(title_str[0])
        item['title'] = title.strip()
        return item


if __name__ == "__main__":
    from twisted.internet import reactor
    from scrapy.crawler import CrawlerRunner
    from scrapy.utils.log import configure_logging

    configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
    runner = CrawlerRunner()

    d = runner.crawl(XinHuaSpider)
    d.addBoth(lambda _: reactor.stop())
    reactor.run()  # the script will block here until the crawling is finished
