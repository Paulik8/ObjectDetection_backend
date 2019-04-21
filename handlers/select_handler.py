from tornado import gen
from app import BaseHandler


class SelectHandler(BaseHandler):
    @gen.coroutine
    def get(self):
        sql = """
        SELECT * FROM users 
        """
        cursor = yield self.db.execute(sql)
        self.write('select')
        print(cursor.fetchall())
