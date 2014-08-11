import os
import sys
from numpy import *
from PIL import Image
import utils

class Block(object):
    def __init__(self):
	self.boundings = (0.0, 0.0)  #xmin, ymin
	self.step = 0.0
	self.width = 0.0
	self.height = 0.0
	self.cameras = {} 
	self.labels = None 

    def __str__(self):
	return ('boundings(xmin,ymin): '+str(self.boundings)+'\n'+
               'step: '+str(self.step)+'\n'+
	       'width: '+str(self.width)+'\n'+
	       'height: '+str(self.height)+'\n'+
	       'cameras: '+str(self.cameras)+'\n'+
	       'labels: \n'+str(self.labels)+'\n')

    
    def read_from_txt(self, path):
	with open(path) as fp:
	    self.lists = map(int, fp.readline().split())
	    fp.readline()
	    l = fp.readline().split()
	    self.boundings = map(float, l[:2]) 
	    self.step = float(l[2])
	    l = map(int, fp.readline().split())
	    self.height, self.width, n = tuple(l)
	    for i in range(n):
		l = fp.readline().split()
		self.cameras[int(l[0])] = tuple(map(int, l[1:]))
		for i in range(5):
		    fp.readline()

    def read_from_bmp(self, path):
	im = array(Image.open(path), int32)
        h, w = im.shape
	assert(self.lists != None and self.lists != [])
	for i in range(h):
	    for j in range (w):
	        im[i,j] = self.lists[im[i,j]] 
        self.labels = im
	del self.lists
    

    def pos(self, x, y, scale=1.0):
	xmin,ymin = self.boundings
	return (xmin+self.step*x/scale,ymin+self.step*y/scale)

    def merge_from_matrix(self, blocks):
	assert(len(blocks) != 0)
	nh, nw = len(blocks), len(blocks[0])
	sample = blocks[0][0]
	h, w = sample.height, sample.width
	self.boundings, self.step = sample.boundings, sample.step
	self.width, self.height = sample.width*nw, sample.height*nh
	self.labels = zeros((self.height, self.width), int32)
	for i in range(nh):
	    for j in range(nw):
		for k in blocks[i][j].cameras.keys():
		    if self.cameras.has_key(k):
			self.cameras[k] = camera_update(self.cameras[k], 
				blocks[i][j].cameras[k], (i*h,j*w))
		    else:
			self.cameras[k] = blocks[i][j].cameras[k]
		self.labels[i*h:(i+1)*h,j*w:(j+1)*w] = blocks[i][j].labels	

def camera_update(a, b, o):
    xmin = min(a[0], b[0]+o[0])
    ymin = min(a[1], b[1]+o[1])
    xmax = max(a[2], b[2]+o[0])
    ymax = max(a[3], b[3]+o[1])
    return (xmin,ymin,xmax,ymax)

def test():
    B0 = utils.load('blk/0.pkl')
    B1 = utils.load('blk/1.pkl')
    B2 = utils.load('blk/4.pkl')
    B3 = utils.load('blk/5.pkl')
    
    BM = [[B0,B1],[B2,B3]]
    P = Block()
    P.merge_from_matrix(BM)
    utils.save(P, 'mb.pkl')
    print P



if __name__ == '__main__':
    test()

