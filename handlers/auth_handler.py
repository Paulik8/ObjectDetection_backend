from app import BaseHandler
from tornado import gen
from parser import auth_parse
import base64
from DAO.userDAO import UserDAO


class AuthHandler(BaseHandler):
    @gen.coroutine
    def post(self):

        list = auth_parse(self)

        userDAO = UserDAO(self.db)
        cursor = yield (userDAO.auth(list))
        if not cursor.closed:
            cursor.close()

        print(list)