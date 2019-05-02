# News-Crawler
爬取各大新闻网站滚动新闻页面的最新新闻，每次只爬去最新的一页数据，可以使用外部定时器定时重复增量爬取最新数据。

# 环境

**Ubuntu/Python3.***

- 安装mysql
```
sudo apt-get install mysql-server
```
- 修改$settings.py$文件中数据库相关配置
```
# 数据库配置
DB_IP = "localhost"
DB_USERNAME = "root"
DB_PASSWD = "822104"
DB_DATABASE = "spider"
```
- 建库
```
source db.sql
```

- 安装anaconda
```
curl -O https://repo.anaconda.com/archive/Anaconda3-5.2.0-Linux-x86_64.sh
sh Anaconda3-5.2.0-Linux-x86_64.sh
```

- 创建环境
```
conda create -n crawler python=3.6
```

- 安装python依赖
```
source activate crawler
conda install --yes --file requirements.txt
```

- 构建文件结构
```
mkdir bloom-filter-backup
mkdir index_files
mkdir log
```

## 文件结构
- bloom-filter-backup: 用于保存布隆过滤器的数据，实现增量采集
- index_files: 存储索引文件
- log： 日志文件夹
- news： 采集主文件夹
  - spiders： 每个网站的采集程序
    - basespider.py: 爬虫父类
    - **spider.py: 各网站爬虫实现
  - tools： 时间格式化、布隆过滤器实现
    - index.py: 创建索引，添加文章到索引
    - pybloom.py: 布隆过滤器实现
    - timeconvert.py: 时间格式化
  - items.py: 新闻实体的封装
  - pipelines.py: 采集、解析出的新闻实体的处理，包括存储和建立索引
  - run.py: 单次运行
  - settings.py: 爬虫配置文件
- db.sql: 数据库结构
- requirements.txt: 依赖
- schedule_crawler.sh: 对单次运行的封装，用于调度执行采集程序



## 启动
单次爬取新闻数据
```
python run.py
```