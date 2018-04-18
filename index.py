import tornado.ioloop
import tornado.web
from app.onestory.controller.user import user


def app_router():

    return tornado.web.Application([
        tornado.web.url(r"/", user.MainHandler),
        tornado.web.url(r"/story/([0-9]+)", user.StoryHandler, dict(db=3333), name="story")
    ])


if __name__ == "__main__":
    app = app_router()
    app.listen(8080)
    tornado.ioloop.IOLoop.instance().start()

