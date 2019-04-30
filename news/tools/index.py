# -*- coding: utf-8 -*-
from whoosh.index import create_in
from whoosh.fields import *
from scrapy.conf import settings
import os

import threading
from jieba.analyse import ChineseAnalyzer

 
def synchronized(func):
    func.__lock__ = threading.Lock()
 
    def lock_func(*args, **kwargs):
        with func.__lock__:
            return func(*args, **kwargs)
 
    return lock_func
 

class Index(object):

    ix = None
    instance = None

    @synchronized
    def __new__(cls, *args, **kwargs):
        """
        :type kwargs: object
        """
        if cls.ix is None:
            cls.instance = super().__new__(cls)
            analyzer = ChineseAnalyzer()
            schema = Schema(url=ID(stored=True), source=ID(stored=True), publish_time=DATETIME(stored=True),
                                title=TEXT(stored=True, analyzer=analyzer), content=TEXT(stored=True, analyzer=analyzer))
            if not os.path.exists(settings.get("INDEX_FILE_PATH")):
                os.mkdir(settings.get("INDEX_FILE_PATH"))
            cls.ix = create_in(settings.get("INDEX_FILE_PATH"), schema)
        return cls.instance
    
    def __init__(self):
        self.date_format = "%Y-%m-%d %H:%M:%S"
 
        
    def add_document(self, item):
        try:
            writer = self.ix.writer()
            writer.add_document(url=item['url'], source=item['source'],
                            publish_time=datetime.datetime.strptime(
                                item['publish_time'], self.date_format),
                            title=item['title'], content=item['content'])
            writer.commit()
        except Exception:
            pass

def test():
    index = Index()
    print("test")

if __name__ == '__main__':
    import _thread, time
    try:
        _thread.start_new_thread(test)
        _thread.start_new_thread(test)
    except:
        pass
    
    while True:

        pass
