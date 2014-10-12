#coding:utf-8
import sys, os
sys.path.append('/home/lewis/lulu/albumCovers/')
import urllib2
import json
import re
sys.path.append('/home/lewis/lulu/albumCovers/utils/')
from getDataFromItunes import itunesapi 

country_code = [ 
    ['deep', 'default'],
    ['ae', 'United Arab Emirates'],
    ['ag', 'Antigua and Barbuda'],
    ['ai', 'Anguilla'],
    ['al', 'Albania'],
    ['am', 'Armenia'],
    ['ao', 'Angola'],
    ['ar', 'Argentina'],
    ['at', 'Austria'],
    ['au', 'Australia'],
    ['az', 'Azerbaijan'],
    ['bb', 'Barbados'],
    ['be', 'Belgium'],
    ['bf', 'Burkina-Faso'],
    ['bg', 'Bulgaria'],
    ['bh', 'Bahrain'],
    ['bj', 'Benin'],
    ['bm', 'Bermuda'],
    ['bn', 'Brunei Darussalam'],
    ['bo', 'Bolivia'],
    ['br', 'Brazil'],
    ['bs', 'Bahamas'],
    ['bt', 'Bhutan'],
    ['bw', 'Botswana'],
    ['by', 'Belarus'],
    ['bz', 'Belize'],
    ['ca', 'Canada'],
    ['cg', 'Democratic Republic of the Congo'],
    ['ch', 'Switzerland'],
    ['cl', 'Chile'],
    ['cn', 'China'],
    ['co', 'Colombia'],
    ['cr', 'Costa Rica'],
    ['cv', 'Cape Verde'],
    ['cy', 'Cyprus'],
    ['cz', 'Czech Republic'],
    ['de', 'Germany'],
    ['dk', 'Denmark'],
    ['dm', 'Dominica'],
    ['do', 'Dominican Republic'],
    ['dz', 'Algeria'],
    ['ec', 'Ecuador'],
    ['ee', 'Estonia'],
    ['eg', 'Egypt'],
    ['es', 'Spain'],
    ['fi', 'Finland'],
    ['fj', 'Fiji'],
    ['fm', 'Federated States of Micronesia'],
    ['fr', 'France'],
    ['gb', 'United Kingdom'],
    ['gd', 'Grenada'],
    ['gh', 'Ghana'],
    ['gm', 'Gambia'],
    ['gr', 'Greece'],
    ['gt', 'Guatemala'],
    ['gw', 'Guinea Bissau'],
    ['gy', 'Guyana'],
    ['hk', 'Hong Kong'],
    ['hn', 'Honduras'],
    ['hr', 'Croatia'],
    ['hu', 'Hungaria'],
    ['id', 'Indonesia'],
    ['ie', 'Ireland'],
    ['il', 'Israel'],
    ['in', 'India'],
    ['is', 'Iceland'],
    ['it', 'Italy'],
    ['jm', 'Jamaica'],
    ['jo', 'Jordan'],
    ['jp', 'Japan'],
    ['ke', 'Kenya'],
    ['kg', 'Krygyzstan'],
    ['kh', 'Cambodia'],
    ['kn', 'Saint Kitts and Nevis'],
    ['kr', 'South Korea'],
    ['kw', 'Kuwait'],
    ['ky', 'Cayman Islands'],
    ['kz', 'Kazakhstan'],
    ['la', 'Laos'],
    ['lb', 'Lebanon'],
    ['lc', 'Saint Lucia'],
    ['lk', 'Sri Lanka'],
    ['lr', 'Liberia'],
    ['lt', 'Lithuania'],
    ['lu', 'Luxembourg'],
    ['lv', 'Latvia'],
    ['md', 'Moldova'],
    ['mg', 'Madagascar'],
    ['mk', 'Macedonia'],
    ['ml', 'Mali'],
    ['mn', 'Mongolia'],
    ['mo', 'Macau'],
    ['mr', 'Mauritania'],
    ['ms', 'Montserrat'],
    ['mt', 'Malta'],
    ['mu', 'Mauritius'],
    ['mw', 'Malawi'],
    ['mx', 'Mexico'],
    ['my', 'Malaysia'],
    ['mz', 'Mozambique'],
    ['na', 'Namibia'],
    ['ne', 'Niger'],
    ['ng', 'Nigeria'],
    ['ni', 'Nicaragua'],
    ['nl', 'Netherlands'],
    ['np', 'Nepal'],
    ['no', 'Norway'],
    ['nz', 'New Zealand'],
    ['om', 'Oman'],
    ['pa', 'Panama'],
    ['pe', 'Peru'],
    ['pg', 'Papua New Guinea'],
    ['ph', 'Philippines'],
    ['pk', 'Pakistan'],
    ['pl', 'Poland'],
    ['pt', 'Portugal'],
    ['pw', 'Palau'],
    ['py', 'Paraguay'],
    ['qa', 'Qatar'],
    ['ro', 'Romania'],
    ['ru', 'Russia'],
    ['sa', 'Saudi Arabia'],
    ['sb', 'Soloman Islands'],
    ['sc', 'Seychelles'],
    ['se', 'Sweden'],
    ['sg', 'Singapore'],
    ['si', 'Slovenia'],
    ['sk', 'Slovakia'],
    ['sl', 'Sierra Leone'],
    ['sn', 'Senegal'],
    ['sr', 'Suriname'],
    ['st', 'Sao Tome e Principe'],
    ['sv', 'El Salvador'],
    ['sz', 'Swaziland'],
    ['tc', 'Turks and Caicos Islands'],
    ['td', 'Chad'],
    ['th', 'Thailand'],
    ['tj', 'Tajikistan'],
    ['tm', 'Turkmenistan'],
    ['tn', 'Tunisia'],
    ['tr', 'Turkey'],
    ['tt', 'Republic of Trinidad and Tobago'],
    ['tw', 'Taiwan'],
    ['tz', 'Tanzania'],
    ['ua', 'Ukraine'],
    ['ug', 'Uganda'],
    ['us', 'United States of America'],
    ['uy', 'Uruguay'],
    ['uz', 'Uzbekistan'],
    ['vc', 'Saint Vincent and the Grenadines'],
    ['ve', 'Venezuela'],
    ['vg', 'British Virgin Islands'],
    ['vn', 'Vietnam'],
    ['ye', 'Yemen'],
    ['za', 'South Africa'],
    ['zw', 'Zimbabwe'],
]

