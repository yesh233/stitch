import os
import sys

def dis((x1,y1),(x2,y2)):
	return (x1-x2)*(x1-x2)+(y1-y2)*(y1-y2)

f = open("../../input/coor.txt", "r")
d = {}
coor = f.readlines()
for c in coor:
	c = c.split()
	d[int(c[0])] = (float(c[1]), float(c[2]))
f.close()

a = []
for parent,dirnames,filenames in os.walk('S-imgs'):
	for filename in filenames:
		a.append(int(filename[4:8]))
a.sort()

a = zip(range(len(a)), a)

f = open("../../input/ad.txt", "w")
f.write(str(len(a))+'\n')
for (idx,x) in a:
	c = []
	for (idy, y) in a:
		if not x == y and y < x:
			c.append((dis(d[x],d[y]), y, idy))
	c.sort()
	c = map(lambda (x,y,z): str(z), c[0:20])
	f.write(str(len(c)) + ' ' + ' '.join(c) + '\n')
f.close()



