#!/usr/bin/env python
# -*- coding:utf-8 -*-
# vim set expandtab

import time
import redis, MySQLdb

class TaskManager:
    def __init__(self, name):
        host = 'localhost'
        port = 6379 
        self.redis = redis.StrictRedis(host, port)
        self.key = name
    
    def get(self):
        score = time.time() + 0.5
        items = self.redis.zrangebyscore(self.key, 0, score)
        if len(items) > 0:
            self.redis.zremrangebyscore(self.key, 0, score)
        return items

    #def pop(self):
    #    return self.redis.zremrangebyrank(self.key, 0, 0)

    def push(self, member, value):
        return self.redis.zadd(self.key, float(value), member)



class Task:
    def __init__(self, row):
        for k in row:
            self.k = row[k]

    @staticmethod
    def get(id):
        db = MySQLdb.connect(host='localhost', user='root', passwd='123456', db='test')
        cursor = db.cursor()
        sql = 'select * from once_task where id=%d' % int(id)
        print sql
        cursor.execute(sql)
        rowset = cursor.fetchall();
        cursor.close()
        print len(rowset)
        db.close()
        return rowset
        if len(rowset) > 0:
            row = rowset[0]
            return Task(row)
        return None

    @staticmethod
    def create(url, run_at):
        #if datetime.strptime(run_at, "%Y-%m-%d %H:%M:%S") > datetime.datetime.now():
        #    print 'wrong time'
        #    return 0

        db = MySQLdb.connect(host='localhost', user='root', passwd='123456', db='test')
        cursor = db.cursor()
        sql = "insert into once_task (url, run_at) values('%s', '%s')" % (url, run_at)
        print sql
        cursor.execute(sql)
        id = cursor.lastrowid
        cursor.close()
        db.close()
        return id
