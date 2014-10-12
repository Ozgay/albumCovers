#coding: UTF-8
import sys, os
sys.path.append('/home/lewis/lulu/albumCovers/')
import time
import DEBUG
from controllers.model import dao

def make_dir():
        name = "Waldemar Matuska, Karel \xc4\x8cernoch, Lenka Filipova, Karel Gott, Karel H\xc3\xa1la, Ji\xc5\x99\xc3\xad \xc5\xa0t\xc4\x9bdro\xc5\x88, Felix Slov\xc3\xa1\xc4\x8dek, Na\xc4\x8fa Urb\xc3\xa1nkov\xc3\xa1, Helena Vondr\xc3\xa1\xc4\x8dkov\xc3\xa1, Hana Zagorov\xc3\xa1, Karel V\xc3\xa1gner Se Sv\xc3\xbdm Orchestrem, Ladislav \xc5\xa0Taidl Se Sv\xc3\xbdm Orchestrem, Orchestr \xc4\x8cs. televize & Tane\xc4\x8dn\xc3\xad"
        print len(name)
        print name[0:254]
        artist_dir = os.getcwd()
        dir_len = len(name)
        if dir_len > 255:
            album_dir = artist_dir + '/' + name[0:254]
        else:
            album_dir = artist_dir + '/' + name

        if not os.path.exists(album_dir):
           os.makedirs(album_dir)
        else:
           DEBUG.p('this album info exist!!!!')

def new_file(path):
    f = open(path, "w")
    f.close()

def func_test(b, a = 1):
    print a

def getDoc2(id):
    return dao.getById2(id)

def getDoc(artist, albumName):
    return dao.getById(artist, albumName)

if __name__ == '__main__':
    #make_dir()
    #new_file("xxoo")
    #result = getDoc('Fabulous Trobadors', 'Duels de tchatche')
    result = getDoc2('f639b7da9b1b1f5d4a463834a3da3b82')
    DEBUG.pd(result)


