# coding: UTF-8
import os
#import web
import traceback
from config import settings
from datetime import datetime

class Dao:
    def __init__(self):
        self.dt = 'cover_info';
        self.db = settings.db
        #self.db = web.database(dbn='mysql', db='cover', user='root', pw='lewis')

    def inster_instance(self, info):
        print '''inster a new instance'''
        newInstance = info
        try:
            self.db.insert(self.dt,\
                            create_date=datetime.now(), \
                            name=newInstance['path'], \
                            album_name=newInstance['album_name'], \
                            artist=newInstance['artist'], \
                            year_record=newInstance['year_record'], \
                            music_contain=newInstance['music_contain'], \
                            type=newInstance['format'], \
                            cover_path=newInstance['path'], \
                            width=newInstance['width'], \
                            height=newInstance['height'], \
                            file_size=newInstance['size'], \
                            kind=newInstance['format'], \
                            des=newInstance['des'], \
                            type_id=0) 
        except:
           print 'insert db failed!'
           print traceback.print_exc() 

    def update_instance(self, info):
        print '''update a instance'''

    def del_instance(self):
        print '''delete a instance'''

    def get_instance_by_name(self, albumName):
        print '''select a instance by name'''

dao = Dao()
if __name__ == '__main__':
    info = {
        'album_name': '123',
        'artist': '1234',
        'year_record': '12345',
        'music_contain': '123456',
        'path': '12345678',
        'width': 123,
        'height': 123,
        'size': 1234,
        'format': 'xxoo',
        'des':'test it'
    }
    dao.inster_instance(info)

