from handlers import firsthandler as f
from handlers import post_handler as p

from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
from tornado import web
import momoko


class BaseHandler(web.RequestHandler):
    @property
    def db(self):
        return self.application.db


from handlers import image_handler as i
from handlers import auth_handler as ah

class Application(web.Application):
    def __init__(self):
        urls = [(r"/", f.FirstHandler),
                (r"/post", p.PostHandler),
                (r"/image", i.ImageHandler),
                (r"/auth", ah.AuthHandler)
                ]
        web.Application.__init__(self, urls)
        self.ioloop = IOLoop.instance()
        dsn = 'dbname=postgres user=postgres password=postgres' \
              ' host=localhost port=5432'
        self.db = momoko.Pool(dsn=dsn, size=1, ioloop=self.ioloop)


if __name__ == "__main__":
    app = Application()
    future = app.db.connect()
    app.ioloop.add_future(future, lambda f: app.ioloop.stop())
    app.ioloop.start()
    future.result()
    # future.result()  # raises exception on connection error

    http_server = HTTPServer(app)
    http_server.listen(3000, 'localhost')
    app.ioloop.start()
