from app import BaseHandler
from tornado import gen
from parser import common_parse
from parser import auth_parse
import base64
import psycopg2
from DAO.userDAO import UserDAO
from DAO.postDAO import PostDAO


class LoginHandler(BaseHandler):

    @gen.coroutine
    def post(self):
        list = yield common_parse(self)
        if list is None:
            self.set_status(403)
            self.finish()
            return

        postDAO = PostDAO(self.db)
        id_user = yield postDAO.get_auth(list)
        if id_user is None:
            self.write({'response': 401})
            self.finish()
        if id_user is not None:
            self.set_status(200)
            self.write({'response': 200})
            self.finish()