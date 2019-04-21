from app import BaseHandler
from tornado import gen
from header_parser import parse
import base64
from DAO.userDAO import UserDAO


class AuthHandler(BaseHandler):
    @gen.coroutine
    def post(self):
        list = []
        header = parse(self.request.headers.get('Authorization'))
        age = self.get_argument('age')
        data = base64.b64decode(header)
        data_str = str(data)[2:-1].split(':')
        nickname = data_str[0]
        password = data_str[1]
        list = [nickname, password, age]

        userDAO = UserDAO(self.db)
        cursor = yield (userDAO.auth(list))

        print(list)