from tornado import gen
from parser import auth_parse


class PostDAO:
    def __init__(self, db):
        self.db = db

    @gen.coroutine
    def load_post(self, arr):
        sql = """
            INSERT INTO posts (author, caption, data, image, tags) 
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor = yield self.db.execute(sql, (arr[0], arr[1], arr[2], 123, "kek"))
        return cursor


    @gen.coroutine
    def get_auth(self, arr):
        sql = """
            SELECT id FROM users WHERE nickname = %s AND password = %s
        """
        cursor = yield self.db.execute(sql, (arr[0], arr[1]))
        return cursor.fetchone()

    def create_table_posts(self):
        sql = """
            CREATE TABLE IF NOT EXISTS posts(
            id SERIAL NOT NULL PRIMARY KEY,
            author citext NOT NULL,
            image INTEGER NOT NULL,
            caption CITEXT,
            data TIMESTAMP,
            tags CITEXT,
            FOREIGN KEY (author) REFERENCES "users" (nickname)
            );
        """
