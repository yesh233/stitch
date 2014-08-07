import os
import sys
from numpy import *
from PIL import Image
import cPickle
import gzip

class Block(object):
    def __init__(self):
	self.__boundings = (0.0, 0.0)  #xmin, ymin
	self.__step = 0.0
	self.__width = 0.0
	self.__height = 0.0
	self.__cameras = []
	self.__small_bounds = []
	self.__labels = array(0)


    def __str__(self):
	return ('boundings(xmin,ymin): '+str(self.__boundings)+'\n'+
               'step: '+str(self.__step)+'\n'+
	       'width: '+str(self.__width)+'\n'+
	       'height: '+str(self.__height)+'\n'+
	       'cameras: '+str(self.__cameras)+'\n'+
	       'small_bounds:\n'+str(self.__small_bounds)+'\n'
	       'labels: \n'+str(self.__labels)+'\n')

    
    def read_from_txt(self, path):
	with open(path) as fp:
	    self.__cameras = map(int, fp.readline().split())
	    fp.readline()
	    l = fp.readline().split()
	    self.__boundings = map(float, l[:2]) 
	    self.__step = float(l[2])
	    l = map(int, fp.readline().split())
	    self.__height, self.__width, self.__n = tuple(l)
	    for i in range(len(self.__cameras)):
		l = fp.readline().split()
		bounds = tuple(map(int, l[1:]))
		self.__small_bounds.append(bounds)
		for i in range(5):
		    fp.readline()

    def read_from_bmp(self, path):
	 with Image.open(path) as im:
	     im = array(im, int32)
	     h, w = im.shape
	     assert(self.__cameras != [])
	     for i in range(h):
		 for j in range (w):
		    im[i,j] = self.__cameras[im[i,j]] 
             self.__labels = im


def saveBlock(block, path):
    with gzip.open(path, 'w') as fp:
	cPickle.dump(block, fp)

def loadBlock(path):
    with gzip.open(path) as fp:
	return cPickle.load(fp)

def test():
    #B = Block()
    #B.read_from_txt('0.txt')
    #B.read_from_bmp('0.bmp')
    #print B
    #saveBlock(B, '0.pkl')
    P = loadBlock('0.pkl')

    print P



if __name__ == '__main__':
    test()

