import sqlite3
import gl

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
        return sqlite3.connect(self.db)

    def connect(self):
        self.conn = self.open()

    def close(self):
        self.conn.close()

    def count(self):
        sql="select count(id) as total from scripts"
        rows = self.execute(sql)
        return rows[0]["total"]


    def getLast(self):
        rows=self.execute('SELECT id, update_date FROM scripts ORDER BY id DESC LIMIT 1');
        if len(rows) > 0:
            result = rows[0]
        return result

    def execute(self, sql):
        conn = self.open()
        conn.row_factory = dict_factory
        cur  = conn.cursor()
        cur.execute(sql)
        result = cur.fetchall()
        cur.close()
        conn.close()
        return result

    def findByName(self, name):
        sql = "select * from scripts where name='%s'" % name
        rows=self.execute(sql)
        if len(rows) > 0:
            return rows[0]

    def findById(self, id):
        sql = "select * from scripts where id=" + str(id)
        rows=self.execute(sql)
        if len(rows) > 0:
            return rows[0]

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
        
