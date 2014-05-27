#coding: UTF-8
import os
import re
import urllib2
import urllib
import json

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

class ItunesAPI:
    def __init__(self):
        self.baseUrl = 'https://itunes.apple.com/search?'

    def getResponeResult(self, url):
        self.url = url
        login_data = urllib.urlencode({})
        login_headers = {'Referer':url, 'User-Agent':'Opera/9.60',}
        login_request = urllib2.Request(url, login_data, login_headers)
        result = urllib2.urlopen(login_request).read()
        return json.loads(result.decode("utf-8"))['results']

    def getInfoByAlbumName(self, albumName, country):
        if not albumName:
           print 'Please special the album name'
           return false 
        if not country:
           print 'country undefine, use "us" as defaulted'
           country = 'us'

        #get album info
        url = self.baseUrl + 'term=%s&country=%s&media=music&entity=album'%(albumName, country)
        print url
        jsonResultAlbum = self.getResponeResult(url)
        print 'result count: %d'%(len(jsonResultAlbum))

        #get album musics info
        url = self.baseUrl + 'term=%s&country=%s&media=music'%(albumName, country)
        print url
        jsonResultMusic = self.getResponeResult(url)
        print 'result count: %d'%(len(jsonResultMusic))

        #save album info files 
        artist_dir = os.getcwd() + '/static/images/' + jsonResultAlbum[0]['artistName'] 
        album_dir = artist_dir + '/' + jsonResultAlbum[0]['collectionName'] 
        if not os.path.exists(artist_dir):
           os.makedirs(artist_dir)
        if not os.path.exists(album_dir):
           os.makedirs(album_dir)

        ##save info to json file
        file = open(album_dir + "/album.json","w")
        json.dump(jsonResultAlbum, file)
        file.close()
        file = open(album_dir + "/album_musics.json","w")
        json.dump(jsonResultMusic, file)
        file.close()

        
        ##save album cover images
        coverImageUrl = jsonResultAlbum[0]['artworkUrl100']
        f = urllib2.urlopen(coverImageUrl)
        with open(album_dir + '/' + coverImageUrl.split('/')[-1], 'wb') as code:
            code.write(f.read())
        print('100 Pic Saved!') 
        coverImageUrl_170 = coverImageUrl.replace('100x100', '170x170')
        f = urllib2.urlopen(coverImageUrl_170)
        with open(album_dir + '/' + coverImageUrl_170.split('/')[-1], 'wb') as code:
            code.write(f.read())
        print('170 Pic Saved!') 
        coverImageUrl_1200 = coverImageUrl.replace('100x100', '1200x1200')
        f = urllib2.urlopen(coverImageUrl_1200)
        with open(album_dir + '/' + coverImageUrl_1200.split('/')[-1], 'wb') as code:
            code.write(f.read())
        print('1200 Pic Saved!') 

itunesapi = ItunesAPI()
if __name__ == '__main__':
    #json = api.getResponeResult('https://itunes.apple.com/search?term=%E5%AE%89%E5%92%8C%E6%A1%A5%E5%8C%97&country=tw&media=music&entity=album')
    api.getInfoByAlbumName('Bigger, Better, Faster, More!', 'tw')
