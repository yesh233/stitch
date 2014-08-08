import os
import sys
from numpy import *
import utils

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

    def spa_to_img(self, pos):
	X = mat(pos).T
	X = mat(self.__R)*X
	X = X + mat(self.__T)
	X = mat(self.__K)*X
	return tuple(map(float, X))

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

    def spa_to_img(self, idx, pos):
	x,y,z = self.__cameras[idx].spa_to_img(pos)
	if z == 0:
	    return (-1,-1)
	else :
	    x,y = -x/z, -y/z
	    h,w = self.__shape
	    h,w = h/2,w/2	
	    if abs(x)+5<w and abs(y)+5<h:
		x,y = x+w, y+h
		x,y = 2*h-y, x
	        return (x,y)
	    else :
		return (-1,-1)
	    


def test():
    #camera_list = CameraList(10, (4912,7360))
    #camera_list.read_from_bundle('bundle.out')
    #print camera_list
    #saveCameraList(camera_list, 'camera_list.pkl')
    C = utils.load('camera_list.pkl')
    print C


if __name__ == '__main__':
    test()
			


    

	
