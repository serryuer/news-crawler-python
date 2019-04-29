from scrapy.crawler import CrawlerProcess

from news.spiders import *
from scrapy.utils.project import get_project_settings

if __name__ == '__main__':
    process = CrawlerProcess(get_project_settings())  # 括号中可以添加参数
    for spider in [ChinaNewsSpider, EastMoneySpider, HuanQiuSpider, XinHuaSpider]:
        try:
            process.crawl(spider)
        except:
            pass
    process.start()
