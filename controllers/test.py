# coding: UTF-8
import web
import os

from config import settings

class Test:
    def __init__(self):
        self.render = settings.render 

    def GET(self):
        info = {
                'album_name': u'Bigger, Better, Faster, More!',
                'artist': u'4 Non Blondes',
                'year_record': '12345',
                'music_contain': '123456',
                'path': u'static/images/4 Non Blondes/Bigger, Better, Faster, More!/dj.xhlljvup.1200x1200-75.jpg',
                'name': u'dj.xhlljvup.1200x1200-75.jpg',
                'width': 123,
                'height': 123,
                'size': 1234,
                'format': 'jepg',
                'des':'test test'
        }
        return self.render.coverShow(info)
