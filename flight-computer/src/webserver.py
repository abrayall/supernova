import os
import threading

import tornado.web
import tornado.ioloop
import tornado.template

class WebServer:
    def __init__(self, rocket={}):
        self.rocket = rocket
        self.app = tornado.web.Application([
            ("/download/(.*)", tornado.web.StaticFileHandler, {'path': '.'}),
            ("/(.*)", WebHandler, dict(rocket=self.rocket)),
        ])

    def start(self):
        self.app.listen(80)
        threading.Thread(target=tornado.ioloop.IOLoop.current().start).start()

class WebHandler(tornado.web.RequestHandler):
    def initialize(self, rocket):
        self.rocket = rocket

    def get(self, slug):
        self.write(tornado.template.Loader("resources/html").load("index.html").generate(rocket=self.rocket, os=os, directory=self.get_argument('directory', 'data')))
