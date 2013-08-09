#!/usr/bin/env python
# -*- coding:utf-8 -*-
# vim set expandtab
from multiprocessing import Process, Queue, Lock, Pool
import sys, time, urllib2, random
from datetime import datetime, timedelta
#import redis, MySQLdb

from task_manager import TaskManager
from task_manager import Task

#db = MySQLdb.connect(host='localhost', user='root', passwd='123456', db='test')

#now = time.now()



def task_handler(task_id):
    print 'task_id:', task_id
    task = Task.get(task_id)
    if task:
        #print task.id
        print task
    else :
        print 'None'
    #res = urllib2.urlopen(task.url)
    #print 'request_result:', len(res.read())


if __name__ == '__main__':
    worker_count=4
    pool = Pool(processes=worker_count)
    task_manager = TaskManager('once_task')


    time_format = "%Y-%m-%d %H:%M:%S"
    run_at = datetime.now() + timedelta(seconds=random.randint(5, 10))
    url = 'http://qq.com'

    def create_task(run_at, url):
        id = Task.create(url, run_at.strftime(time_format))
        task_manager.push(id, time.mktime(run_at.timetuple()))

    run_at = datetime.now()
    create_task(run_at, url)
    create_task(run_at, url)
    create_task(run_at, url)

    while True:
        task_ids = task_manager.get()
        if len(task_ids) > 0:
            pool.map(task_handler, task_ids)
        time.sleep(5)
        break;
