from app import BaseHandler
from tornado import gen
from parser import auth_parse
import base64
import psycopg2
from DAO.userDAO import UserDAO


class AuthHandler(BaseHandler):
    @gen.coroutine
    def post(self):

        list = yield auth_parse(self)

        userDAO = UserDAO(self.db)
        try:
            cursor = yield (userDAO.auth(list))
            self.write({'response': 200})
        except psycopg2.IntegrityError:
            print('duplicate')
            self.write({'response': 409})

        self.finish()

        print(list)