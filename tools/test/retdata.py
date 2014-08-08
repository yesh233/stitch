import os
import sys
from numpy import *
from PIL import Image
import utils

class Ret(object):
    def __init__(self):
	self.block = None
	self.imgs = {}
	self.camera_list = None 
	self.plane = None
	self.zoom = 1
    
    def prepare(self, block_path, imgs_path, camera_list_path, 
	        plane_path):
	self.block = utils.load(path)
	for i in self.block.cameras.keys():
	    self.imgs[i] = array(Image.open(imgs_path +
		  str(self.block.cameras[i])+'.jpg'))
	self.camera_list = utils.load(camera_list_path)
	self.plane = utils.load(plane_path)

    def label_ret(self):
        pass	
	

    
    





