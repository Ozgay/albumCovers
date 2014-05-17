# coding: UTF-8
import Image
from os.path import basename
from os.path import getsize

class img:
    def __init__(self):
        self.prePath =  ''

    def getImgInfo(self, filePath):
        im = Image.open(filePath) 
        imgInfo = {}
        imgInfo['path'] = filePath 
        imgInfo['name'] = basename(filePath) 
        imgInfo['width'] = im.size[0]
        imgInfo['height'] = im.size[1]
        imgInfo['format'] = im.format
        imgInfo['size'] = getsize(filePath)
        #print imgInfo
        return imgInfo

img = img()
if __name__ == '__main__':
       img.getImgInfo('mzi.wysmcykf.1200x1200-75.jpg')
