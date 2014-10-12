#coding: UTF-8
import os
import re
import urllib2
import urllib
import json
import traceback
import DEBUG
from controllers.model import dao

#itunes seach api:
#http://www.apple.com/itunes/affiliates/resources/documentation/itunes-store-web-service-search-api.htmlhttp://www.apple.com/itunes/affiliates/resources/documentation/itunes-store-web-service-search-api.html
#format:
#https://itunes.apple.com/search?parameterkeyvalue
#parameterkeyvalue: key1=value1&key2=value2&key3=value3
#term
#country : us, tw,  
#media : movie, podcast, music, musicVideo, audiobook, shortFilm, tvShow, software, ebook, all
#entity:
##movie: movieArtist, movie
##podcast: podcastAuthor, podcast
##music: musicArtist, musicTrack, album, musicVideo, mix, song
##musicVideo: musicArtist, musicVideo
##audiobook: audiobookAuthor, audiobook
##shortFilm: shortFilmArtist, shortFilm
##tvShow: tvEpisode, tvSeason
##software: software, iPadSoftware, macSoftware
##ebook:ebook
#...

#https://itunes.apple.com/search?term=%E5%AE%89%E5%92%8C%E6%A1%A5%E5%8C%97&country=tw&media=music
#{
#    "wrapperType":"track", 
#    "kind":"song",
#    "artistId":708069069,
#    "collectionId":771269538,
#    "trackId":771269549,
#    "artistName":"宋冬野",
#    "collectionName":"安和??????",
#    "trackName":"董小姐",
#    "collectionCensoredName":"安和??????",
#    "trackCensoredName":"董小姐",
#    "artistViewUrl":"https://itunes.apple.com/tw/artist/song-dong-ye/id708069069?uo=4",
#    "collectionViewUrl":"https://itunes.apple.com/tw/album/dong-xiao-jie/id771269538?i=771269549&uo=4",
#    "trackViewUrl":"https://itunes.apple.com/tw/album/dong-xiao-jie/id771269538?i=771269549&uo=4",
#    "previewUrl":"http://a676.phobos.apple.com/us/r1000/027/Music4/v4/59/fd/ff/59fdff70-49f2-448d-ef33-a8a5bc925471/mzaf_3388213124261872805.plus.aac.p.m4a",
#    "artworkUrl30":"http://a5.mzstatic.com/us/r30/Music6/v4/5c/95/8c/5c958c00-424b-bdf4-11a7-0fa31039cd86/886444295185.30x30-50.jpg",
#    "artworkUrl60":"http://a2.mzstatic.com/us/r30/Music6/v4/5c/95/8c/5c958c00-424b-bdf4-11a7-0fa31039cd86/886444295185.60x60-50.jpg",
#    "artworkUrl100":"http://a1.mzstatic.com/us/r30/Music6/v4/5c/95/8c/5c958c00-424b-bdf4-11a7-0fa31039cd86/886444295185.100x100-75.jpg",
#    "collectionPrice":200.00,
#    "trackPrice":20.00,
#    "releaseDate":"2013-12-03T08:00:00Z",
#    "collectionExplicitness":"notExplicit",
#    "trackExplicitness":"notExplicit",
#    "discCount":1,
#    "discNumber":1,
#    "trackCount":12,
#    "trackNumber":4,
#    "trackTimeMillis":310213,
#    "country":"TWN",
#    "currency":"TWD",
#    "primaryGenreName":"Mandopop"
#}

#https://itunes.apple.com/search?term=%E5%AE%89%E5%92%8C%E6%A1%A5%E5%8C%97&country=tw&media=music&entity=album
#{
#    "wrapperType":"collection",
#    "collectionType":"Album",
#    "artistId":708069069,
#    "collectionId":771269538,
#    "artistName":"宋冬野",
#    "collectionName":"安和??????",
#    "collectionCensoredName":"安和??????",
#    "artistViewUrl":"https://itunes.apple.com/tw/artist/song-dong-ye/id708069069?uo=4",
#    "collectionViewUrl":"https://itunes.apple.com/tw/album/an-he-qiao-bei/id771269538?uo=4",
#    "artworkUrl60":"http://a2.mzstatic.com/us/r30/Music6/v4/5c/95/8c/5c958c00-424b-bdf4-11a7-0fa31039cd86/886444295185.60x60-50.jpg",
#    "artworkUrl100":"http://a1.mzstatic.com/us/r30/Music6/v4/5c/95/8c/5c958c00-424b-bdf4-11a7-0fa31039cd86/886444295185.100x100-75.jpg",
#    "collectionPrice":200.00,
#    "collectionExplicitness":"notExplicit",
#    "trackCount":12,
#    "copyright":"????2013 Modern Sky Entertainment Co.,Ltd",
#    "country":"TWN",
#    "currency":"TWD",
#    "releaseDate":"2013-12-03T08:00:00Z",
#    "primaryGenreName":"Mandopop"
#}

