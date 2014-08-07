import os
import sys
from numpy import *
import cPickle
import gzip

class Camera(object):
    def __init__(self):
	self.__R = zeros((3,3), float32)
	self.__T = zeros((3,1), float32)
	self.__K = zeros((3,3), float32)
    
    def __str__(self):
	return ('R:\n' + str(self.__R) +'\n' +
               'T:\n' + str(self.__T) +'\n' +
	       'K:\n' + str(self.__K) +'\n')

    def set_RTK(self, R, T, K):
	self.__R, self.__T, self.__K = R, T, K


class CameraList(object):
    def __init__(self, scale, shape):
	self.__cameras = []
	self.__scale = scale 
	self.__shape = shape

    def __str__(self):
	return ('scale: ' + str(self.__scale) + '\n' + 
               'shape: ' + str(self.__shape) + '\n' + 
	       '\n'.join(map(str, self.__cameras)) + '\n')

    def read_from_bundle(self, path):
	with open(path) as fp:
	    fp.readline()
	    n = int(fp.readline().split()[0])
	    for i in range(n):
		focal, k1, k2 = map(float, fp.readline().split())
                R = [map(float, fp.readline().split()) for i in range(3)]
		T = map(lambda x:[float(x)], fp.readline().split())
		K = zeros((3,3), float32) 
		K[0,0] = K[1,1] = focal * self.__scale
		K[2,2] = 1
		f = lambda x:array(x, float32)
		c = Camera()
		c.set_RTK(f(R),f(T),f(K))
		self.__cameras.append(c)

def saveCameraList(camera_list, path):
    with gzip.open(path, 'w') as fp:
	cPickle.dump(camera_list, fp)

def loadCameraList(path):
    with gzip.open(path) as fp:
	return cPickle.load(fp)

	
def test():
    #camera_list = CameraList(10, (4912,7360))
    #camera_list.read_from_bundle('bundle.out')
    #print camera_list
    #saveCameraList(camera_list, 'camera_list.pkl')
    C = loadCameraList('camera_list.pkl')
    print C


if __name__ == '__main__':
    test()
			


    

	
