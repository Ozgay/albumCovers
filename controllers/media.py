# coding: UTF-8
import web
from config import settings

class Test:
    def __init__(self):
        self.render = settings.render 

    def GET(self):
        web.header('Content-type','text/html')
        web.header('Transfer-Encoding','chunked')
        return self.render.mediaServer()
