# -*- coding: utf-8 -*-
import os
import sys
import platform
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import numpy as np
import copy as cp
from PIL import Image
import pyqtgraph as pg
from retdata import *

class myImageItem(pg.ImageItem):
    def hoverEvent(self, ev):
	try :
	   self.emit(SIGNAL("moved"), ev.pos())
	except Exception:
	    pass

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
	super(MainWindow, self).__init__(parent)
	self.ret = Ret()  

        #layout
	w = pg.GraphicsView()
	w.setMinimumSize(200,200)
	centralWidget = QWidget()
	vlayout = QVBoxLayout()
	vlayout.addWidget(w)
	hlayout = QHBoxLayout()
	prepare_button = QPushButton('prepare')
	default_button = QPushButton('default')
	update_button = QPushButton('update')
	self.select_button = QPushButton('select')
	hlayout.addStretch()
	hlayout.addWidget(prepare_button)
	hlayout.addWidget(default_button)
	hlayout.addWidget(self.select_button)
	hlayout.addWidget(update_button)
	hlayout.addStretch()
	self.select_button.setCheckable(True)
	vlayout.addLayout(hlayout)
	centralWidget.setLayout(vlayout)
	self.setCentralWidget(centralWidget)

        #dock
        cameraDockWidget = QDockWidget('Cameras', self)
	cameraDockWidget.setObjectName('cameraDockWidget')
        cameraDockWidget.setAllowedAreas(Qt.LeftDockWidgetArea|
		Qt.RightDockWidgetArea)
	self.listWidget = QListWidget()
	cameraDockWidget.setWidget(self.listWidget)
	cameraDockWidget.setMinimumWidth(110)
	cameraDockWidget.setMaximumWidth(110)
	cameraDockWidget.setContentsMargins(5,5,5,5)
	self.addDockWidget(Qt.RightDockWidgetArea, cameraDockWidget)

        #viewbox
	self.view = pg.ViewBox()
	self.view.setAspectLocked()
	self.img = myImageItem()
	self.view.addItem(self.img)
	w.setCentralItem(self.view)
         
	#status bar
	self.posLabel = QLabel()
	self.posLabel.setFrameStyle(QFrame.StyledPanel|QFrame.Sunken)
	status = self.statusBar()
	status.setSizeGripEnabled(False)
	status.addPermanentWidget(self.posLabel)
	status.showMessage("Ready", 5000)

        #roi
	self.roi = pg.ROI([0,0], [100,100])
        self.roi.addScaleHandle([1,0],[0,1])
	self.roi.sigRegionChanged.connect(self.update_list)

	prepare_button.clicked.connect(self.prepare)
	default_button.clicked.connect(self.default)
	self.select_button.clicked.connect(self.select)
	update_button.clicked.connect(self.update)
	self.connect(self.img, SIGNAL('moved'), self.update_pos)

	self.setWindowTitle('Yesh233')
	self.setGeometry(500,400,600,500)

    def update_pos(self, pos):
	try:
	    x, y,scale = int(pos.x()), int(pos.y()),self.ret.scale
	    self.posLabel.setText("Pos: [{0},{1}]".format(x,y))
	    self.statusBar().showMessage('From Camera: {0}'. \
		    format(self.ret.labels[x/scale,y/scale]), 5000)
	except Exception:
	    pass


    def update_list(self):
	self.listWidget.clear()
	x0,y0 = self.roi.pos().x(), self.roi.pos().y()
	x1,y1 = x0+self.roi.size().x(), y0+self.roi.size().y()
	x0,y0,x1,y1 = map(lambda x:int(x/self.ret.scale),[x0,y0,x1,y1])
	for i in self.ret.block.cameras:
	    a0,b0,a1,b1 = self.ret.block.cameras[i]
	    if a0 < x1 and b0 < y1 and a1 > x0 and b1 > y0:
		self.listWidget.addItem(str(i))

    def prepare(self):
	prefix = '/home/mfkiller/stitch/tools/test/data/'
	self.ret.scale = 15
	self.ret.init_img = np.array(Image.open(prefix+'tmp/4.jpg'))
	self.ret.prepare(prefix+'blocks/4.pkl',prefix+'imgs/',prefix+'cameralist.pkl',
		prefix+'plane.pkl')
	self.ret.img = cp.deepcopy(self.ret.init_img)
        self.img.setImage(self.ret.img)
	print 'prepare finished'


    def update(self):
	if self.select_button.isChecked() and self.listWidget.currentItem() != None:
	    x0,y0 = self.roi.pos().x(), self.roi.pos().y()
	    x1,y1 = x0+self.roi.size().x(), y0+self.roi.size().y()
	    x0,y0,x1,y1 = map(int,[x0,y0,x1,y1])
	    c = int(self.listWidget.currentItem().text())
	    progress = QProgressDialog(u'UPDATING...',u'Cancel',0,(x1-x0)*(y1-y0)-1,self)
	    progress.setWindowTitle(u'Please Waiting')
	    progress.setWindowModality(Qt.ApplicationModal)
	    for i in self.ret.img_update((x0,y0,x1,y1),c):
		progress.setValue(i)
	    self.img.setImage(self.ret.img)

    def default(self):
	if self.select_button.isChecked():
	    x0,y0 = self.roi.pos().x(), self.roi.pos().y()
	    x1,y1 = x0+self.roi.size().x(), y0+self.roi.size().y()
	    x0,y0,x1,y1 = map(int,[x0,y0,x1,y1])
	    progress = QProgressDialog(u'RESTORING...',u'CANCEL',0,(x1-x0)*(y1-y0)-1,self)
	    progress.setWindowTitle(u'Please Waiting')
	    progress.setWindowModality(Qt.ApplicationModal)
	    for i in self.ret.img_update((x0,y0,x1,y1)):
		progress.setValue(i)
	    self.img.setImage(self.ret.img)


    def select(self):
	if self.select_button.isChecked():
	    self.view.addItem(self.roi)
	    self.update_list()
	else:
	    self.view.removeItem(self.roi)
	    self.listWidget.clear()
	

def main():
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()

