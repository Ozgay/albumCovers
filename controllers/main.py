# coding: UTF-8
import web
import os

from config import settings

class Test:
    def __init__(self):
        self.render = settings.render 

    def GET(self):
        return self.render.bootstrapTest()
