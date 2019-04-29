#!/bin/bash
log_path=log/`date +%Y-%m-%d-%H-%M-%S`.log
bin_path=~/ir/news-crawler/news/

crawlerid=`ps aux | grep run.py | grep -v grep | awk '{print $2}'`
if [ -n "$crawlerid" ];then
    echo "crawler is running" >> $log_path
else
    cd $bin_path
    nohup /home/yu/anaconda3/envs/ir-ui/bin/python run.py >> $log_path  2>&1 &
fi
