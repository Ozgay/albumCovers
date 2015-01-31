# coding: UTF-8
import web
from config import settings

class Test:
    def __init__(self):
        self.render = settings.render 

    def GET(self):
        web.header('Content-type','text/html')
        web.header('Transfer-Encoding','chunked')
        videos = [
                    {'title':   u'...Test...',
                    'video': ["LoverCD1.mp4", "LoverCD2.mp4"],
                    'nu': 2,
                    'info': u'.CD1.',
                    'discription': u'.CD1.',
                    'copy_right': u'lewis'},

                    {'title':   u'...H...',
                    'video': ["h.1.mp4", "h.2.mp4", "h.3.mp4"],
                    'nu': 3,
                    'info': u'.CD1.',
                    'discription': u'.CD1.',
                    'copy_right': u'lewis'},

                    {'title':   u'...AirLineStewardess...',
                    'video': ["airlineStewardess-1.mp4", "airlineStewardess-4.mp4", "airlineStewardess-3.mp4", "airlineStewardess-4.mp4"],
                    'nu': 4,
                    'info': u'.CD1.',
                    'discription': u'.CD1.',
                    'copy_right': u'lewis'},

                    {'title':   u'...喜剧之王...',
                    'video': ["xjzw.mp4"],
                    'nu': 1,
                    'info': u'.CD1.',
                    'discription': u'.CD1.',
                    'copy_right': u'lewis'},

                    {'title':   u'...我的野蛮女友...',
                    'video': ["MyCurelGirlFriend.mp4"],
                    'nu': 1,
                    'info': u'.CD1.',
                    'discription': u'.CD1.',
                    'copy_right': u'lewis'},

                    {'title':   u'...Test...',
                    'video': ["loveLession.mp4"],
                    'nu': 1,
                    'info': u'.CD1.',
                    'discription': u'.CD1.',
                    'copy_right': u'lewis'},
                 ]
        return self.render.mediaServer(videos)
