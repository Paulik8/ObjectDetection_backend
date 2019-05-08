import os, sys
import pygame
import base64
import hashlib
from tornado.web import RequestHandler
from tornado import gen
from app import BaseHandler
from parser import auth_parse, common_parse, tags_parse
from DAO.postDAO import PostDAO
from DAO.imageDAO import ImageDAO
from PIL import Image
import json
from handlers.list_post_handler import ListPostHandler
from io import StringIO, BytesIO
import datetime



class SearchHandler(BaseHandler):

    @gen.coroutine
    def get(self, tags):
        page = self.request.arguments.get('page')[0].decode('utf-8')
        page_int = int(page)
        arr_tags = tags.split('_')
        postDAO = PostDAO(self.db)
        result = yield postDAO.get_posts_by_tag(arr_tags, page_int)
        json_res = yield self.resp_json(result)

        self.set_status(200)
        self.write(json.dumps(json_res, default=SearchHandler.myconverter))


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
