#!/usr/bin/env python

import sys, traceback,time,datetime
import cgi
import os
reload(sys)
sys.setdefaultencoding("utf-8")

CUR_DIR =os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = CUR_DIR + '/..'
LIB_DIR  = ROOT_DIR  + '/lib/vim'
DATA_DIR = ROOT_DIR  + '/data'
VIEW_DIR = ROOT_DIR  + '/views'

sys.path.append(LIB_DIR)
from plugin import PluginTable 
from fetcher import Fetcher 
from grader import Grader
import gl

gl.DATA_DIR = DATA_DIR

def help(command=None):
    doc='''
Usage: %s [command] [args]

command is valid operation.

    command:
        help
        update -- update scripts db
        grade  -- update scripts score
        top    -- show scripts rank
        search -- search scripts by keyword
        detail -- show script detail
        info   -- show repositry info

args is related with specific command
        
    command args:
        update: [from [to]] -- specify update range
            from -- update range id begin, default 0
            to   -- update range id end, default 0

        grade [id] 
            id   -- only grade one script when id supplied
       
        top [len]
            col  -- column used to sort by 
            len  -- returned items count
            year -- only return created in latest n years data when supplied

        search [type, year,sort, page, len]

        detail id
            id   -- script id, required 

        info: no args
        '''
    print doc % sys.argv[0]

def update_db(id=0):
    pass

def top_scripts():
    pass

def search(keyword):
    pass

def detail(name='', id=0):
    pass

def grade(id=0):
    pass

def info():
    pass


if __name__ == "__main__":
    argv = sys.argv
    argc = len( argv )
    if argc==1:
        help()
        exit()

    command = argv[1]
    if command == 'help':
        help()
    elif command == 'update':
        update_db()
        pass
    elif command == 'top':
        top()
        pass
    elif command == 'search':
        search(keyword)
        pass
    elif command == 'detail':
        detail()
        pass
    elif command == 'grade':
        grade()
        pass
    else:
        print "cannot find command %s" % command
        help()

    

    #fetcher = Fetcher()
#fetcher.refresh()
    #grader = Grader()
    #print grader.calcAvg()
#grader.calc()
