#coding: UTF-8
import couchdb
import hashlib
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
        
    def addOneDoc(self, doc):
        keyStr = '%s:%s'%(doc['artist'], doc['album_name']) 
        doc['_id'] = hashlib.md5(keyStr.encode('ascii', 'ignore')).hexdigest()
        doc_id, doc_rev = self.__db[self.__db_name['cover']].save(doc)
        print 'addOneDoc done'

    def delOneDoc(self, doc):
        self.__db[self.__db_name['cover']].delete(doc)
    
    def getById(self, artist, albumName):
        keyStr = '%s:%s'%(doc['artist'], doc['album_name']) 
        return  self.__db[self.__db_name['cover']](keyStr.encode('ascii', 'ignore'))
        

dao = Model()
if __name__ == '__main__':
    print 'test...'
