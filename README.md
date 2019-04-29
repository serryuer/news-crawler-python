# News-Crawler
爬取各大新闻网站滚动新闻页面的最新新闻

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
pip install -r requirements.txt
```

## 数据格式



## 启动