luooUrl = 'http://www.luoo.net/music/'

def getMusicListFromLuoo(vol):
    page = urllib2.urlopen(luooUrl + '%d'%(vol)).read()
    matchs = re.findall(r'<p class="name">(.*?)</p>\n\t\t\t\t\t\t\t\t\t\t<p class="artist">Artist: (.*?)</p>\n\t\t\t\t\t\t\t\t\t\t<p class="album">Album: (.*?)</p>', page, re.S)
    jsonFile = os.getcwd() + '/tmp/VOL%d.json'%(vol)
    list = [] 
    if matchs:
        nu = len(matchs)
        print u'vol%d: music number: %d' % (vol,nu)
        for match in matchs:
            list.append(match) 
        #save music list into json file
        file = open(jsonFile,"w")
        json.dump(list, file)
        file.close()
    else:
        print u'vol%d; get music number failed!!!!'%(vol)

    return list

def getInfoByJsonFile(vol):
    print 'start get VOL %d'%(vol)
    jsonFile = os.getcwd() + '/tmp/VOL%d.json'%(vol)
    if not os.path.exists(jsonFile):
       print jsonFile + ' not exist'
       return
    failedJsonFile = os.getcwd() + '/tmp/vol%d.json'%(vol)
    if not os.path.exists(failedJsonFile):
       failedJson = []
    else:
       file = open(failedJsonFile,"r")
       failedJson = json.load(file) 
       file.close()

    count = 0
    country = 'us'
    limit = 200
    albumName = ''
    artistName = ''
    jsonMusicList = json.load(open(jsonFile, 'r')) 
    for item in country_code:
            country = item[0]
            for music in jsonMusicList:
                print 'name:%s; artist:%s; album:%s'%(music[0], music[1], music[2])
                artistName = music[1]
                albumName = music[2]
                if country == 'deep' and albumName:
                    print('get deep creep: %s' % (albumName))
                    infos = itunesapi.getInfosWithAlbumName_deep(albumName, None, limit)
                    count += len(infos)
                if country == 'deep' and artistName:
                    print('get deep creep: %s' % (artistName))
                    infos = itunesapi.getInfosWithAritstName_deep(artistName, None, limit)
                    count += len(infos)
                if albumName: 
                    print('get album: %s' % (albumName))
                    infos = itunesapi.getInfosWithAlbumName(albumName, country, limit)
                    count += len(infos)
                if artistName: 
                    print('get album by %s' % (artistName))
                    infos = itunesapi.getInfosWithArtistName(artistName, country, limit)
                    count += len(infos)

                print 'Get %d album info!!!' % (count)
                if count == 0:
                   print 'failed get info by music:'
                   print music 
                   failedJson.append(music)
                   #save failed music list into json file
                   file = open(failedJsonFile,"w")
                   json.dump(failedJson, file)
                   file.close()

    ##remove origin VOLx.json
    #os.remove(jsonFile)
    

if __name__ == '__main__':
   #1-625
   for i in range(1, 2):
       print 'start get vol%d info'%(i)
       #getMusicListFromLuoo(i)
       getInfoByJsonFile(i)
       
