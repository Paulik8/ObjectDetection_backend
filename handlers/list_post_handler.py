import os, sys
import pygame
from tornado.web import RequestHandler
from tornado import gen
from app import BaseHandler
from DAO import postDAO as p
from PIL import Image
from io import StringIO, BytesIO
import json
import datetime


class ListPostHandler(BaseHandler):

    @gen.coroutine
    def get(self):
        page = self.request.arguments.get('page')[0].decode('utf-8')
        page_int = int(page)
        postDAO = p.PostDAO(self.db)
        result = yield postDAO.get_posts(page_int)
        json_res = yield self.resp_json(result)

        self.write(json.dumps(json_res, default=ListPostHandler.myconverter))

    @gen.coroutine
    def resp_json(self, res):
        response = []
        for i in res:
            post = {}
            author = {'nickname': i[0], 'age': i[1]}
            image = i[2]
            caption = i[3]
            date = i[4]
            post.update({'author': author, 'image': image, 'caption': caption, 'date': date})
            response.append(post)
        return response


    def myconverter(o):
        if isinstance(o, datetime.datetime):
            return o.__str__()
    # def get(self):
    #     img_name = os.path.join("/home/paul/PycharmProjects/diplom/backend/images", "img")
    #     img = Image.open(img_name)
    #     imgByteArr = BytesIO()
    #     img.save(imgByteArr, img.format)
    #     imgByteArr = imgByteArr.getvalue()
    #     self.write(imgByteArr)
    #     self.set_header("Content-type", "image/" + img.format)

    # def post(self):
    #     #        data = self.get_argument('kek')
    #     #         photo = self.get_argument('photo')
    #     file_body = self.request.files['photo'][0]['body']
    #     img = Image.open(BytesIO(file_body))
    #     path = "/home/paul/PycharmProjects/diplom/backend/images"
    #     img.save(os.path.join(path, "img"), img.format)
    #     self.write({'message': 'ok'})
