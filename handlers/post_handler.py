import os, sys
import pygame
from tornado.web import RequestHandler
from tornado import gen
from app import BaseHandler
from parser import auth_parse
from DAO.postDAO import PostDAO
from PIL import Image
from io import StringIO, BytesIO


class PostHandler(BaseHandler):

    @gen.coroutine
    def post(self):
        list = auth_parse(self)
        postDAO = PostDAO(self.db)
        isExists = yield postDAO.get_auth(list)
        if isExists is not None:    # if header not contain basicAuth => return forbidden 403 else:
            author = self.get_argument("author")
            caption = self.get_argument("caption")
            data = self.get_argument("data")
            new_post = [author, caption, data]  #TODO если вместе с картинкой добавлять и получится долгое тегирование
                                                #то вернуть ответ 200 Ok и тегировать картинку и добавить в базу затем

            cursor = yield postDAO.load_post(new_post)
            if not (cursor.closed):
                cursor.close()
            self.write('added')



