# coding: UTF-8
import web
import os
import shutil
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
        data = web.input(path={}) 

        coverPath = ''
        needMv = 0
        if data.coverurl:
            print data.coverurl
            coverPath = borrowData.getAlbumImageFromUrl(data.coverurl) 
            if len(coverPath) <= 0:
               return 'sorry, get image failed...'
        elif data.path.filename:
            filename = data.path.filename.replace('\\','/')
            coverPath = os.getcwd() +'/static/images/'+ filename
            fout = open(coverPath, 'wb')
            fout.write(data.path.file.read())
            needMv = 0
        else:
            return 'please input the file or coverurl!'

        newInstance = img.getImgInfo(coverPath)
            

        if data.path:
           newInstance['name'] = data.path
           newInstance['path'] = os.getcwd() + '/static/images/' + data.path

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

        if needMv and newInstance['artist'] and newInstance['album_name']:
           artist_dir = os.getcwd() + '/static/images/' + newInstance['artist'] 
           album_dir = artist_dir + '/' + newInstance['album_name'] 
           if not os.path.exists(artist_dir):
              os.makedirs(artist_dir)
           if not os.path.exists(album_dir):
              os.makedirs(album_dir)
           shutil.move(coverPath, album_dir)
           

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

        return self.render.coverShow(newInstance)