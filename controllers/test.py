# coding: UTF-8
import web
import os

from config import settings

class Test:
    def __init__(self):
        self.render = settings.render 

    def GET(self):
        infos = [{
                'album_name': '',
                'artist': '',
                'year_record': '12345',
                'music_contain': 'Nothing',
                'path': u'static/images/onePiece.png',
                'cover_name_1200': u'onePiece.png',
                'cover_name_170': u'onePiece.png',
                'cover_name_100': u'onePiece.png',
                'copy_right': u'lewis',
                'track_count': 1,
                'width': 0,
                'height': 0,
                'size': 0,
                'format': 'png',
                'des':'come on boy!!! day day up!!!',
                'url': ''},
                ]
        return self.render.coverShow(infos)
