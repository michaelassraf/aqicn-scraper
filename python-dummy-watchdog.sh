#!/bin/bash
PYTHON_PID=`/sbin/pidof -s python`
DATE_FORMAT="+%Y-%m-%d_%H-%M-%S"
if [[ ! $PYTHON_PID ]]; then
	DATE=`/bin/date $DATE_FORMAT`
        /bin/echo "$DATE - Started python script" >> /aerovibe-logs/python-dummy-watchdog.log
        /bin/python /AQICNScraper/Scraper.py >> /aerovibe-logs/AQICNScrpaer.log 2>&1 &
        DATE=`/bin/date $DATE_FORMAT`
        /bin/echo "$DATE - Finished launched python script" >> /aerovibe-logs/python-dummy-watchdog.log 2>&1
        exit 0
else
    	DATE=`/bin/date $DATE_FORMAT`
        /bin/echo "$DATE - Python script is already running. PID is $PYTHON_PID" >> /aerovibe-logs/python-dummy-watchdog.log 2>&1
        exit 0
fi
