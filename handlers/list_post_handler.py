import os, sys
import pygame
from tornado.web import RequestHandler
from app import BaseHandler
from PIL import Image
from io import StringIO, BytesIO
import json


class ListPostHandler(BaseHandler):

    def get(self):
        img_name = os.path.join("/home/paul/PycharmProjects/diplom/backend/images", "img")
        img = Image.open(img_name)
        imgByteArr = BytesIO()
        img.save(imgByteArr, img.format)
        imgByteArr = imgByteArr.getvalue()
        self.write(imgByteArr)
        self.set_header("Content-type", "image/" + img.format)

    # def post(self):
    #     #        data = self.get_argument('kek')
    #     #         photo = self.get_argument('photo')
    #     file_body = self.request.files['photo'][0]['body']
    #     img = Image.open(BytesIO(file_body))
    #     path = "/home/paul/PycharmProjects/diplom/backend/images"
    #     img.save(os.path.join(path, "img"), img.format)
    #     self.write({'message': 'ok'})
