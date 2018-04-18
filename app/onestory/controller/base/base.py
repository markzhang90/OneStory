import tornado.web


class BaseHandler(tornado.web.RequestHandler):

    def run(self):
        return 111

