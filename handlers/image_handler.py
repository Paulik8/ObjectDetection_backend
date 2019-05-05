import os
from PIL import Image
from io import StringIO, BytesIO
from tornado import gen
from app import BaseHandler


class ImageHandler(BaseHandler):

    @gen.coroutine
    def get(self, id):
        # id = self.request.arguments.get('id')[0].decode("utf-8")
        img_name = os.path.join("/home/paul/PycharmProjects/diplom/backend/images", id)
        img = Image.open(img_name)
        imgByteArr = BytesIO()
        img.save(imgByteArr, img.format)
        imgByteArr = imgByteArr.getvalue()
        self.set_status(200)
        self.write(imgByteArr)
        self.set_header("Content-type", "image/" + img.format)

    # def prepare(self):
    #     print(self.request.arguments.get('id'))
