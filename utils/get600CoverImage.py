#coding: UTF-8
import os
import sys
sys.path.append('/home/lewis/lulu/albumCovers/')
sys.path.append('/home/lewis/lulu/albumCovers/controllers/')
from model import dao
import json
import DEBUG
import urllib2

def __saveCoverImage(albumDir, coverImageUrl):
        try:
            f = urllib2.urlopen(coverImageUrl)
            with open(albumDir + '/' + coverImageUrl.split('/')[-1], 'wb') as code:
                code.write(f.read())
            DEBUG.p('%s Pic Saved!' % (coverImageUrl.split('/')[-1])) 
        except:
            DEBUG.p('%s Pic Saved failed! and try again...' % (coverImageUrl.split('/')[-1])) 
            try:
                f = urllib2.urlopen(coverImageUrl)
                with open(albumDir + '/' + coverImageUrl.split('/')[-1], 'wb') as code:
                    code.write(f.read())
                DEBUG.p('%s Pic Saved!' % (coverImageUrl.split('/')[-1])) 
            except:
                DEBUG.p('err: %s Pic Saved failed!' % (coverImageUrl.split('/')[-1])) 

def download600CoverImage():
    db = dao.getAllDoc()    
    for id in db:
        albumJson = db[id]['path'] + '/album.json'
        jsonResultAlbum = json.load(open(albumJson, 'r')) 
        coverImageUrl_600 = jsonResultAlbum['artworkUrl100'].replace('100x100', '600x600')
        print coverImageUrl_600 
        __saveCoverImage(db[id]['path'], coverImageUrl_600)


if __name__ == '__main__':
    download600CoverImage()
