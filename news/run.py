from scrapy.crawler import CrawlerProcess


from news.spiders.xinhuanetspider import ABoLuoSpider
from scrapy.utils.project import get_project_settings

if __name__ == '__main__':
    process = CrawlerProcess(get_project_settings())  # 括号中可以添加参数
    for spider in [ABoLuoSpider]:
        try:
            process.crawl(spider)
        except:
            pass
    process.start()

