import sqlite3
import gl

#| id | name | type | desc | user | user_link | create_date | update_date | ratings | ratings_count | downloads | versions | curr_version | score |
#"""CREATE TABLE scripts(
#   id INT PRIMARY KEY,
#   name VARCHAR(256) NOT NULL DEFAULT '',
#   type VARCHAR(32) NOT NULL DEFAULT '',
#   desc TEXT NOT NULL DEFAULT '',
#   user VARCHAR(64) NOT NULL DEFAULT '',
#   user_link VARCHAR(64) NOT NULL DEFAULT '',
#   create_date VARCHAR(16) NOT NULL DEFAULT '',
#   update_date VARCHAR(16) NOT NULL DEFAULT '',
#   ratings INT NOT NULL DEFAULT 0,
#   ratings_count INT NOT NULL DEFAULT 0,
#   downloads INT NOT NULL DEFAULT 0,
#   versions INT NOT NULL DEFAULT 0,
#   curr_version VARCHAR(64) NOT NULL DEFAULT '',
#   score DOUBLE NOT NULL DEFAULT 0
#   );"""


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

class PluginTable:
    def __init__(self, db='vim.db'):
        if gl.DATA_DIR:
            path=gl.DATA_DIR + '/' + db
        else:
            path='./' + db
        self.db = path

    def open(self):
        print self.db
        return sqlite3.connect(self.db)

    def connect(self):
        self.conn = self.open()

    def close(self):
        self.conn.close()

    def getLast(self):
        conn = self.open()
        cur = conn.cursor()
        cur.execute('SELECT id, update_date FROM scripts ORDER BY id DESC LIMIT 1');
        result=cur.fetchone()
        cur.close()
        conn.close()
        return result

    def save(self, data):
        conn = self.open()
        cur = conn.cursor()
        cur.execute('SELECT * FROM scripts WHERE id=?', (data['id'], ));
        if cur.fetchone():
            result = conn.execute("update scripts set desc=?, update_date=?, ratings=?, ratings_count=?, downloads=?, versions=?, curr_version=?  where id=?", (data["desc"], data["update_date"], data["ratings"],data['ratings_count'], data["downloads"], data["versions"], data['curr_version'], data["id"]))
        else:
            result = conn.execute("insert into scripts (id, name, type, desc, user, user_link,create_date, update_date, ratings, ratings_count, downloads, versions, curr_version) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (data["id"], data["name"], data["type"], data["desc"], data["user"], data['user_link'], data["create_date"], data["update_date"], data["ratings"], data['ratings_count'], data["downloads"], data["versions"], data["curr_version"]));
        conn.commit()
        cur.close()
        conn.close()

    def findPlugin(self, id):
        conn = self.open()
        conn.row_factory = dict_factory
        cur = conn.cursor()
        cur.execute('SELECT * FROM scripts where id=?', (id,));
        data = cur.fetchone()
        cur.close()
        conn.close()
        return data

    def updateScore(self, id, score):
        self.conn.execute("UPDATE scripts SET score=? WHERE id=?", (score, id))
        self.conn.commit()

    def traverse(self, op):
        conn = self.open()
        conn.row_factory = dict_factory
        cur = conn.cursor()
        cur.execute('SELECT * FROM scripts')
        while True:
            data = cur.fetchone()
            if not data:
                conn.commit()
                cur.close()
                conn.close()
            print data
            op(data, self)
        conn.close()

    def queryBySql(self, sql):
        conn = self.open()
        conn.row_factory = dict_factory
        cur = conn.cursor()
        cur.execute(sql)
        row = cur.fetchone()
        cur.close()
        conn.close()
        return row

    def query(self, condition=None, sort='score', limit=50, offset=0):
        conn = self.open()
        conn.row_factory = dict_factory
        cur = conn.cursor()
        sql = 'SELECT * FROM scripts'
        if condition:
            sql += ' WHERE '+condition
        if sort:
            sql += ' ORDER BY %s DESC ' % sort
        if limit >0:
            sql += ' LIMIT ?'
            sql += ' OFFSET ?'
            cur.execute(sql, (limit, offset))
        else:
            cur.execute(sql)

        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows
        
