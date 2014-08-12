import os
import sys
import utils
from blockdata import *
from cameradata import *
from planedata import *

def main():
    prefix = '/home/mfkiller/stitch/hdfs/1/' 
    savepath = '/home/mfkiller/stitch/tools/test/data/'
    P = Plane()  
    P.read_from_txt(prefix+'plane.txt')
    utils.save(P, savepath+'plane.pkl')
    C = CameraList(10, (4912,7360))
    C.read_from_bundle(prefix+'bundle.out')
    utils.save(C, savepath+'cameralist.pkl')
    for i in range(16):
	B = Block()
	B.read_from_txt(prefix+'blocks/'+str(i)+'.txt')
	B.read_from_bmp(prefix+'labels/'+str(i)+'.bmp')
	utils.save(B, savepath+'blocks/'+str(i)+'.pkl')
    
def test():
   pass 

if __name__ == '__main__':
    main()
