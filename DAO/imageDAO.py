from tornado import gen
from parser import auth_parse


class ImageDAO:
    def __init__(self, db):
        self.db = db


    @gen.coroutine
    def get_id(self, hash):
        sql = """
            SELECT id from images WHERE hash = %s
        """
        cursor = yield self.db.execute(sql, (hash,))
        return cursor.fetchone()

    @gen.coroutine
    def load_image(self, code):
        sql = """
            INSERT INTO images (hash) VALUES (%s)
        """
        cursor = yield self.db.execute(sql, (code,))
        return cursor

    def create_table(self):
        sql = """
            CREATE TABLE IF NOT EXISTS images(
            id SERIAL NOT NULL PRIMARY KEY,
            hash citext NOT NULL
            );
        """
