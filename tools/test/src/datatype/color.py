import sys
import utils
import numpy as np
from PIL import Image

'''
color_list = []
for a in sys.stdin:
    a = a.split()
    color_list.append(np.array(map(int,a[1:4])))

utils.save(color_list, 'color.pkl')
'''

a = np.array(Image.open('../../data/tmp/4.jpg'))
utils.save(a, '4.img.pkl')