#https://itunes.apple.com/search?term=Rammstein&country=us&media=music&entity=musicArtist
#{
#    "wrapperType":"artist",
#    "artistType":"Artist",
#    "artistName":"Rammstein",
#    "artistLinkUrl":"https://itunes.apple.com/us/artist/rammstein/id408932?uo=4",
#    "artistId":408932,
#    "amgArtistId":198625,
#    "primaryGenreName":"Rock",
#    "primaryGenreId":21,
#    "radioStationUrl":"https://itunes.apple.com/station/idra.408932"
#}

#https://itunes.apple.com/search?term=Rammstein&country=us&media=music&entity=albumName
#{
#    "wrapperType":"collection",
#    "collectionType":"Album",
#    "artistId":408932,
#    "collectionId":368317231,
#    "amgArtistId":198625,
#    "artistName":"Rammstein",
#    "collectionName":"Sehnsucht",
#    "collectionCensoredName":"Sehnsucht",
#    "artistViewUrl":"https://itunes.apple.com/us/artist/rammstein/id408932?uo=4",
#    "collectionViewUrl":"https://itunes.apple.com/us/album/sehnsucht/id368317231?uo=4#",
#    "artworkUrl60":"http://a5.mzstatic.com/us/r30/Music/58/b3/d8/mzi.nncogslg.60x60-50.jpg",
#    "artworkUrl100":"http://a4.mzstatic.com/us/r30/Music/58/b3/d8/mzi.nncogslg.100x100-75.jpg",
#    "collectionPrice":7.99,
#    "collectionExplicitness":"notExplicit",
#    "trackCount":11,
#    "copyright":"????1997 Universal Music Domestic Rock/Urban, a division of Universal Music GmbH",
#    "country":"USA",
#    "currency":"USD",
#    "releaseDate":"2010-02-05T08:00:00Z",
#    "primaryGenreName":"Rock"
#}

