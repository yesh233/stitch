import os
import sys
from PIL import Image
import numpy as np
import copy as cp
import utils
from blockdata import *
from planedata import *
from cameradata import *

class Ret(object):
    def __init__(self):
	self.block = None
	self.imgs = {}
	self.camera_list = None 
	self.plane = None
	self.scale = 1.0
	self.init_img = None
	self.ava_img = None
	self.img = None
        self.color = None
	self.labels = None
	self.h, self.w = 0, 0
    
    def __str__(self):
	return ('block:\n'+str(self.block)+'\n'+
               'plane:\n'+str(self.plane)+'\n'+
	       'scale: '+str(self.scale)+'\n')

    def prepare(self, block_path, imgs_path, camera_list_path, 
	        plane_path):
	self.block = utils.load(block_path)
	for i in self.block.cameras:
	    self.imgs[i] = np.array(Image.open(imgs_path +
		  str(i)+'.jpg'))
	self.camera_list = utils.load(camera_list_path)
	self.plane = utils.load(plane_path)
	self.h, self.w = self.block.height * self.scale, self.block.width*self.scale
	self.h, self.w = int(self.h), int(self.w)
	self.labels = cp.deepcopy(self.block.labels)
	self.img = zeros((self.h,self.w,3),uint8)

    def img_update(self, box, camera = -1):
	h0,w0,h1,w1 = box
	cnt = 0
        print cnt
        for i in range(h0, h1): 	
	    for j in range(w0, w1):
                ci, cj = i/self.scale, j/self.scale
                if camera == -1:
                    #defulat
                    self.labels[ci,cj] = self.block.labels[ci,cj]
                    self.img[i,j] = self.init_img[i,j]
                else :
                    self.labels[ci,cj] = camera
                    idx = self.labels[ci,cj]    
                    pos = self.block.pos(i,j,self.scale)
		    pos = self.plane.to_spa(pos)
		    pos = self.camera_list.spa_to_img(idx, pos)
	            if pos != None:
		        self.img[i,j] = self.imgs[idx][pos]
		yield cnt
		cnt = cnt + 1
        print cnt


    def init_img(self):
	self.labels = copy.deepcopy(self.block.labels)
	if self.init_img == None:
	    for i in img_update((0,0,self.h,self.w)):
	         pass
	    self.init_img = copy.deepcopy(self.img)
	    

def test():
    R = Ret()
    prefix = '/home/mfkiller/stitch/tools/test/data/'
    R.prepare(prefix+'blocks/4.pkl',prefix+'imgs/',prefix+'cameralist.pkl',
	      prefix+'plane.pkl')
    #R.scale = 10.0
    utils.save(R, '../ret.pkl')

if __name__ == '__main__':
    global color
    color = utils.load('color.pkl')
    test()


    
    





