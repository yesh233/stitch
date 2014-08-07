import os
import sys
from numpy import *
import cPickle
import gzip

class Plane(object):
    def __init__(self):
	self.__boundings = (0.0, 0.0, 0.0, 0.0) #xmin,ymin,xmax,ymax 
	self.__coeffients = (0.0, 0.0, 0.0, 0.0)

    def __str__(self):
	return 'boundings(xmin,ymin,xmax,ymax): %s \ncoeffients: %s \n' % \
		(self.__boundings, self.__coeffients)

    def read_from_txt(self, path):
	with open(path) as fp:
	    l = map(float, fp.readline().split())
	    self.__coeffients = tuple(l)
	    l = map(float, fp.readline().split())
	    self.__boundings = tuple(l)

def savePlane(plane, path):
    with gzip.open(path, 'w') as fp:
	cPickle.dump(plane, fp)

def loadPlane(path):
    with gzip.open(path) as fp:
	return cPickle.load(fp)

def test():
    B = loadPlane('plane.pkl') 
    print B

if __name__ == '__main__':
    test()


    

	    



	

