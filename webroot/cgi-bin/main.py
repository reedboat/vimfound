#!/usr/bin/env python
# coding: utf-8

import sys, traceback,time,datetime
import cgi
import os
reload(sys)
sys.setdefaultencoding("utf-8")

from jinja2 import Template 

print '''Content-type: text/html\n\n'''
CUR_DIR =os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = CUR_DIR + '/../../src'
LIB_DIR  = ROOT_DIR  + '/lib/vim'
DATA_DIR = ROOT_DIR  + '/data'
VIEW_DIR = ROOT_DIR  + '/views'

sys.path.append(LIB_DIR)
from plugin import PluginTable 
from fetcher import Fetcher 
from grader import Grader
import gl

gl.DATA_DIR = DATA_DIR

def plugin_query(keyword, type, year, sort, page, size):
    table = PluginTable()
    condition=''
    if len(keyword) > 0:
        condition="(name like '%"+keyword+"%' or desc like '%"+keyword+"%')"
    if type != 'all':
        if len(condition) > 0:
            condition += ' AND '
        condition="type='"+type+"'"
    if year != 0:
        if len(condition) > 0:
            condition += ' AND '
        date = datetime.date.fromtimestamp(time.time() - year*365 * 86400).strftime("%Y-%m-%d")
        condition += "create_date > '"+date+"'"

    limit = size
    offset = (page-1) * size
    
    rows = table.query(condition, sort, limit, offset)
    return rows

if __name__ == '__main__':
    form = cgi.FieldStorage()
    sort = form.getvalue('sort', default='ratings')
    type = form.getvalue('type', default='all')
    size = form.getvalue('size', default=50)
    page = form.getvalue('page', default=1)
    year = form.getvalue('year', default=0)
    keyword = form.getvalue('keyword', default='');
    year = int(year)
    page = int(page)
    size = int(size)
    rows = plugin_query(keyword, type, year, sort, page, size)
    try:
        template = Template(open(VIEW_DIR + "/main.tpl").read())
        print template.render(rows=rows, year=year, sort=sort, type=type)
    except:
        traceback.print_exc()