class ItunesAPI:
    def __init__(self):
        self.baseUrl = 'https://itunes.apple.com/search?'
        self.limit = 50

    def __getResponeResult(self, url):
        try:
            login_data = urllib.urlencode({})
            login_headers = {'Referer':url, 'User-Agent':'Opera/9.60',}
            login_request = urllib2.Request(url, login_data, login_headers)
            result = urllib2.urlopen(login_request, data=None, timeout=30).read()
            return json.loads(result.decode("utf-8"))['results']
        except:
            DEBUG.p('get data failed, and try again...')
            try:
                login_data = urllib.urlencode({})
                login_headers = {'Referer':url, 'User-Agent':'Opera/9.60',}
                login_request = urllib2.Request(url, login_data, login_headers)
                result = urllib2.urlopen(login_request, data=None, timeout=30).read()
                return json.loads(result.decode("utf-8"))['results']
            except:
                DEBUG.p('err: get data failed from: %s' % (url))
                result = []
                return result

    def __saveCoverImage(self, album_dir, coverImageUrl):
        try:
            #f = urllib2.urlopen(coverImageUrl)
            #with open(album_dir + '/' + coverImageUrl.split('/')[-1], 'wb') as code:
            #    code.write(f.read())
            data = urllib2.urlopen(coverImageUrl, data=None, timeout=20).read()
            DEBUG.p('got data:') 
            f = open(album_dir + '/' + coverImageUrl.split('/')[-1], 'wb')
            f.write(data)
            DEBUG.p('%s Pic Saved!' % (coverImageUrl.split('/')[-1])) 
            f.close()
            return 1 
        except:
            DEBUG.p('%s Pic Saved failed! and try again...' % (coverImageUrl.split('/')[-1])) 
            try:
                data = urllib2.urlopen(coverImageUrl, data=None, timeout=30).read()
                DEBUG.p('got data:') 
                f = open(album_dir + '/' + coverImageUrl.split('/')[-1], 'wb')
                f.write(data)
                DEBUG.p('%s Pic Saved!' % (coverImageUrl.split('/')[-1])) 
                f.close()
                return 1 
            except:
                DEBUG.p('err: %s Pic Saved failed!' % (coverImageUrl.split('/')[-1])) 
                #remove failed-file
                os.remove(album_dir + '/' + coverImageUrl.split('/')[-1])
                f = open(album_dir + '/' + coverImageUrl.split('/')[-1] + ".failed", "w")
                f.close()
                return 0 

    def __saveAllInfos(self, jsonResultAlbum, country):
        #prepare dir
        dir_len = len(jsonResultAlbum['artistName'])
        if dir_len > 255:
            artist_dir = os.getcwd() + '/static/images/' + jsonResultAlbum['artistName'][0:200]
        else:
            artist_dir = os.getcwd() + '/static/images/' + jsonResultAlbum['artistName']
        dir_len = len(jsonResultAlbum['collectionName'])
        if dir_len > 255:
            album_dir = artist_dir + '/' + jsonResultAlbum['collectionName'][0:200]
        else:
            album_dir = artist_dir + '/' + jsonResultAlbum['collectionName']

        if not os.path.exists(artist_dir):
           os.makedirs(artist_dir)
        if not os.path.exists(album_dir):
           os.makedirs(album_dir)
        else:
           DEBUG.p('this album dir exist:%s'%(album_dir))
           result = dao.getById(jsonResultAlbum['artistName'], jsonResultAlbum['collectionName']) 
           DEBUG.pd(result)
           if result != None:
              DEBUG.p('this album info exist in db!!!!')
              return result 
           else:
              DEBUG.pw('this album info not exist in db!!!!')

        #result = dao.getById(jsonResultAlbum['artistName'], jsonResultAlbum['collectionName']) 
        #coverImage_1200 = jsonResultAlbum['artworkUrl100'].replace('100x100', '1200x1200').split('/')[-1]
        #if result != None and os.path.exists(album_dir + '/' + coverImage_1200):
        #   DEBUG.p('this album info exist in db!!!!')
        #   DEBUG.p('album:%s; artist:%s'%( jsonResultAlbum['collectionName'], jsonResultAlbum['artistName']))
        #   return result

        #save album info json file
        file = open(album_dir + "/album.json","w")
        json.dump(jsonResultAlbum, file)
        file.close()

        
        ##save album cover images
        ret = 0 
        coverImageUrl = jsonResultAlbum['artworkUrl100']
        ret += self.__saveCoverImage(album_dir, coverImageUrl)
        coverImageUrl_170 = coverImageUrl.replace('100x100', '170x170')
        ret += self.__saveCoverImage(album_dir, coverImageUrl_170)
        coverImageUrl_600 = coverImageUrl.replace('100x100', '600x600')
        ret += self.__saveCoverImage(album_dir, coverImageUrl_600)
        coverImageUrl_1200 = coverImageUrl.replace('100x100', '1200x1200')
        ret += self.__saveCoverImage(album_dir, coverImageUrl_1200)
        if ret == 0:
           return ret 

        info = {
                'album_name': '',
                'artist': '',
                'year_record': '12345',
                'music_contain': 'Nothing',
                'path': u'static/images/',
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
        #DEBUG.pd(jsonResultAlbum)
        info['path'] = album_dir + '/'
        info['cover_name_1200'] = coverImageUrl_1200.split('/')[-1] 
        info['cover_name_170'] = coverImageUrl_170.split('/')[-1] 
        info['cover_name_100'] = coverImageUrl.split('/')[-1] 
        info['album_name'] = jsonResultAlbum['collectionName'] 
        info['artist'] = jsonResultAlbum['artistName'] 
        info['cover_name'] = coverImageUrl_1200.split('/')[-1] 
        info['year_record'] = jsonResultAlbum['releaseDate']
        info['track_count'] = jsonResultAlbum['trackCount']
        info['itunes_album_url'] = jsonResultAlbum['collectionViewUrl']
        if jsonResultAlbum.has_key('artistViewUrl'): 
           info['itunes_artist_url'] = jsonResultAlbum['artistViewUrl']
        if jsonResultAlbum.has_key('copyright'): 
           info['copy_right'] = jsonResultAlbum['copyright']

        musicContains = []
        jsonMusics = []
        jsonResultMusics = self.__getMusicLists(jsonResultAlbum['collectionName'], country)
        if len(jsonResultMusics) == jsonResultAlbum['trackCount']: 
           for jsonResultMusic in jsonResultMusics:
               musicContains.append(jsonResultMusic['trackName'])
           jsonMusics = jsonResultMusics
        else:
           for jsonResultMusic in jsonResultMusics:
               if jsonResultMusic['artistName'] == jsonResultAlbum['artistName']:
                  musicContains.append(jsonResultMusic['trackName'])
                  jsonMusics.append(jsonResultMusic)
        try:
            if len(jsonMusics) == 0:
               for jsonResultMusic in jsonResultMusics:
                   if jsonResultMusic['collectionId'] == jsonResultAlbum['collectionId']:
                      musicContains.append(jsonResultMusic['trackName'])
                      jsonMusics.append(jsonResultMusic)
        except:
            DEBUG.p("empty music list!!!")

        #save music list json file
        file = open(album_dir + "/album_musics.json","w")
        json.dump(jsonMusics, file)
        file.close()

        info['music_contain'] = list(set(musicContains)) 
        DEBUG.pd(info)

        try:
            #record info into db
            dao.addOneDoc(info)
        except:
            print 'add doc failed: %s:%s'%(info['artist'], info['album_name'])
            print traceback.print_exc()
            

        return info
    def __getMusicLists(self, albumName, country):
        #get album musics info
        url = self.baseUrl + 'term=%s&country=%s&media=music&limit=%d'%(albumName, country, self.limit)
        DEBUG.p(url)
        jsonResultMusics = self.__getResponeResult(url)
        DEBUG.p('result count: %d'%(len(jsonResultMusics)))
        return jsonResultMusics
        
    def __getInfoByAlbumName(self, albumName, country):
        if not albumName:
           DEBUG.p('Please special the album name')
           return false 
        if not country:
           DEBUG.p('country undefine, use "us" as defaulted')
           country = 'us'

        url = self.baseUrl + 'term=%s&country=%s&media=music&entity=album&limit=%d'%(albumName, country, self.limit)
        DEBUG.p(url)
        jsonResultAlbums = self.__getResponeResult(url)
        DEBUG.p('result count: %d'%(len(jsonResultAlbums)))
        return jsonResultAlbums

    def __getInfoByArtistName(self, artistName, country):
        if not artistName:
           DEBUG.p('Please special the artist name')
           return false 
        if not country:
           DEBUG.p('country undefine, use "us" as defaulted')
           country = 'us'

        url = self.baseUrl + 'term=%s&country=%s&media=music&entity=album&limit=%d'%(artistName, country, self.limit)
        DEBUG.p(url)
        jsonResultAlbums = self.__getResponeResult(url)
        DEBUG.p('result count: %d'%(len(jsonResultAlbums)))
        return jsonResultAlbums

    def getInfosWithAritstName_deep(self, artistName, country, limit = 50):
        if not artistName:
           DEBUG.p('Please special the artist name')
           return false 
        if not country:
           DEBUG.p('country undefine, use "us" as defaulted')
           country = 'us'
        if limit != 50:
           self.limit = int(limit)

        infos = []
        #get all albums of the artist
        jsonResultAlbums = self.__getInfoByArtistName(artistName, country)
        for jsonResultAlbum in jsonResultAlbums:
            ret = self.__saveAllInfos(jsonResultAlbum, country)
            if not ret: 
               continue
            infos.append(ret) 
            #enter db

            #get all albums of other artist
            if jsonResultAlbum['artistName'] != artistName:
                    jsonAlbums = self.__getInfoByArtistName(jsonResultAlbum['artistName'], country)
                    for jsonAlbum in jsonAlbums:
                        ret = self.__saveAllInfos(jsonAlbum, country)
                        if not ret:
                           continue
                        infos.append(ret) 

                        jsonResultAlbums2 = self.__getInfoByAlbumName(jsonAlbum['collectionName'], country)
                        for jsonResultAlbum2 in jsonResultAlbums2:
                            ret = self.__saveAllInfos(jsonResultAlbum2, country)
                            if not ret:
                               continue
                            infos.append(ret) 

                            jsonAlbums2 = self.__getInfoByArtistName(jsonResultAlbum2['artistName'], country)
                            for jsonAlbum2 in jsonAlbums2:
                                ret = self.__saveAllInfos(jsonAlbum2, country)
                                if not ret:
                                   continue
                                infos.append(ret) 

        return infos

    def getInfosWithArtistName(self, artistName, country, limit = 50):
        if not artistName:
           DEBUG.p('Please special the artist name')
           return false 
        if not country:
           DEBUG.p('country undefine, use "us" as defaulted')
           country = 'us'
        if limit != 50:
           self.limit = int(limit)

        infos = []
        #get all albums of the artist
        jsonResultAlbums = self.__getInfoByArtistName(artistName, country)
        for jsonResultAlbum in jsonResultAlbums:
            ret = self.__saveAllInfos(jsonResultAlbum, country)
            if not ret: 
               continue
            infos.append(ret) 

        return infos

    def getInfosWithAlbumName_deep(self, albumName, country, limit = 50):
        if not albumName:
           DEBUG.p('Please special the album name')
           return false 
        if not country:
           DEBUG.p('country undefine, use "us" as defaulted')
           country = 'us'
        if limit != 50:
           self.limit = int(limit)

        infos = []
        #get all albums of name 'albumName' 
        jsonResultAlbums = self.__getInfoByAlbumName(albumName, country)
        for jsonResultAlbum in jsonResultAlbums:
            ret = self.__saveAllInfos(jsonResultAlbum, country)
            if not ret: 
               continue
            infos.append(ret) 

            #get all albums of the artist
            jsonAlbums = self.__getInfoByArtistName(jsonResultAlbum['artistName'], country)
            for jsonAlbum in jsonAlbums:
                ret = self.__saveAllInfos(jsonAlbum, country)
                if not ret:
                   continue
                infos.append(ret) 

                jsonResultAlbums2 = self.__getInfoByAlbumName(jsonAlbum['collectionName'], country)
                for jsonResultAlbum2 in jsonResultAlbums2:
                    ret = self.__saveAllInfos(jsonResultAlbum2, country)
                    if not ret:
                       continue
                    infos.append(ret) 

                    jsonAlbums2 = self.__getInfoByArtistName(jsonResultAlbum2['artistName'], country)
                    for jsonAlbum2 in jsonAlbums2:
                        ret = self.__saveAllInfos(jsonAlbum2, country)
                        if not ret:
                           continue
                        infos.append(ret) 

        return infos

    def getInfosWithAlbumName(self, albumName, country, limit = 50):
        if not albumName:
           DEBUG.p('Please special the album name')
           return false 
        if not country:
           DEBUG.p('country undefine, use "us" as defaulted')
           country = 'us'
        if limit != 50:
           self.limit = int(limit)

        infos = []
        #get all albums of name 'albumName' 
        jsonResultAlbums = self.__getInfoByAlbumName(albumName, country)
        for jsonResultAlbum in jsonResultAlbums:
            ret = self.__saveAllInfos(jsonResultAlbum, country)
            if not ret: 
               continue
            infos.append(ret) 

        return infos

    def getInfosWithAlbumNameAndArtistName(self, albumName, artistName, country, limit = 50):
        if not albumName and not artistName:
           DEBUG.p('Please special the album name and artist name')
           return false 
        if not country:
           DEBUG.p('country undefine, use "us" as defaulted')
           country = 'us'
        if limit != 50:
           self.limit = int(limit)

        infos = []
        #get all albums of name 'albumName' 
        jsonResultAlbums = self.__getInfoByArtistName(artistName, country)
        for jsonResultAlbum in jsonResultAlbums:
            DEBUG.p('albumName:%s; collectionName:%s'%(albumName, jsonResultAlbum['collectionName']))
            if jsonResultAlbum['collectionName'] == albumName:
                    ret = self.__saveAllInfos(jsonResultAlbum, country)
                    if not ret: 
                       continue
                    infos.append(ret) 

        return infos

    def getInfosWithAlbum_deepdeep(self, albumName, country, limit = 50):
        if not albumName:
           DEBUG.p('Please special the album name')
           return false 
        if not country:
           DEBUG.p('country undefine, use "us" as defaulted')
           country = 'us'
        if limit != 50:
           self.limit = int(limit)

        infos = []
        #get all albums of name 'albumName' 
        jsonResultAlbums = self.__getInfoByAlbumName(albumName, country)
        for jsonResultAlbum in jsonResultAlbums:
            ret = self.__saveAllInfos(jsonResultAlbum, country)
            if not ret: 
               continue
            infos.append(ret) 

            #get all albums of the artist
            infos.extend(self.getInfosWithAritstName_deep(jsonResultAlbum['artistName'], country, limit))
            #get all albums of the album 
            infos.extend(self.getInfosWithAlbumName_deep(jsonResultAlbum['collectionName'], country, limit))
        return infos


itunesapi = ItunesAPI()
if __name__ == '__main__':
    #json = api.__getResponeResult('https://itunes.apple.com/search?term=%E5%AE%89%E5%92%8C%E6%A1%A5%E5%8C%97&country=tw&media=music&entity=album')
    #itunesapi.__getInfoByAlbumName('Bigger, Better, Faster, More!', 'tw')
    itunesapi.getInfosWithAlbum_deepdeep('Bigger, Better, Faster, More!', 'us', 200)
    
