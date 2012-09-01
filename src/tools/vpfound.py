#!/usr/bin/env python

import sys, traceback,time,datetime, string
import cgi
from os import path
from optparse import OptionParser

reload(sys)
sys.setdefaultencoding("utf-8")

CUR_DIR =path.dirname(path.realpath(__file__))
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

def update(new=True, begin=0, end=0, ids=[]):
    fetcher = Fetcher()
    if new: 
        count=fetcher.fetchNew()
    elif len(ids) == 0:
        count=fetcher.fetchAll(begin, end)
    else:
        count=fetcher.fetchSelected(ids)
    print "%d items updated" % count
        

def top(sort, year, limit):
    table=PluginTable()
    if year != 0:
        date = datetime.date.fromtimestamp(time.time() - year*365 * 86400).strftime("%Y-%m-%d")
        condition = "create_date > '"+date+"'"
    else:
        condition = ''

    rows = table.query(condition, sort, limit)
    template = ("%-5d %-30s %-15s %s")
    i=0
    print "%-5s %-30s %-15s %s" % ("rank", "name", sort, 'desc')
    for row in rows:
        i=i+1
        print template % (i, row['name'], str(row[sort]), row['desc'])
        

def search(keyword, more=False):
    table=PluginTable()
    condition="(name like '%"+keyword+"%'"
    if more:
        condition+="or desc like '%"+keyword+"%')"
    else:
        condition+=")"

    rows = table.query(condition)
    for row in rows:
        print string.Template("$name \t$score \t$desc").substitute(row)

def detail(name):
    try:
        id  = int(name)
    except:
        id  = 0
    table = PluginTable()
    if id > 0:
        plugin = table.findById(id)
    else:
        plugin = table.findByName(name)

    if plugin:
        printPlugin(plugin)
    else:
        print "Sorry, we cannot find plugin %s for you" % name

def grade(name=None):
    grader = Grader()
    if not name:
        count = grader.calc()
        print "jobs done, scores of %d plugins updated" % count
        return 

    try:
        id = int(name)
    except:
        id = 0

    table = PluginTable()
    if id:
        plugin = table.findById(id)
    else:
        plugin = table.findByName(name)

    if plugin:
        grader.calc(data=plugin)
    else:
        print "Sorry, we cannot find plugin %s" % name 


def info():
    table = PluginTable()
    row = table.getLast()
    update_date = row['update_date']
    total = table.count()
    print '''
    vim plugins info
    total: %d, 
    last updated at %s 
    ''' % (total, update_date)

def printPlugin(data):
    tpl='''
   plugin  --  $name (id:$id $type)  
   score   --  $score 
   date    --  created:$create_date  updated:$update_date
   stats   --  rating:$ratings/$ratings_count downloas:$downloads
   desc    --  $desc
    '''
    print string.Template(tpl).substitute(data)

def help():
    MSG_USAGE='''%s <command> [options]
command is valid operation.
command can be:
    help   -- list help
    update -- update scripts data
    grade  -- calucate scripts score
    top    -- list top-n scripts
    search -- search scripts by keyword
    detail -- show scripts detail
    info   -- show repositry info

options is related with specific command, you can use 

    %s <command> -h 

for details
''' % (sys.argv[0], sys.argv[0])
    print "Usage:"
    print MSG_USAGE

if __name__ == "__main__":

    args = sys.argv[1:]
    if len(args) == 0:
        help()
        exit()

    command   = args[0]
    left_args = args[1:]

    if command == 'help' or command=='-h' or command =='--help':
        help()

    elif command=='update':
        MSG_USAGE = "vpfound.py update [-b <begin>] [-e <end>] [-l <idlist>] [-n] [-a]"
        parser= OptionParser(MSG_USAGE)
        parser.add_option("-b", "--begin", action="store", type="int", dest="begin", default=1)
        parser.add_option("-e", "--end",  action="store", type="int", dest="end", default=sys.maxint)
        parser.add_option("-l", "--list", action="store", type="string", dest="ids", default='',
                help='only update selected plugins with provided id,format is <id1,id2,id3,...>')
        parser.add_option("-n", "--new", action="store_true", dest="new", default=True,
                help='only fetch latest created or updated plugins')
        parser.add_option("-a", "--all", action="store_true", dest="all", default=True,
                help='only fetch all plugins')
        options, args=parser.parse_args(left_args)

        if len(options.ids)==0:
            ids = []
        else:
            ids = options.ids.split(',')
        new = not options.all
        update(new=new, begin=options.begin, end=options.end, ids=ids)

    elif command == 'top':
        MSG_USAGE = "vpfound.py top [-n <top n>] [-s <sort>] [-y year]"
        parser= OptionParser(MSG_USAGE)

        parser.add_option("-o", "--order", action="store", type="string", dest="sort", default='score', 
                help="the order must be on of [score, downloads, ratings]")
        parser.add_option("-y", "--year",  action="store", type="int", dest="year", default=0,
                help="show plugins created in latest <n> years")
        parser.add_option("-n", "--size",  action="store", type="int", dest="size", default=10, 
                help ="show only <n> items")
        options, args=parser.parse_args(left_args)
        top(sort=options.sort, year=options.year, limit=options.size)

    elif command == 'search':
        MSG_USAGE = "vpfound.py search <keyword> [-m]"
        parser= OptionParser(MSG_USAGE)
        parser.add_option("-m", "--more",  action="store_true", dest="more", default=False)
        options, args=parser.parse_args(left_args)

        if len(args) < 1:
            parser.print_help()
            exit(-1)
        search(args[0], options.more)

    elif command == 'detail':
        MSG_USAGE = "vpfound.py detail <id or name>"
        parser= OptionParser(MSG_USAGE)
        options, args=parser.parse_args(left_args)
        if len(args) < 1:
            parser.print_help()
            exit()
        detail(args[0])

    elif command == 'grade':
        MSG_USAGE = "vpfound.py grade [<id or name>]"
        parser= OptionParser(MSG_USAGE)
        options, args=parser.parse_args(left_args)
        if len(args) == 1:
            grade(left_args[0])
        elif len(args) == 0:
            grade()
        else:
            parser.print_help()

    elif command == 'info':
        info()
    elif command == 'run':
        print "python -m CGIHTTPServer"
    else:
        help()
        exit()
