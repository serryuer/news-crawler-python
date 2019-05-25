#!/bin/bash
log_path=~/postGraduate/InformationRetrieve/IR_system/news-crawler-python/log/`date +%Y-%m-%d-%H-%M-%S`.log
bin_path=~/postGraduate/InformationRetrieve/IR_system/news-crawler-python/news

crawlerid=`ps aux | grep run-crawler.py | grep -v grep | awk '{print $2}'`
if [ -n "$crawlerid" ];then
    echo "crawler is running" >> $log_path
else
    rm -rf $bin_path/index2_files
    cd $bin_path
    /Users/zhezhouli/anaconda3/envs/crawler/bin/python run-crawler.py >> $log_path  2>&1 &
fi
