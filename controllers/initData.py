# coding: UTF-8
import web
import os
import traceback
from datetime import datetime
from config import settings
from utils.img import img
from dao import dao 
from utils.getDataFromOther import borrowData 

class Data:
    def __init__(self):
        self.render = settings.render 
        self.prePath = ''
        self.dt = 'cover_info';
        self.db = settings.db

    def GET(self):
        return self.render.data()

    def POST(self):
        data = web.input() 

        if data.coverurl:
            borrowData.getAlbumImageFromUrl(data.coverurl) 
            newInstance = img.getImgInfo('onePiece.png')
        else:
            #newInstance = img.getImgInfo($config.static + '/images/' + data.path)
            print 'error: can not find cover image!!!'
            

        newInstance['name'] = data.path
        newInstance['path'] = self.prePath + data.path
        newInstance['des'] = data.des

        if data.ximiurl:
           #musics list
           musics = borrowData.getMusicListFromXiMi(data.ximiurl) 
           print ','.join(musics)
           newInstance['music_contain'] = ';'.join(musics) 
           
           #artist, album_name, year_record
           (newInstance['artist'], newInstance['album_name'], newInstance['year_record']) = borrowData.getArtistAndAlbumFromXiMi(data.ximiurl)          
        else:
           newInstance['artist'] = data.artist
           newInstance['album_name'] = data.album_name
           newInstance['year_record'] = data.year_record
           newInstance['music_contain'] = data.music_contain

        print 'ximiurl: ' + data.ximiurl 
        print 'name: ' + newInstance['name'] 
        print 'album_name: ' + newInstance['album_name']
        print 'artist: ' + newInstance['artist'] 
        print 'year_record' + newInstance['year_record'] 
        print 'des: ' + newInstance['des'] 
        print 'music_contain: ' + newInstance['music_contain'] 
        print 'path: ' + newInstance['path']
        try:
           dao.inster_instance(newInstance)
        except:
           print 'dao.inster_instance failed!'
           print traceback.print_exc() 

        return newInstance
