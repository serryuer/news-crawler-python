# -*- coding: utf-8 -*-
'''
import os
import sys
os.chdir("/Users/zhezhouli/Repository/news-crawler-python/news")
print(os.getcwd() )
'''
#import sys, os
#sys.path.append(os.path.dirname(os.path.abspath('/Users/zhezhouli/postGraduate/InformationRetrieve/IR_system/news-crawler-python')))
#sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath('/Users/zhezhouli/postGraduate/InformationRetrieve/IR_system/news-crawler-python'))))
import jieba
from news.spiders.basespider import *
#from basespider import *
#import basespider
# 百度热搜

class TopBaiduSpider(BaseSpider):
    name = "TopBaidu"
    #count = 0
    start_urls = [
        'http://top.baidu.com/buzz?b=1&fr=topindex',
    ]
    filter_path = "bloom-filter-backup/topbaidu.bloom"

    def parse(self, response):
        content_list = response.xpath("//*[@id='main']/div[2]/div/table/tr")
        links = []
        tops = []
        items = []
        count = 0
        for tr in content_list:
            news_link = ""
            top = ""
            try:
                top = tr.xpath(".//td[2]/a[1]/text()").extract()
                news_link = tr.xpath(".//td[2]/a[1]/@href").extract()
                if len(top)==0:
                    continue
                if count >= 10:
                    continue
                #if self.filter.add(top):
                #    continue
                links.append(news_link)
                item = NewsItem()
                item['url'] = response.url.strip()
                item['source'] = 'Tops'
                words = list(jieba.cut(top[0]))
                search_item = ''
                word = ''
                for word in words:
                    search_item = search_item + word + '0xffff'
                
                item['title'] = top[0]
                item['content'] = search_item
                count = count + 1
            except BaseException:
                continue
            else:
                tops.append(top)
            yield item
     

    #//*[@id="main"]/div[2]/div/table/tbody/tr[2]/td[2]/a[1]
    #def parse_home_page(self, response):
     #   content_list = response.xpath("//*[@id='main']/div[2]/div/table/tr"
if __name__ == "__main__":
    from twisted.internet import reactor
    from scrapy.crawler import CrawlerRunner
    from scrapy.utils.log import configure_logging
    configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
    runner = CrawlerRunner()

    d = runner.crawl(TopBaiduSpider)
    d.addBoth(lambda _: reactor.stop())
    reactor.run()  # the script will block here until the crawling is finished
'''
        content_list = response.xpath("//*[@id='main']/div[2]/div/table/tr")
        links = []
        tops = []
        items = []
        for tr in content_list:
            news_link = ""
            top = ""
            try:
                top = tr.xpath(".//td[2]/a[1]/text()").extract()
                news_link = tr.xpath(".//td[2]/a[1]/@href").extract()
                if len(top)==0:
                    continue
                if self.filter.add(top):
                    continue
            except BaseException:
                continue
            else:
                #time = DateFormat.convertStandardDateFormat(time_str[0])
                links.append(news_link)
                item = NewsItem()
                item['url'] = response.url.strip()
                item['publish_time'] = 99
                item['source'] = 'tops'
                item['content'] = top
                item['title'] = top
                items.append(item)
                tops.append(top)
        yield items
     
'''