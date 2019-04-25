from tornado import gen


class UserDAO:
    def __init__(self, db):
        self.db = db

    @gen.coroutine
    def auth(self, arr):
        sql = """
            INSERT INTO users (nickname, password, age)
            VALUES (%s, %s, %s)"""
        cursor = yield self.db.execute(sql, (arr[0], arr[1], arr[2]))
        return cursor
