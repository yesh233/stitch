import os
import sys
from numpy import *
from PIL import Image
import gzip
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
    
    def __str__(self):
	return ('block:\n'+str(self.block)+'\n'+
               'plane:\n'+str(self.plane)+'\n'+
	       'scale: '+str(self.scale)+'\n')

    def prepare(self, block_path, imgs_path, camera_list_path, 
	        plane_path):
	self.block = utils.load(block_path)
	for i in self.block.cameras.keys():
	    self.imgs[i] = array(Image.open(imgs_path +
		  str(i)+'.jpg'))
	self.camera_list = utils.load(camera_list_path)
	self.plane = utils.load(plane_path)

    def label_ret(self):
	assert(self.block != None and self.camera_list != None 
		and self.plane != None)
	h, w = self.block.height * self.scale, self.block.width*self.scale
	h, w = int(h), int(w)
	ret = zeros((h,w,3),uint8) 
        for i in range(h): 	
	    for j in range(w):
		idx = self.block.labels[i/self.scale,j/self.scale]
	        pos = self.block.pos(i,j,self.scale)
		pos = self.plane.to_spa(pos)
		pos = self.camera_list.spa_to_img(idx, pos)
	        if pos != None:
		    ret[i,j] = self.imgs[idx][pos]
		else :
		    ret[i,j] = zeros(3,uint8)
        return ret		    

def test():
    R = Ret()
    R.prepare('blk/0.pkl','imgs/','camera_list.pkl','plane.pkl')
    R.scale = 2.0
    im = Image.fromarray(R.label_ret())
    print im.save('1.jpg') 

if __name__ == '__main__':
    test()


    
    





