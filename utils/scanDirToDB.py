#coding: UTF-8
import os
import sys
sys.path.append('/home/lewis/lulu/albumCovers/')
sys.path.append('/home/lewis/lulu/albumCovers/controllers/')
from model import dao
import json


def readFilesInfo(rootDir):
        albumList = []
        #images/xx
        for artist in os.listdir(rootDir):
            artistPath = '%s/%s' % (rootDir, artist)
            #print artistPath
            if os.path.isdir(artistPath):
               #images/artist/xx
               for album in os.listdir(artistPath):
                   albumPath = '%s/%s' % (artistPath, album)
                   if os.path.isdir(albumPath):
                      if os.path.exists('%s/done' % (albumPath)):
                         print 'album: %s has been recorded' % (albumPath)
                         #continue
                      albumInfo = {}
                      albumInfo['artist'] = artist
                      albumInfo['album_name'] = album 
                      albumInfo['path'] = albumPath
                      albumInfo['album_json'] = '%s/album.json' % (albumPath)
                      albumInfo['album_music_json'] = '%s/album_musics.json' % (albumPath)
                      albumInfo['cover_1200'] = ''
                      albumInfo['cover_170'] = ''
                      albumInfo['cover_100'] = ''
                      #images/artist/album/xx
                      for albumfile in os.listdir(albumPath):
                          if albumfile[-16:] == '1200x1200-75.jpg':
                             albumInfo['cover_1200'] = '%s/%s' % (albumPath, albumfile)
                          if albumfile[-14:] == '170x170-75.jpg':
                             albumInfo['cover_170'] = '%s/%s' % (albumPath, albumfile)
                          if albumfile[-14:] == '100x100-75.jpg':
                             albumInfo['cover_100'] = '%s/%s' % (albumPath, albumfile)
                      albumList.append(albumInfo)
                      #print albumInfo 
                      open('%s/done' % (albumPath), 'w').close()

        return albumList

def scanCoverInfo(rootDir):
        print("start scan %s..." % (rootDir))
        if not os.path.exists(rootDir):
           print('can not find %s' % (rootDir))

        fileList = readFilesInfo(rootDir) 
        print len(fileList)
        
        info = {
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
                'format': 'jpeg',
                'des':'come on boy!!! day day up!!!',
                'itunes_album_url': '',
                'itunes_artist_url': ''
        }
        
        for album in fileList:
            if os.path.exists(album['album_json']) and os.path.getsize(album['album_json']) > 10L:
                jsonResultAlbum = json.load(open(album['album_json'], 'r')) 
                ##save album cover images
                coverImageUrl = jsonResultAlbum['artworkUrl100']
                coverImageUrl_170 = coverImageUrl.replace('100x100', '170x170')
                coverImageUrl_1200 = coverImageUrl.replace('100x100', '1200x1200')
                
                info['path'] = album['path']
                info['cover_name'] = coverImageUrl_1200.split('/')[-1] 
                info['cover_name_1200'] = coverImageUrl_1200.split('/')[-1] 
                info['cover_name_170'] = coverImageUrl_170.split('/')[-1] 
                info['cover_name_100'] = coverImageUrl.split('/')[-1] 
                info['album_name'] = jsonResultAlbum['collectionName'] 
                info['artist'] = jsonResultAlbum['artistName'] 
                info['year_record'] = jsonResultAlbum['releaseDate']
                info['track_count'] = jsonResultAlbum['trackCount']
                info['itunes_album_url'] = jsonResultAlbum['collectionViewUrl']
                if jsonResultAlbum.has_key('artistViewUrl'): 
                   info['itunes_artist_url'] = jsonResultAlbum['artistViewUrl']
                if jsonResultAlbum.has_key('copyright'): 
                   info['copy_right'] = jsonResultAlbum['copyright']

            else:
                print 'warning: %s/album.json not exist or empyt!!!' % (album['path'])

            if os.path.exists(album['album_music_json']) and os.path.getsize(album['album_music_json']) > 10L:
                jsonResultMusics = json.load(open(album['album_music_json'], 'r')) 
                musicContains = []
                for jsonResultMusic in jsonResultMusics:
                    musicContains.append(jsonResultMusic['trackName'])
                info['music_contain'] = musicContains 
            else:
                print 'warning: %s/album_musics.json not exist or empty!!!' % (album['path'])
                info['music_contain'] = [] 

            #print info 
            dao.addOneDoc(info)
            
        


if __name__ == '__main__':
    scanPath = '/home/lewis/lulu/albumCovers/static/images'
    scanCoverInfo(scanPath)

