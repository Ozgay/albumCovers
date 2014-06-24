#coding: UTF-8
import couchdb
import hashlib
import random
import DEBUG 
from couchdb.client import Server
from config import settings

class Model:
    def __init__(self):
        try:
            self.__server = Server()
        except:
            print 'can not connect to Couchdb:%s'%(settings.c['db_url'])

        self.__db = {} 
        self.__db_name = settings.c['db_name']
        DEBUG.p(self.__db_name.items())
        for (k, v) in self.__db_name.items():
            try:
                self.__db[v] = self.__server.create(v)
            except:
                self.__db[v] = self.__server[v]

    def create(self, dbname):
        return self.__server.create(dbname) 

    def delete(self, dbname):
        try:
           self.__server.delete(dbname)
        except:
           print 'database %s doeso not exist!!!'%(dbname)
        
    def clearDB(self, dbname):
        try:
           self.__server.delete(dbname)
        except:
           print 'database %s doeso not exist!!!'%(dbname)

        self.__db[v] = self.__server.create(dbname)

    def getAllDoc(self):
        return self.__db[self.__db_name['cover']] 
        
    def addOneDoc(self, doc):
        keyStr = '%s:%s'%(doc['artist'], doc['album_name']) 
        doc['_id'] = hashlib.md5(keyStr.encode('ascii', 'ignore')).hexdigest()
        doc_id, doc_rev = self.__db[self.__db_name['cover']].save(doc)
        print 'addOneDoc done'

    def delOneDoc(self, doc):
        self.__db[self.__db_name['cover']].delete(doc)
    
    def getById(self, artist, albumName):
        keyStr = '%s:%s'%(artist, albumName) 
        _id = hashlib.md5(keyStr.encode('ascii', 'ignore')).hexdigest()
        map_fun = '''function(doc) {
             if (doc._id == '%s')
                 emit(doc, null);
                 }''' % (_id)
        albums = self.__db[self.__db_name['cover']].query(map_fun)
        for album in albums: 
            return album.key 
        return None

    def getByKeyValue(self, key, value):
        map_fun = '''function(doc) {
             if (doc.%s == '%s')
                 emit(doc, null);
                 }''' % (key, value)
        albums = self.__db[self.__db_name['cover']].query(map_fun)
        for album in albums: 
            return album.key 
        return None

    def getByArtist(self, artist):
        map_fun = '''function(doc) {
             if (doc.artist == '%s')
                 emit(doc, null);
                 }''' % (artist)
        albums = self.__db[self.__db_name['cover']].query(map_fun)
        for album in albums: 
            return album.key 
        return None

    def getByAbbumName(self, albumName):
        map_fun = '''function(doc) {
             if (doc.album_name == '%s')
                 emit(doc, null);
                 }''' % (albumName)
        albums = self.__db[self.__db_name['cover']].query(map_fun)
        for album in albums: 
            return album.key 
        return None

    def getByCopyRight(self, copyRight):
        map_fun = '''function(doc) {
             if (doc.copy_right == '%s')
                 emit(doc, null);
                 }''' % (copyRight)
        albums = self.__db[self.__db_name['cover']].query(map_fun)
        for album in albums: 
            return album.key 
        return None

    def getRandom(self, seed = 11):
        db = self.getAllDoc()    
        tenNews = [] 
        for id in db:
            rd = random.randint(0, seed)
            if rd != 5:
               continue
            if len(tenNews) < 10:
               print db[id]
               tenNews.append(db[id])
        return tenNews

dao = Model()
if __name__ == '__main__':
    print 'test...'
