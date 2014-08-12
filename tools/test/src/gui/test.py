import os
import sys
import platform
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import numpy as np
from PIL import Image
import pyqtgraph as pg

class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
	w = pg.GraphicsView()
	centralWidget = QWidget()
	layout = QVBoxLayout()
	button = QPushButton('button')
	layout.addWidget(w)
	layout.addWidget(button)
	centralWidget.setLayout(layout)
	self.setCentralWidget(centralWidget)

	view = pg.ViewBox()
	view.setAspectLocked()
        self.arr = np.array(Image.open('/home/mfkiller/stitch/tools/test/data/tmp/1.jpg'))
	self.img = pg.ImageItem(self.arr)
	roi = pg.ROI([100,100],[500,500])
	roi.addScaleHandle([1,0],[0.5,0.5])
	view.addItem(roi)
	view.addItem(self.img)
	w.setCentralItem(view)
	self.flag = 0
	print self.arr.shape
	def P():
	   #a,b=  roi.getArrayRegion(arr, img, returnMappedCoords=True)
	   #k,w,h = b.shape 
	   #print b[0,0,0]
	   print 'shit'
	   if self.flag == 0:
	       for i in range(300,900):
		   for j in range(300,900):
		       self.arr[i,j] = [0,0,0]
	   else:
	       for i in range(300,900):
		   for j in range(300,900):
		       self.arr[i,j] = [255,255,255]
           self.flag = (self.flag + 1 ) % 2
	   self.img.setImage(self.arr)

	button.clicked.connect(P)

        self.setWindowTitle("Test")

def main():
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()
