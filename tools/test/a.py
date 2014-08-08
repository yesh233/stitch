from PIL import Image
from numpy import *
import gzip

for i in range(30):
    f = open('imgs/'+str(i)+'.jpg')
    fo = gzip.open('img/'+str(i)+'.zip','w')
    fo.writelines(f)
    fo.close()
    f.close()
