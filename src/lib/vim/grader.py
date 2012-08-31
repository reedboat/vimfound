#!/usr/bin/env python

import sqlite3, datetime, time, traceback, math
from plugin import PluginTable
import gl


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class Grader:
    ''' vim plugins grader '''
    def __init__(self):
        pass

    def gradePlugin(self, data, avg):
        try:
            score = (avg['score'] * avg['persons'] + data["ratings"]) / float((avg['persons'] + data['ratings_count'])) + math.log10(data["downloads"]) / 6
            print data['name'], score;
            #num = 50 * int(data['ratings']) + int(data['downloads']) #if num < 0: #    score = -1 * math.log(abs(num))
            #else:
            #    score = math.log(num)

            ##print "rating & downloads score:", score
            #year, month, day = data['create_date'].split('-')
            #create_date = datetime.date(int(year), int(month), int(day))
            #base_date = datetime.date(2000, 1, 1);
            #delta     = create_date - base_date
            #create_date_score = 0.75 * delta.total_seconds() / (86400 * 365)
            #score+= create_date_score;
            ##print "create date score:", date_score

            #year, month, day = data['update_date'].split('-')
            #update_date = datetime.date(int(year), int(month), int(day))
            #base_date = datetime.date(2000, 1, 1);
            #delta     = update_date - base_date
            #update_date_score =0.25 * delta.total_seconds() / (86400 * 365)
            #score +=update_date_score
            ##print "update date score:", date_score

            #version_score = math.log10(int(data['versions']))
            #score += version_score
            #print "version score:", version_score
        except:
            print data
            traceback.print_exc()
            score = 0
        #if int(data['versions']) > 3:
        #    score += 1
        return score;

    def calcPlugin(self, data, obj):
        avg = self.calcAvg()
        score = self.gradePlugin(data, avg)
        obj.updateScore(int(data['id']), score)

    def calcAvg(self):
        table = PluginTable();
        row   = table.queryBySql("select count(*) as items_count, sum(ratings) as total_ratings, sum(ratings_count) as total_ratings_count, sum(downloads) as total_downloads from scripts");
        avg_score = row['total_ratings'] / float(row['total_ratings_count'])
        avg_persons=row['total_ratings_count'] / float(row['items_count'])
        print row
        return {'score':avg_score, 'persons':avg_persons}

    def calc(self, id=0):
        table = PluginTable()
        table.connect()
        id = int(id)
        avg = self.calcAvg()

        if id > 0:
            data  = table.findPlugin(id)
            score = self.gradePlugin(data, avg)
            table.updateScore(id, score)
            print id, score
            return True

        for row in table.query(None, None, 0):
            score = self.gradePlugin(row, avg)
            table.updateScore(row['id'], score)


if __name__ == '__main__':
    grader = Grader()
    #grader.calc(12)
    grader.calcAvg()
    #grader.calc()
