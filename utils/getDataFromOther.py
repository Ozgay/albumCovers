# coding: UTF-8
import os
import re
import urllib2
import urllib

class BorrowData:
    def __init__(self):
        self.title = 'sorry'
        self.unicodePage = ''
        self.url = ''

    def getPageSourceCode(self, url):
        self.url = url
        login_data = urllib.urlencode({})
        login_headers = {'Referer':url, 'User-Agent':'Opera/9.60',}
        login_request = urllib2.Request(url, login_data, login_headers)
        html = urllib2.urlopen(login_request).read()
        return html.decode("utf-8")
        
    
    def getMusicListFromXiMi(self, url):
        if len(self.unicodePage) == 0 or url != self.url: 
            self.url = url
            html = self.getPageSourceCode(url)
            self.unicodePage = html 
        myItems = re.findall('<td class="song_name"><a href=(.*?) title="">(.*?)</a>',self.unicodePage,re.S)
        musicList = []
        for item in myItems:
            musicList.append(item[1]) 
        return musicList

    def getArtistAndAlbumFromXiMi(self, url):
        if len(self.unicodePage) == 0 or url != self.url: 
            self.url = url
            html = self.getPageSourceCode(url)
            self.unicodePage = html 
        time = re.findall(u'发行时间：(.*?)<td valign="top">(.*?)</td>', self.unicodePage, re.S)
        artist = re.findall(u'艺人：</td>(.*?)<a href="/artist/(.*?)" title="">(.*?)<', self.unicodePage, re.S)
        album = re.findall('<h1 property="v:itemreviewed">(.*?)</h1>', self.unicodePage, re.S)
        print time[0][1]
        print artist[0][2]
        print album[0]
        return artist[0][2], album[0], time[0][1]

    def getAlbumImageFromUrl(self, url):
        self.url = url
        html = self.getPageSourceCode(url)
        if not len(html) or not html:#try again
           print 'try again'
           html = self.getPageSourceCode(url) 
        if  not len(html):
            print 'get source code failed!!!'
            return 
        self.unicodePage = html

        coverImageUrl_170 = re.findall(u'id="left-stack">(.*?)src="(.*?)" /></div></a>(.*?)><span>View In iTunes</span></a>', self.unicodePage, re.S)
        albumName = re.findall(u'<h1>(.*?)</h1>', self.unicodePage, re.S)
        artist = re.findall(u'<h2><a href="https:(.*?)">(.*?)</a></h2>', self.unicodePage, re.S)
        coverImageUrl_1200 = coverImageUrl_170[0][1].replace('170x170','1200x1200')

        print albumName 
        print artist 
        print coverImageUrl_1200 
        print coverImageUrl_170[0][1]
        
        #save image
        artist_dir = os.getcwd() + '/static/images/' + artist[0][1] 
        album_dir = os.getcwd() + '/static/images/' + artist[0][1] + '/' + albumName[0]
        if not os.path.exists(artist_dir):
           os.makedirs(artist_dir)
        if not os.path.exists(album_dir):
           os.makedirs(album_dir)

        f = urllib2.urlopen(coverImageUrl_170[0][1])
        with open(album_dir + '/' + coverImageUrl_170[0][1].split('/')[-1], 'wb') as code:
            code.write(f.read())
        print('170 Pic Saved!') 
        f = urllib2.urlopen(coverImageUrl_1200)
        with open(album_dir + '/' + coverImageUrl_1200.split('/')[-1], 'wb') as code:
            code.write(f.read())
        print('1200 Pic Saved!') 

        return album_dir + '/' + coverImageUrl_1200.split('/')[-1] 

borrowData = BorrowData()
if __name__ == '__main__':
    print '''test'''
