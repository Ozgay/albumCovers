# coding: UTF-8
import web
import os
from model import dao

from config import settings

class Test:
    def __init__(self):
        self.render = settings.render 

    def GET(self):
        infos = [{
                'album_name': 'Bigger, Better, Faster, More!',
                'artist': '4 Non Blondes',
                'year_record': '12345',
                'music_contain': ['123','456','789'],
                'path': u'static/images/4 Non Blondes/Bigger, Better, Faster, More!',
                'cover_name_1200': u'dj.xhlljvup.1200x1200-75.jpg',
                'cover_name_170': u'dj.xhlljvup.170x170-75.jpg',
                'cover_name_100': u'dj.xhlljvup.100x100-75.jpg',
                'copy_right': u'lewis',
                'track_count': 1,
                'width': 0,
                'height': 0,
                'size': 0,
                'format': 'png',
                'des':'come on boy!!! day day up!!!',
                'url': ''},
                {'album_name': 'Bigger, Better, Faster, More!',
                'artist': '4 Non Blondes',
                'year_record': '12345',
                'music_contain': ['0','01','012','456','789'],
                'path': u'static/images/4 Non Blondes/Bigger, Better, Faster, More!',
                'cover_name_1200': u'dj.xhlljvup.1200x1200-75.jpg',
                'cover_name_170': u'dj.xhlljvup.170x170-75.jpg',
                'cover_name_100': u'dj.xhlljvup.100x100-75.jpg',
                'copy_right': u'lewis',
                'track_count': 1,
                'width': 0,
                'height': 0,
                'size': 0,
                'format': 'png',
                'des':'come on boy!!! day day up!!!',
                'url': ''},
                ]
        infos = dao.getRandom(100)
        return self.render.coverShow2(infos)
