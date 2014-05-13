# coding: UTF-8
import Image
from os.path import getsize
from config import settings

class img:
    def __init__(self):
        self.prePath =  '/home/lulu/albumCovers/static/images/'

    def getImgInfo(self, filename):
        im = Image.open(self.prePath + filename) 
        imgInfo = {}
        imgInfo['width'] = im.size[0]
        imgInfo['height'] = im.size[1]
        imgInfo['format'] = im.format
        imgInfo['size'] = getsize(self.prePath + filename)
        #print imgInfo
        return imgInfo

img = img()
if __name__ == '__main__':
       img.getImgInfo('mzi.wysmcykf.1200x1200-75.jpg')
