#!/usr/bin/env python

import re, os, sys, time, datetime, traceback
import md5 as hash
import urllib
from pyquery import PyQuery as pq

from plugin import PluginTable

class Fetcher:
    '''vim plugins info fetcher'''

    TOTAL_URL  = "http://www.vim.org/scripts/script_search_results.php?order_by=creation_date&direction=descending" 
    PLUGIN_URL = "http://www.vim.org/scripts/script.php?script_id=%d"

    def __init__(self):
        pass

    def download(self, url, cache=True):
        ''' download page and cache it '''
        path = "/tmp/%s" % hash.md5(url).hexdigest()
        #print "load url:", url, "path:", path
        if cache and os.path.exists(path):
            f=open(path, 'r')
            html=f.read()
            f.close()
        else: 
            html=urllib.urlopen(url).read()
            if cache:
                f=open(path, 'w')
                f.write(html)
                f.close()
        return html

    def getTotal(self):
        html=self.download(self.TOTAL_URL)
        links=pq(html).find("body>table").eq(1).find("tr:first>td").eq(2).find("tr>td:first>a")
        p=re.compile('script_id=(\d*)')
        max_id=0
        for link in links:
            data=p.search(pq(link).attr('href'))
            if data:
                id=int(data.group(1))
                if id > max_id:
                    max_id = id
        return max_id

    def fetchPlugin(self, id):
        url  = self.PLUGIN_URL % id
        html = self.download(url)
        if html.find("upload new version") < 0:
            return None

        tables=pq(html).find("table")
        if len(tables) < 9:
            return None
        data = {'id':id}
        d = tables[5]
        title = pq(tables[5]).find("td:first>span:first").text()

        try:
            data['name'], data['desc'] = title.split(" : ", 1)
            trs = pq(tables[7]).find("tr")
            data['type'] = trs.eq(4).text()
            data['user'] = trs.eq(1).find("a").text()
            data['user_link'] = trs.eq(1).find("a").attr("href")
        except:
            return None

        #rating count and download count table
        text = pq(tables[6]).find("tr:first>td").eq(1).text()
        result = re.search('Rating (-?\d*)\/(\d*)', text)
        data['ratings']   = int(result.group(1))
        data['ratings_count']   = int(result.group(2))
        result=re.search('Downloaded by (\d*)', text)
        data['downloads'] = int(result.group(1))

        #version table
        version_table = tables[9]
        trs=pq(version_table).find("tr")
        data["versions"]       = len(trs) - 1
        if len(trs) <= 1:
            return None
        data["create_date"]    = pq(trs[data['versions']]).find("td").eq(2).text()
        current_tr             = pq(trs[1])
        data["update_date"]    = current_tr.find("td").eq(2).text()
        data["curr_version"]   = current_tr.find("td").eq(1).text()

        return data


    def refresh(self, start=1, end=0):
        if end <= 0:
            end = self.getTotal()
        if end < start:
            return False
        pool=0
        pool_size=20
        model = PluginTable()
        for id in xrange(start, end):
            try:
                if pool <= pool_size:
                    pid=os.fork()
                else:
                    time.sleep(pool-pool_size)
                    pid=os.fork()
            except:
                print "fork error"
                traceback.print_exc()
                os._exit(-1)
            
            if pid:
                #parent
                pool=pool+1
                #print "fork pool=%d ", pid, id
                while True:
                    result=os.waitpid(-1, os.WNOHANG)
                    if not result[0]:
                        break;
                    pool=pool-1
                continue

            else:
                #child
                print "fetch script", id
                try:
                    data=self.fetchPlugin(id) 
                    if data:
                        #print "save script", id
                        model.save(data)
                        os._exit(0)
                    else:
                        print "cannot get script", id
                        os._exit(0)
                except:
                    print "error in getting script", id
                    traceback.print_exc()
                    os._exit(-1)
        
        time.sleep(3)
        while True:
            try:
                result = os.waitpid(-1, os.WNOHANG)
                if not result[0]:
                    print "Task finished"
                    break;
            except:
                break;


    def fetchNew(self):
        table = PluginTable()
        last_id, last_date=table.getLast()
        print last_id, last_date
        self.refresh(last_id)

    def fetchSelected(self, idList):
        model = PluginTable()
        for id in idList:
            try:
                data = self.fetchPlugin(id)
                if not data:
                    print "plugin not exist ", id
                    continue
                model.save(data)
                print "fetch plugin success ", id
            except:
                print "fetch plugin error ", id
                traceback.print_exc()
                continue


if __name__ == '__main__':
    fetcher = Fetcher()
    fetcher.refresh(1, 30)
    fetcher.fetchSelected([31, 33, 35])
    print fetcher.getTotal()
    print fetcher.fetchNew()
