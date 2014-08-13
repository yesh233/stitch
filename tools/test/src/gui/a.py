import os
import sys
import platform
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import numpy as np
from PIL import Image
import pyqtgraph as pg
from .datatype.retdata import *

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
	super(MainWindow, self).__init__(parent)
	self.retdata = Retdata()  
   


