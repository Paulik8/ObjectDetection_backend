import os, sys
import pygame
import base64
import hashlib
from tornado.web import RequestHandler
from tornado import gen
from app import BaseHandler
from parser import auth_parse, common_parse
from DAO.postDAO import PostDAO
from DAO.imageDAO import ImageDAO
from PIL import Image
from io import StringIO, BytesIO


class PostHandler(BaseHandler):

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
            self.set_status(403)
            self.finish()
            return

        if id_user is not None:
            # if header not contain basicAuth => return forbidden 403 else:

            file_body = self.request.files['photo'][0]['body']
            img = Image.open(BytesIO(file_body))
            path = "/home/paul/PycharmProjects/diplom/backend/images"
            #img.save(os.path.join(path, img), img.format)
            bs64 = base64.b64encode(file_body)
            hash_image = str(hashlib.md5(file_body).hexdigest())
            id_image = 1
            imageDAO = ImageDAO(self.db)
            isLoaded = yield imageDAO.get_duplicate_hash(hash_image)
            if isLoaded is not None:
                id_image = isLoaded[0]
            if isLoaded is None:
                id_image_arr = yield imageDAO.load_image(hash_image)
                id_image = id_image_arr[0]
                img.save(os.path.join(path, str(id_image)), img.format)

            caption = self.get_argument("caption")
            data = self.get_argument("data")
            new_post = [id_user[0], caption, data, id_image]  #TODO если вместе с картинкой добавлять и получится долгое тегирование
                                                #то вернуть ответ 200 Ok и тегировать картинку и добавить в базу затем


            cursor = yield postDAO.load_post(new_post)
            if not (cursor.closed):
                cursor.close()
            self.set_status(200)



