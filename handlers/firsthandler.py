from tornado.web import RequestHandler, Application
from entities.post import Post
from handlers.post_handler import PostHandler
from header_parser import parse
from tornado import gen
from app import BaseHandler
import psycopg2
import momoko
from momoko import *


class FirstHandler(BaseHandler):
    @gen.coroutine
    def get(self):
        sql = """
            CREATE TABLE IF NOT EXISTS users(
            id SERIAL NOT NULL PRIMARY KEY,
            nickname citext,
            password citext,
            age INTEGER
            );
        """
        cursor = yield self.db.execute(sql)
        cursor.close()
        self.write('close')
        # first_post = Post()
        # header = self.request.headers.get('Authorization')
        # print(header)
        # parse(header)
        # self.write(first_post.toJSON())







