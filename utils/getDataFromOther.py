# coding: UTF-8
import os
import re
import urllib2
import urllib
#from config import settings

class BorrowData:
    def __init__(self):
        self.title = 'sorry'
        self.unicodePage = ''
        self.url = ''
    
    def getMusicListFromXiMi(self, url):
        if len(self.unicodePage) == 0 or url != self.url: 
            self.url = url
            login_data = urllib.urlencode({})
            login_headers = {'Referer':url, 'User-Agent':'Opera/9.60',}
            login_request = urllib2.Request(url, login_data, login_headers)
            html = urllib2.urlopen(login_request).read()
            self.unicodePage = html.decode("utf-8")
        #response = urllib2.urlopen(url)  
        #html = response.read() 
        myItems = re.findall('<td class="song_name"><a href=(.*?) title="">(.*?)</a>',self.unicodePage,re.S)
        musicList = []
        for item in myItems:
            musicList.append(item[1]) 
        return musicList

    def getArtistAndAlbumFromXiMi(self, url):
        if len(self.unicodePage) == 0 or url != self.url: 
            self.url = url
            login_data = urllib.urlencode({})
            login_headers = {'Referer':url, 'User-Agent':'Opera/9.60',}
            login_request = urllib2.Request(url, login_data, login_headers)
            html = urllib2.urlopen(login_request).read()
            self.unicodePage = html.decode("utf-8")
        time = re.findall(u'发行时间：(.*?)<td valign="top">(.*?)</td>', self.unicodePage, re.S)
        artist = re.findall(u'艺人：</td>(.*?)<a href="/artist/(.*?)" title="">(.*?)<', self.unicodePage, re.S)
        album = re.findall('<h1 property="v:itemreviewed">(.*?)</h1>', self.unicodePage, re.S)
        print time[0][1]
        print artist[0][2]
        print album[0]
        return artist[0][2], album[0], time[0][1]

    def getAlbumImageFromUrl(self, url):
        self.url = url
        login_data = urllib.urlencode({})
        login_headers = {'Referer':url, 'User-Agent':'Opera/9.60',}
        login_request = urllib2.Request(url, login_data, login_headers)
        html = urllib2.urlopen(login_request).read()
        self.unicodePage = html.decode("utf-8")

        coverImageUrl = re.findall(u'<div id="left-stack">(.*?)src="(.*?)" /></div></a>(.*?)><span>View In iTunes</span></a>', self.unicodePage, re.S)
        result = coverImageUrl[0][1].replace('170x170','1200x1200')
        
        #save image
        #dst = settings.config.static + '/images/' 
        dst = './xxoo.jpg'
        f = urllib2.urlopen(result)
        with open(dst, 'wb') as code:
            code.write(f.read())
        print('Pic Saved!') 
        print result 

borrowData = BorrowData()
if __name__ == '__main__':
        borrowData.getMusicListFromXiMi('http://www.xiami.com/album/170743?spm=0.0.0.0.DY9VVn')
        borrowData.getArtistAndAlbumFromXiMi('http://www.xiami.com/album/170743?spm=0.0.0.0.DY9VVn')
        borrowData.getAlbumImageFromUrl('https://itunes.apple.com/us/album/bigger-better-faster-more!/id362946')
