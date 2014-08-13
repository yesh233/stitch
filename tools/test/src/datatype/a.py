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
	self.emit(SIGNAL("moved"), ev.pos())

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
	super(MainWindow, self).__init__(parent)
	self.ret = Ret()  

	w = pg.GraphicsView()
	centralWidget = QWidget()
	vlayout = QVBoxLayout()
	vlayout.addWidget(w)
	hlayout = QHBoxLayout()
	prepare_button = QPushButton('prepare')
	default_button = QPushButton('default')
	self.select_button = QPushButton('select')
	hlayout.addWidget(prepare_button)
	hlayout.addWidget(default_button)
	hlayout.addWidget(self.select_button)
	self.select_button.setCheckable(True)
	vlayout.addLayout(hlayout)
	centralWidget.setLayout(vlayout)
	self.setCentralWidget(centralWidget)


        cameraDockWidget = QDockWidget('Cameras', self)
	cameraDockWidget.setObjectName('cameraDockWidget')
        cameraDockWidget.setAllowedAreas(Qt.LeftDockWidgetArea|
		Qt.RightDockWidgetArea)
	self.listWidget = QListWidget()
	cameraDockWidget.setWidget(self.listWidget)
	self.addDockWidget(Qt.RightDockWidgetArea, cameraDockWidget)

	self.view = pg.ViewBox()
	self.view.setAspectLocked()
	self.img = myImageItem()
	self.view.addItem(self.img)
	w.setCentralItem(self.view)
	
	prepare_button.clicked.connect(self.prepare)
	default_button.clicked.connect(self.default)
	self.select_button.clicked.connect(self.select)
	self.connect(self.img, SIGNAL('moved'), self.hehe)

	self.setWindowTitle('Yesh233')

    def hehe(self, pos):
	print pos.x(), pos.y() 

    def prepare(self):
	prefix = '/home/mfkiller/stitch/tools/test/data/'
	self.ret.scale = 1
	self.ret.prepare(prefix+'blocks/4.pkl',prefix+'imgs/',prefix+'cameralist.pkl',
		prefix+'plane.pkl')
	self.roi = pg.ROI([self.ret.h/4,self.ret.w/4],[self.ret.h/2,self.ret.w/2])
        self.roi.addScaleHandle([1,0],[0.5,0.5])
	print 'prepare finished'

    def default(self):
	self.ret.labels = cp.deepcopy(self.ret.block.labels)
	if self.ret.init_img == None:
	    progress = QProgressDialog(u'生成...',u'取消',0,self.ret.w*self.ret.h-1,
		    self)
            progress.setWindowTitle(u'请等待')
	    progress.setWindowModality(Qt.ApplicationModal)
	    for i in self.ret.img_update((0,0,self.ret.h,self.ret.w)):
		progress.setValue(i)
            self.ret.init_img = self.ret.img
	else:
	    self.ret.img = self.ret.init_img
        self.img.setImage(self.ret.img)

    def select(self):
	if self.select_button.isChecked():
	    self.view.addItem(self.roi)
	else:
	    self.view.removeItem(self.roi)
	

def main():
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()

