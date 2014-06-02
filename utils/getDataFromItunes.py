#coding: UTF-8
import os
import re
import urllib2
import urllib
import json
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

    def __getResponeResult(self, url):
        try:
            login_data = urllib.urlencode({})
            login_headers = {'Referer':url, 'User-Agent':'Opera/9.60',}
            login_request = urllib2.Request(url, login_data, login_headers)
            result = urllib2.urlopen(login_request).read()
            return json.loads(result.decode("utf-8"))['results']
        except:
            DEBUG.p('get data failed, and try again...')
            try:
                login_data = urllib.urlencode({})
                login_headers = {'Referer':url, 'User-Agent':'Opera/9.60',}
                login_request = urllib2.Request(url, login_data, login_headers)
                result = urllib2.urlopen(login_request).read()
                return json.loads(result.decode("utf-8"))['results']
            except:
                DEBUG.p('err: get data failed from: %s' % (url))
                result = []
                return result

    def __saveCoverImage(self, album_dir, coverImageUrl):
        try:
            f = urllib2.urlopen(coverImageUrl)
            with open(album_dir + '/' + coverImageUrl.split('/')[-1], 'wb') as code:
                code.write(f.read())
            DEBUG.p('%s Pic Saved!' % (coverImageUrl.split('/')[-1])) 
        except:
            DEBUG.p('%s Pic Saved failed! and try again...' % (coverImageUrl.split('/')[-1])) 
            try:
                f = urllib2.urlopen(coverImageUrl)
                with open(album_dir + '/' + coverImageUrl.split('/')[-1], 'wb') as code:
                    code.write(f.read())
                DEBUG.p('%s Pic Saved!' % (coverImageUrl.split('/')[-1])) 
            except:
                DEBUG.p('err: %s Pic Saved failed!' % (coverImageUrl.split('/')[-1])) 

    def __getMusicLists(self, albumName, country):
        #get album musics info
        url = self.baseUrl + 'term=%s&country=%s&media=music'%(albumName, country)
        DEBUG.p(url)
        jsonResultMusics = self.__getResponeResult(url)
        DEBUG.p('result count: %d'%(len(jsonResultMusics)))
        return jsonResultMusics

    def __saveAllInfos(self, jsonResultAlbum, country):
        #prepare dir
        artist_dir = os.getcwd() + '/static/images/' + jsonResultAlbum['artistName'] 
        album_dir = artist_dir + '/' + jsonResultAlbum['collectionName'] 
        if not os.path.exists(artist_dir):
           os.makedirs(artist_dir)
        if not os.path.exists(album_dir):
           os.makedirs(album_dir)
        else:
           DEBUG.p('this album info exist!!!!')
           result = dao.getById(jsonResultAlbum['artistName'], jsonResultAlbum['collectionName']) 
           return

        #save album info json file
        file = open(album_dir + "/album.json","w")
        json.dump(jsonResultAlbum, file)
        file.close()

        
        ##save album cover images
        coverImageUrl = jsonResultAlbum['artworkUrl100']
        self.__saveCoverImage(album_dir, coverImageUrl)
        coverImageUrl_170 = coverImageUrl.replace('100x100', '170x170')
        self.__saveCoverImage(album_dir, coverImageUrl_170)
        coverImageUrl_1200 = coverImageUrl.replace('100x100', '1200x1200')
        self.__saveCoverImage(album_dir, coverImageUrl_1200)

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

        #save music list json file
        file = open(album_dir + "/album_musics.json","w")
        json.dump(jsonMusics, file)
        file.close()

        info['music_contain'] = musicContains 
        DEBUG.pd(info)

        return info
        
    def getInfoByAlbumName(self, albumName, country):
        if not albumName:
           DEBUG.p('Please special the album name')
           return false 
        if not country:
           DEBUG.p('country undefine, use "us" as defaulted')
           country = 'us'

        #get album info
        url = self.baseUrl + 'term=%s&country=%s&media=music&entity=album'%(albumName, country)
        DEBUG.p(url)
        jsonResultAlbums = self.__getResponeResult(url)
        DEBUG.p('result count: %d'%(len(jsonResultAlbums)))

        infos = []
        for jsonResultAlbum in jsonResultAlbums:
            ret = self.__saveAllInfos(jsonResultAlbum, country)
            if not ret: 
               continue
            infos.append(ret) 
            #enter db
            dao.addOneDoc(ret)
            #get all albums of the artist
            url = self.baseUrl + 'term=%s&country=%s&media=music&entity=album'%(jsonResultAlbum['artistName'], country)
            DEBUG.p(url)
            jsonAlbums = self.__getResponeResult(url)
            DEBUG.p('result count: %d'%(len(jsonAlbums)))
            for jsonAlbum in jsonAlbums:
                #get album info
                url = self.baseUrl + 'term=%s&country=%s&media=music&entity=album'%(jsonAlbum['collectionName'], country)
                DEBUG.p(url)
                jsonResultAlbums2 = self.__getResponeResult(url)
                DEBUG.p('result count: %d'%(len(jsonResultAlbums2)))
                for jsonResultAlbum2 in jsonResultAlbums2:
                    ret = self.__saveAllInfos(jsonResultAlbum2, country)
                    if not ret:
                       continue
                    infos.append(ret) 
                    #enter db
                    dao.addOneDoc(ret)


        return infos

itunesapi = ItunesAPI()
if __name__ == '__main__':
    #json = api.__getResponeResult('https://itunes.apple.com/search?term=%E5%AE%89%E5%92%8C%E6%A1%A5%E5%8C%97&country=tw&media=music&entity=album')
    api.getInfoByAlbumName('Bigger, Better, Faster, More!', 'tw')
