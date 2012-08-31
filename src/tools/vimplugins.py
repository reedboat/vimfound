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

fetcher = Fetcher()
#fetcher.refresh()
grader = Grader()
print grader.calcAvg()
#grader.calc()
