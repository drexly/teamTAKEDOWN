# -*- coding: utf-8 -*-
#
# 
# System name : RUDA (Real-time UAV Sound Detection and Analysis System)
# Created by: Team TAKEDOWN
# Team Members : Juhyun Kim, Cheonbok Park, Jinwoo Ahn, Youlim Ko, Junghyun Park
# helped by: John C. Gallagher, Eric T. Matson
#
#
# *** RUDA paper was accepted by 2017 IEEE Sensors Application Symposium (SAS). ***
#
# ** Any Revision or Copy of this code should be notified to the creators. **

import datetime
import os
import struct
import threading
import operator
import pyaudio
import numpy as np
import shutil
import matplotlib
import cv2
import scipy
import socket
import scipy.fftpack
import scipy.io.wavfile
import scipy.stats
import xlwt
import xlrd
import time
import matplotlib.pyplot as plt
np.set_printoptions(threshold=np.nan)
import matplotlib.ticker as mtick
matplotlib.use("TkAgg")
from matplotlib import figure
from PyQt4 import QtCore, QtGui
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from skimage.measure import compare_ssim as ssim

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8


    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

if not os.path.exists("./O"):
    os.makedirs("./O")
if not os.path.exists("./X"):
    os.makedirs("./X")
if not os.path.exists("./ML"):
    os.makedirs("./ML")

itemdatalist=[]
sock=None

dgr=0
clstatus="ONLINE"
generalresult="ANALYZE-READY"
mlresult="PENDING"
dapstat=0

class destIPdiag(QtGui.QDialog):
    def __init__(self, parent=None):
        super(destIPdiag, self).__init__(parent)
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)
        self.setWindowTitle("Connect to Server")
        self.addr = QtGui.QLineEdit(self)
        self.portdgr=str(dgr+6000)
        self.addr.setText("192.168..:"+self.portdgr)
        self.addr.setCursorPosition(8)
        self.conbtn=QtGui.QPushButton(self)
        self.conbtn.setText("Connect")
        self.conbtn.clicked.connect(self.conbtnwork)
        self.twowdglayout=QtGui.QHBoxLayout(self)
        self.twowdglayout.addWidget(self.addr)
        self.twowdglayout.addWidget(self.conbtn)

    def conbtnwork(self):
        global sock
        global dgr
        global clstatus
        global generalresult
        global mlresult
        global dapstat
        self.setWindowTitle("Connecting")
        self.conbtn.setText("Don't Click")
        self.conbtn.setDisabled(True)
        dst=str(self.addr.text()).split(":")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((dst[0], int(dst[1])))
        data='#'+str(dgr)+'#$'+str(dapstat)+'$^'+str(generalresult)+'^&'+str(clstatus)+'&*'+str(mlresult)+'*'
        #data = (str(dgr)+'|0|GeneralResult\nINITIALIZED|ClientStatus\nINITIALIZED|MachineLearntResult\nINITIALIZED|')
        sock.sendall(data)
        if sock.recv(99999) is not None:
            self.conbtn.setText('Port CONNECTED: '+self.portdgr)
            self.conbtn.setEnabled(True)
            threading.Thread(target=self.conn).start()
            self.setWindowTitle("Server Connected. CLOSE THIS WINDOW")
            ui.statusbar.showMessage("Server Connected")
        else:
            self.conbtn.setText('Not CONNECTED: ' + self.portdgr)
            self.setWindowTitle("CLOSE THIS WINDOW & DO AGAIN")
            self.addr.setEnabled(False)
            ui.statusbar.showMessage("Not CONNECTED! ReConnect!")
        ipaddress.close()

    def conn(self):
        global sock
        global dgr
        global clstatus
        global generalresult
        global mlresult
        global dapstat
        while True:
            data = '#' + str(dgr) + '#$' + str(dapstat) + '$^' + str(generalresult) + '^&' + str(clstatus) + '&*' + str(
                mlresult) + '*'
            #print data
            time.sleep(0.1)
            sock.sendall(data)

class Ui_MainWindow(object):
    # plot visualization variables
    present = None
    timer = None
    buffer = 16384
    linecolor = "green"
    # setting for pyaudio
    rate = 44100
    p = pyaudio.PyAudio()
    chunks = []
    detectChunks=[]
    inStream = None
    recThread = None
    addThread = None
    pltThread=None

    xlimit = 10000
    ylimit = 1000000

    savename=None
    displayTime = None
    data = None
    capFlag = 0
    mlFlag=2


    fth=True
    sth=False
    tth=False

    dapper=[0.00,0.00,0.00]
    avgper=0.00

    ndapper = [0.00,0.00,0.00]
    navgper = 0.00

    x1r = 0
    y1r =0
    llbnd1 =0
    rrbnd1 = 0
    tth1 = 0

    x2r = 0
    y2r = 0
    llbnd2 =0
    rrbnd2 = 0
    tth2 = 0

    x3r = 0
    y3r = 0
    llbnd3 =0
    rrbnd3 =0
    tth3 = 0

    detectFlag=False

    cntPD=0
    cntNonPD=0

    regx=[]
    regy=[]
    #    namePre=None
 #   ratePre=None
  #  spectrumPre=None
   # freqPre=None
    #nsamPre=None

#
    def stream(self):
        while True:
            if self.inStream is not None:
                self.chunks.append(self.inStream.read(self.buffer))

    def record(self):
        self.inStream = self.p.open(format=pyaudio.paInt16, channels=1,
                                    rate=self.rate, input=True, frames_per_buffer=self.buffer)
        self.addThread = threading.Thread(target=self.stream)
        self.addThread.start()

    # a figure instance to plot on
    figure = None
    # this is the Canvas Widget that displays the `figure`
    canvas = None
    # this is the Navigation widget
    # it takes the Canvas widget and a parent
    toolbar = None

    def setupUi(self, MainWindow):
        screen_resolution = app.desktop().screenGeometry()
        width, height = screen_resolution.width(), screen_resolution.height()
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(width / 1.5, height / 1.5)
        MainWindow.setStyleSheet("QMainWindow {background: '#fafafa';}")
        #        MainWindow.setMinimumSize(QtCore.QSize(1024, 768))
        #        MainWindow.setMaximumSize(QtCore.QSize(width / 1.5, height / 1.5))

        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))

        # self.plotlayout = QtGui.QVBoxLayout(self.centralwidget)
        self.gridlayout = QtGui.QGridLayout(self.centralwidget)

        # a figure instance to plot on
        self.figure = plt.figure()
        # this is the Canvas Widget that displays the `figure`
        self.canvas = FigureCanvas(self.figure)
        cid = self.canvas.mpl_connect('button_press_event', self.plotClick)
        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self.centralwidget)

        self.savexls = QtGui.QPushButton(self.canvas)
        self.savexls.setObjectName(_fromUtf8("savexls"))
        self.savexls.clicked.connect(self.xlswrite)

        self.clrqueue = QtGui.QPushButton(self.canvas)
        self.clrqueue.setObjectName(_fromUtf8("clearqueue"))
        self.clrqueue.clicked.connect(self.queueclear)

        self.thmillisec = QtGui.QSpinBox(self.canvas)
        self.thmillisec.setRange(0, 20000)
        self.thmillisec.setValue(1000)
        self.thmillisec.setObjectName(_fromUtf8("thresholdmillisec"))

        self.inGridlayout = QtGui.QGridLayout()
        self.inBoxlayout = QtGui.QHBoxLayout()

        # inGridlayout has toolbar, button, ...etc
        # inBoxlayout has button6, button5, button4
        #        self.gridLayout.addWidget(self.toolbar)
        self.gridlayout.addWidget(self.toolbar, 0, 0)
        self.gridlayout.addWidget(self.thmillisec, 0, 1)
        self.gridlayout.addWidget(self.savexls, 0, 2)
        self.gridlayout.addWidget(self.clrqueue, 0, 3)
        self.gridlayout.addWidget(self.canvas, 1, 0)
        self.gridlayout.addLayout(self.inGridlayout, 3, 0)
        self.gridlayout.addLayout(self.inBoxlayout, 2, 0)
        # self.inBoxlayout.addWidget(self.toolbar,0)
        self.gridlayout.setObjectName(_fromUtf8("griddisplay"))
        # self.centralwidget.setLayout(self.plotlayout)

        #color_black
        palettegl = QtGui.QPalette()
        palettegl.setBrush(QtGui.QPalette.Light, QtCore.Qt.black)
        # color_red
        paletteRed = QtGui.QPalette()
        paletteRed.setBrush(QtGui.QPalette.Light, QtCore.Qt.red)
        # color_blue
        paletteBlue = QtGui.QPalette()
        paletteBlue.setBrush(QtGui.QPalette.Light, QtCore.Qt.blue)
        # color_navy
        paletteNavy = QtGui.QPalette()
        paletteNavy.setBrush(QtGui.QPalette.Light, QtCore.Qt.darkBlue)
        # color_green
        paletteGreen = QtGui.QPalette()
        paletteGreen.setBrush(QtGui.QPalette.Light, QtCore.Qt.darkGray)

        self.lineEdit = QtGui.QListWidget(self.centralwidget)
        # self.lineEdit.setGeometry(QtCore.QRect(10, 475, 800, 105))
        self.gridlayout.addWidget(self.lineEdit, 1, 1, 3, 4)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.lineEdit.itemDoubleClicked.connect(self.plotitem)

        self.qlabeldap = QtGui.QLabel(self.centralwidget)
        self.qlabeldap.setText("Realtime Threshold Detect Drone's Appearance Percentage")
        self.inGridlayout.addWidget(self.qlabeldap, 1, 0, 1, 1)

        self.leftBoundary_1 = QtGui.QPushButton(self.centralwidget)
        self.leftBoundary_1.setGeometry(QtCore.QRect(340, 668, 91, 38))
        self.leftBoundary_1.setObjectName(_fromUtf8("leftBoundary_1"))
        self.leftBoundary_1.clicked.connect(self.lbnd1f)
        self.leftBoundary_1.setStyleSheet("background-color:#b2dfdb")
        #        self.leftBoundary_1.setPalette(palettegl)
        #        self.leftBoundary_1.display("00:00")
        self.inGridlayout.addWidget(self.leftBoundary_1, 1, 1, 1, 1)

        self.rightBoundary_1 = QtGui.QPushButton(self.centralwidget)
        self.rightBoundary_1.setGeometry(QtCore.QRect(340, 668, 91, 38))
        self.rightBoundary_1.setObjectName(_fromUtf8("rightBoundary_1"))
        self.rightBoundary_1.clicked.connect(self.rbnd1f)
        self.rightBoundary_1.setStyleSheet("background-color:#80cbc4")
        #        self.rightBoundary_1.setPalette(palettegl)
        #        self.rightBoundary_1.display("00:00")
        self.inGridlayout.addWidget(self.rightBoundary_1, 1, 2, 1, 1)

        self.threshold_1 = QtGui.QPushButton(self.centralwidget)
        self.threshold_1.setGeometry(QtCore.QRect(340, 668, 91, 38))
        self.threshold_1.setObjectName(_fromUtf8("threshold_1"))
        self.threshold_1.clicked.connect(self.th1f)
        self.threshold_1.setStyleSheet("background-color:#4db6ac")
        #        self.threshold_1.setPalette(palettegl)
        #        self.threshold_1.display("00:00")
        self.inGridlayout.addWidget(self.threshold_1, 1, 3, 1, 1)

        #        self.qLabelChunk1 = QtGui.QLabel(self.centralwidget)
        #        self.qLabelChunk1.setText("labelChunk1")
        #        self.inGridlayout.addWidget(self.qLabelChunk1,2,0,1,1)

        self.Dapp = QtGui.QLCDNumber(self.centralwidget)
        self.Dapp.setGeometry(QtCore.QRect(340, 668, 91, 38))
        self.Dapp.setObjectName(_fromUtf8("Dapp"))
        self.Dapp.setPalette(paletteRed)
        self.Dapp.display("00.00")
        self.inGridlayout.addWidget(self.Dapp, 2, 0, 1, 1)

        self.lbnd1 = QtGui.QSpinBox(self.centralwidget)
        self.lbnd1.setRange(0, 20000)
        self.lbnd1.setValue(1000)
        self.lbnd1.setGeometry(QtCore.QRect(740, 668, 55, 38))
        self.lbnd1.setObjectName(_fromUtf8("lbnd1size"))
        self.inGridlayout.addWidget(self.lbnd1, 2, 1, 1, 1)


        self.rbnd1 = QtGui.QSpinBox(self.centralwidget)
        self.rbnd1.setRange(0, 20000)
        self.rbnd1.setValue(2500)
        self.rbnd1.setGeometry(QtCore.QRect(740, 668, 55, 38))
        self.rbnd1.setObjectName(_fromUtf8("rbnd1size"))
        self.inGridlayout.addWidget(self.rbnd1, 2, 2, 1, 1)

        self.th1 = QtGui.QSpinBox(self.centralwidget)
        self.th1.setRange(200000, 100000000)
        self.th1.setValue(200000)
        self.th1.setGeometry(QtCore.QRect(740, 668, 55, 38))
        self.th1.setObjectName(_fromUtf8("th1size"))
        self.inGridlayout.addWidget(self.th1, 2, 3, 1, 1)

        self.qLabelLCD2 = QtGui.QLabel(self.centralwidget)
        self.qLabelLCD2.setText("Machine Learnt simmilarity between 'O'groups/'X'groups")
        self.inGridlayout.addWidget(self.qLabelLCD2, 3, 0, 1, 1)

        self.leftBoundary_2 = QtGui.QPushButton(self.centralwidget)
        self.leftBoundary_2.setGeometry(QtCore.QRect(340, 668, 91, 38))
        self.leftBoundary_2.setObjectName(_fromUtf8("leftBoundary_2"))
        self.leftBoundary_2.clicked.connect(self.lbnd2f)
        self.leftBoundary_2.setStyleSheet("background-color:#b2dfdb")
        #        self.leftBoundary_2.setPalette(palettegl)
        #        self.leftBoundary_2.display("00:00")
        self.inGridlayout.addWidget(self.leftBoundary_2, 3, 1, 1, 1)

        self.rightBoundary_2 = QtGui.QPushButton(self.centralwidget)
        self.rightBoundary_2.setGeometry(QtCore.QRect(340, 668, 91, 38))
        self.rightBoundary_2.setObjectName(_fromUtf8("rightBoundary_2"))
        self.rightBoundary_2.clicked.connect(self.rbnd2f)
        self.rightBoundary_2.setStyleSheet("background-color:#80cbc4")
        #        self.rightBoundary_2.setPalette(palettegl)
        #        self.rightBoundary_2.display("00:00")
        self.inGridlayout.addWidget(self.rightBoundary_2, 3, 2, 1, 1)

        self.threshold_2 = QtGui.QPushButton(self.centralwidget)
        self.threshold_2.setGeometry(QtCore.QRect(340, 668, 91, 38))
        self.threshold_2.setObjectName(_fromUtf8("threshold_2"))
        self.threshold_2.clicked.connect(self.th2f)
        self.threshold_2.setStyleSheet("background-color:#4db6ac")
        #        self.threshold_2.setPalette(palettegl)
        #        self.threshold_2.display("00:00")
        self.inGridlayout.addWidget(self.threshold_2, 3, 3, 1, 1)

        #        self.qLabelChunk2 = QtGui.QLabel(self.centralwidget)
        #        self.qLabelChunk2.setText("labelChunk2")
        #        self.inGridlayout.addWidget(self.qLabelChunk2,4,0,1,1)

        self.nDapp = QtGui.QLCDNumber(self.centralwidget)
        self.nDapp.setGeometry(QtCore.QRect(340, 668, 91, 38))
        self.nDapp.setObjectName(_fromUtf8("nDapp"))
        self.nDapp.setPalette(paletteGreen)
        self.nDapp.display("00:00")
        self.inGridlayout.addWidget(self.nDapp, 4, 0, 1, 1)

        self.lbnd2 = QtGui.QSpinBox(self.centralwidget)
        self.lbnd2.setRange(0, 20000)
        self.lbnd2.setValue(2500)
        self.lbnd2.setGeometry(QtCore.QRect(740, 668, 55, 38))
        self.lbnd2.setObjectName(_fromUtf8("lbnd2size"))
        self.inGridlayout.addWidget(self.lbnd2, 4, 1, 1, 1)
        self.lbnd2.setEnabled(False)


        self.rbnd2 = QtGui.QSpinBox(self.centralwidget)
        self.rbnd2.setRange(0, 20000)
        self.rbnd2.setValue(6000)
        self.rbnd2.setGeometry(QtCore.QRect(740, 668, 55, 38))
        self.rbnd2.setObjectName(_fromUtf8("rbnd2size"))
        self.inGridlayout.addWidget(self.rbnd2, 4, 2, 1, 1)
        self.rbnd2.setEnabled(False)


        self.th2 = QtGui.QSpinBox(self.centralwidget)
        self.th2.setRange(200000, 100000000)
        self.th2.setValue(200000)
        self.th2.setGeometry(QtCore.QRect(740, 668, 55, 38))
        self.th2.setObjectName(_fromUtf8("th2size"))
        self.inGridlayout.addWidget(self.th2, 4, 3, 1, 1)
        self.th2.setEnabled(False)

        self.qLabelLCD3 = QtGui.QLabel(self.centralwidget)
        self.qLabelLCD3.setText("Appearance of Drone/Non-Drone Detection item Count")
        self.inGridlayout.addWidget(self.qLabelLCD3, 5, 0, 1, 1)

        self.leftBoundary_3 = QtGui.QPushButton(self.centralwidget)
        self.leftBoundary_3.setGeometry(QtCore.QRect(340, 668, 91, 38))
        self.leftBoundary_3.setObjectName(_fromUtf8("leftBoundary_3"))
        self.leftBoundary_3.clicked.connect(self.lbnd3f)
        self.leftBoundary_3.setStyleSheet("background-color:#b2dfdb")
        #        self.leftBoundary_3.setPalette(palettegl)
        #        self.leftBoundary_3.display("00:00")
        self.inGridlayout.addWidget(self.leftBoundary_3, 5, 1, 1, 1)

        self.rightBoundary_3 = QtGui.QPushButton(self.centralwidget)
        self.rightBoundary_3.setGeometry(QtCore.QRect(340, 668, 91, 38))
        self.rightBoundary_3.setObjectName(_fromUtf8("rightBoundary_3"))
        self.rightBoundary_3.clicked.connect(self.rbnd3f)
        self.rightBoundary_3.setStyleSheet("background-color:#80cbc4")
        #        self.lcdNumber3_2.setPalette(palettegl)
        #        self.lcdNumber3_2.display("00:00")
        self.inGridlayout.addWidget(self.rightBoundary_3, 5, 2, 1, 1)

        self.threshold_3 = QtGui.QPushButton(self.centralwidget)
        self.threshold_3.setGeometry(QtCore.QRect(340, 668, 91, 38))
        self.threshold_3.setObjectName(_fromUtf8("threshold_3"))
        self.threshold_3.clicked.connect(self.th3f)
        self.threshold_3.setStyleSheet("background-color:#4db6ac")
        #        self.threshold_3.setPalette(palettegl)
        #        self.threshold_3.display("00:00")
        self.inGridlayout.addWidget(self.threshold_3, 5, 3, 1, 1)

        #        self.qLabelChunk3 = QtGui.QLabel(self.centralwidget)
        #        self.qLabelChunk3.setText("labelChunk3")
        #        self.inGridlayout.addWidget(self.qLabelChunk3, 6, 0, 1, 1)

        self.CntLcd = QtGui.QLCDNumber(self.centralwidget)
        self.CntLcd.setGeometry(QtCore.QRect(340, 668, 91, 38))
        self.CntLcd.setObjectName(_fromUtf8("CntLcd"))
        self.CntLcd.setPalette(palettegl)
        self.CntLcd.display("00:00")
        self.inGridlayout.addWidget(self.CntLcd, 6, 0, 1, 1)

        self.lbnd3 = QtGui.QSpinBox(self.centralwidget)
        self.lbnd3.setRange(0, 20000)
        self.lbnd3.setValue(6000)
        self.lbnd3.setGeometry(QtCore.QRect(740, 668, 55, 38))
        self.lbnd3.setObjectName(_fromUtf8("lbnd3size"))
        self.inGridlayout.addWidget(self.lbnd3, 6, 1, 1, 1)
        self.lbnd3.setEnabled(False)


        self.rbnd3 = QtGui.QSpinBox(self.centralwidget)
        self.rbnd3.setRange(0, 20000)
        self.rbnd3.setValue(9000)
        self.rbnd3.setGeometry(QtCore.QRect(740, 668, 55, 38))
        self.rbnd3.setObjectName(_fromUtf8("rbnd3size"))
        self.inGridlayout.addWidget(self.rbnd3, 6, 2, 1, 1)
        self.rbnd3.setEnabled(False)

        self.th3 = QtGui.QSpinBox(self.centralwidget)
        self.th3.setRange(200000,100000000)
        self.th3.setValue(200000)
        self.th3.setGeometry(QtCore.QRect(740, 668, 55, 38))
        self.th3.setObjectName(_fromUtf8("th3size"))
        self.inGridlayout.addWidget(self.th3, 6, 3, 1, 1)
        self.th3.setEnabled(False)

        self.lcdNumber = QtGui.QLCDNumber(self.centralwidget)
        self.lcdNumber.setGeometry(QtCore.QRect(340, 668, 91, 38))
        self.lcdNumber.setObjectName(_fromUtf8("lcdNumber"))
        self.lcdNumber.setPalette(palettegl)
        self.lcdNumber.display("00:00")
        self.inBoxlayout.addWidget(self.lcdNumber, 1)

        self.analyzeButton = QtGui.QPushButton(self.centralwidget)
        self.analyzeButton.setGeometry(QtCore.QRect(440, 668, 91, 38))
        self.analyzeButton.setObjectName(_fromUtf8("analyzeButton"))
        self.analyzeButton.clicked.connect(self.start)
        self.analyzeButton.setStyleSheet("background-color:#26a69a; color:white")
        self.inBoxlayout.addWidget(self.analyzeButton, 2)
        self.analyzeButton.connect(QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_F1), self.centralwidget),
                                   QtCore.SIGNAL('activated()'), self.start)
        #     self.inGridlayout.addWidget(self.analyzeButton)


        self.stopButton = QtGui.QPushButton(self.centralwidget)
        self.stopButton.setGeometry(QtCore.QRect(540, 668, 91, 38))
        self.stopButton.setObjectName(_fromUtf8("stopButton"))
        self.stopButton.clicked.connect(self.stop)
        self.stopButton.setStyleSheet("background-color:#26a69a; color:white")
        self.inBoxlayout.addWidget(self.stopButton, 3)
        self.stopButton.connect(QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_F2), self.centralwidget),
                                QtCore.SIGNAL('activated()'), self.stop)
        #      self.inGridlayout.addWidget(self.stopButton)

        self.recordButton = QtGui.QPushButton(self.centralwidget)
        self.recordButton.setGeometry(QtCore.QRect(640, 668, 91, 38))
        self.recordButton.setObjectName(_fromUtf8("recordButton"))
        self.recordButton.clicked.connect(self.save)
        self.recordButton.setStyleSheet("background-color:#26a69a; color:white")
        self.inBoxlayout.addWidget(self.recordButton, 4)
        self.recordButton.connect(QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_F3), self.centralwidget),
                                  QtCore.SIGNAL('activated()'), self.save)

        self.chunksize = QtGui.QSpinBox(self.centralwidget)
        self.chunksize.setRange(10, 17)
        self.chunksize.setValue(14)
        self.chunksize.setGeometry(QtCore.QRect(740, 668, 55, 38))
        self.chunksize.setObjectName(_fromUtf8("chunksize"))
        self.inBoxlayout.addWidget(self.chunksize, 5)
        self.chunksize.valueChanged.connect(self.intchanged)

        #       self.inGridlayout.addWidget(self.recordButton)
        self.horizontalSlider = QtGui.QSlider(self.centralwidget)
        self.horizontalSlider.setRange(200, 20000)
        self.horizontalSlider.setValue(10000)
        self.horizontalSlider.valueChanged.connect(self.hsvhandler)
        self.horizontalSlider.setGeometry(QtCore.QRect(800, 668, 71, 38))
        self.inBoxlayout.addWidget(self.horizontalSlider, 6)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName(_fromUtf8("horizontalSlider"))
        #    self.inGridlayout.addWidget(self.horizontalSlider)

        self.verticallSlider = QtGui.QSlider(self.centralwidget)
        self.verticallSlider.setRange(1000000, 100000000)
        self.verticallSlider.setValue(1000000)
        self.verticallSlider.valueChanged.connect(self.vsvhandler)
        self.verticallSlider.setGeometry(QtCore.QRect(880, 668, 71, 38))
        self.verticallSlider.setOrientation(QtCore.Qt.Vertical)
        self.inBoxlayout.addWidget(self.verticallSlider, 7)
        self.verticallSlider.setObjectName(_fromUtf8("verticalSlider"))
        #  self.inGridlayout.addWidget(self.verticallSlider, 7, 0, 7, 2)
        #   self.inGridlayout.addWidget(self.verticallSlider)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1024, 26))
        self.menubar.setObjectName(_fromUtf8("menubar"))

        self.menuML = QtGui.QMenu(self.menubar)
        self.menuML.setObjectName(_fromUtf8("menuML"))

        self.menuCapture = QtGui.QMenu(self.menubar)
        self.menuCapture.setObjectName(_fromUtf8("menuCapture"))

        self.menuThreshold = QtGui.QMenu(self.menubar)
        self.menuThreshold.setObjectName(_fromUtf8("menuThreshold"))

        self.menuConnection = QtGui.QMenu(self.menubar)
        self.menuConnection.setObjectName(_fromUtf8("menuConnection"))

        self.menuRegress = QtGui.QMenu(self.menubar)
        self.menuRegress.setObjectName(_fromUtf8("menuRegress"))

        self.menuSVM = QtGui.QMenu(self.menubar)
        self.menuSVM.setObjectName(_fromUtf8("menuSVM"))

        self.menuDegree = QtGui.QMenu(self.menubar)
        self.menuDegree.setObjectName(_fromUtf8("menuDegree"))

        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName(_fromUtf8("menuHelp"))

        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))

        MainWindow.setStatusBar(self.statusbar)


        agML = QtGui.QActionGroup(MainWindow, exclusive=True)
        self.autopilot = agML.addAction(QtGui.QAction(MainWindow, checkable=True))
        self.autopilot.triggered.connect(self.automode)
        self.autopilot.setObjectName(_fromUtf8("autopilot"))

        self.supervise = agML.addAction(QtGui.QAction(MainWindow, checkable=True))
        self.supervise.triggered.connect(self.manualmode)
        self.supervise.setObjectName(_fromUtf8("supervise"))

        self.thonly = agML.addAction(QtGui.QAction(MainWindow, checkable=True))
        self.thonly.triggered.connect(self.thmode)
        self.thonly.setObjectName(_fromUtf8("thonly"))
        self.thonly.setChecked(True)


        self.menuML.addAction(self.autopilot)
        self.menuML.addAction(self.supervise)
        self.menuML.addAction(self.thonly)

        self.menubar.addAction(self.menuML.menuAction())

        agTh = QtGui.QActionGroup(MainWindow, exclusive=False)

        self.fir = agTh.addAction(QtGui.QAction(MainWindow, checkable=True))
        self.fir.setChecked(True)
        self.fir.setObjectName(_fromUtf8("First"))
        self.fir.triggered.connect(self.chkfir)


        self.sec = agTh.addAction(QtGui.QAction(MainWindow, checkable=True))
        self.sec.setObjectName(_fromUtf8("Second"))
        self.sec.triggered.connect(self.chksec)

        self.thi = agTh.addAction(QtGui.QAction(MainWindow, checkable=True))
        self.thi.setObjectName(_fromUtf8("Third"))
        self.thi.triggered.connect(self.chkthi)

        self.legend=agTh.addAction(QtGui.QAction(MainWindow, checkable=True))
        self.legend.setObjectName(_fromUtf8("legend"))

        self.menuThreshold.addAction(self.fir)
        self.menuThreshold.addAction(self.sec)
        self.menuThreshold.addAction(self.thi)
        self.menuThreshold.addSeparator()
        self.menuThreshold.addAction(self.legend)

        self.menubar.addAction(self.menuThreshold.menuAction())

        agRegress = QtGui.QActionGroup(MainWindow,exclusive=False)

        self.regressDap= agRegress.addAction(QtGui.QAction(MainWindow,checkable=False))
        self.regressDap.triggered.connect(self.regasync)
        #self.regressDap.setChecked(True)
        self.regressDap.setObjectName(_fromUtf8("rgrsplotDap"))

        #self.regressNDap = agRegress.addAction(QtGui.QAction(MainWindow,checkable=True))
        #self.regressNDap.setObjectName(_fromUtf8("rgrsplotNDap"))

        self.menuRegress.addAction(self.regressDap)
        #self.menuRegress.addAction(self.regressNDap)

        self.menubar.addAction(self.menuRegress.menuAction())

        agConn = QtGui.QActionGroup(MainWindow, exclusive=True)

        self.con = agConn.addAction(QtGui.QAction(MainWindow, checkable=True))
        self.con.triggered.connect(self.destinate)
        self.con.setObjectName(_fromUtf8("Connect"))

        #elf.discon = agConn.addAction(QtGui.QAction(MainWindow))
        #self.discon.setChecked(True)
        #self.discon.setObjectName(_fromUtf8("Disconnect"))

        self.menuConnection.addAction(self.con)
        #self.menuConnection.addAction(self.discon)
        self.menubar.addAction(self.menuConnection.menuAction())

        agCapture = QtGui.QActionGroup(MainWindow, exclusive=True)
        self.scr = agCapture.addAction(QtGui.QAction(MainWindow, checkable=True))
        self.scr.setChecked(True)
        self.scr.triggered.connect(self.scrmode)
        self.scr.setObjectName(_fromUtf8("scrOnly"))

        self.rec = agCapture.addAction(QtGui.QAction(MainWindow, checkable=True))
        self.rec.triggered.connect(self.recmode)
        self.rec.setObjectName(_fromUtf8("recOnly"))

        self.scrnrec = agCapture.addAction(QtGui.QAction(MainWindow, checkable=True))
        self.scrnrec.triggered.connect(self.scrnrecmode)
        self.scrnrec.setObjectName(_fromUtf8("scrNrec"))

        self.menuCapture.addAction(self.scr)
        self.menuCapture.addAction(self.rec)
        self.menuCapture.addAction(self.scrnrec)

        self.menubar.addAction(self.menuCapture.menuAction())

        # SVM Menu
        agSVM = QtGui.QActionGroup(MainWindow, exclusive=False)

        self.fSVM = agSVM.addAction(QtGui.QAction(MainWindow, checkable=True))
        self.fSVM.setChecked(True)
        self.fSVM.setObjectName(_fromUtf8("fSVM"))

        self.sSVM = agSVM.addAction(QtGui.QAction(MainWindow, checkable=True))
        self.sSVM.setObjectName(_fromUtf8("sSVM"))

        self.menuSVM.addAction(self.fSVM)
        self.menuSVM.addAction(self.sSVM)

        self.menubar.addAction(self.menuSVM.menuAction())

        agObject = QtGui.QActionGroup(MainWindow, exclusive=True)
        self.zero = agObject.addAction(QtGui.QAction(MainWindow, checkable=True))
        self.zero.setChecked(True)
        self.zero.triggered.connect(self.degree)
        self.zero.setObjectName(_fromUtf8("zero"))

        self.sixty = agObject.addAction(QtGui.QAction(MainWindow, checkable=True))
        self.sixty.triggered.connect(self.degree)
        self.sixty.setObjectName(_fromUtf8("sixty"))

        self.d120 = agObject.addAction(QtGui.QAction(MainWindow, checkable=True))
        self.d120.triggered.connect(self.degree)
        self.d120.setObjectName(_fromUtf8("d120"))

        self.d180 = agObject.addAction(QtGui.QAction(MainWindow, checkable=True))
        self.d180.triggered.connect(self.degree)
        self.d180.setObjectName(_fromUtf8("d180"))

        self.d240 = agObject.addAction(QtGui.QAction(MainWindow, checkable=True))
        self.d240.triggered.connect(self.degree)
        self.d240.setObjectName(_fromUtf8("d240"))

        self.d300 = agObject.addAction(QtGui.QAction(MainWindow, checkable=True))
        self.d300.triggered.connect(self.degree)
        self.d300.setObjectName(_fromUtf8("d300"))

        self.menuDegree.addAction(self.zero)
        self.menuDegree.addAction(self.sixty)
        self.menuDegree.addAction(self.d120)
        self.menuDegree.addAction(self.d180)
        self.menuDegree.addAction(self.d240)
        self.menuDegree.addAction(self.d300)
        self.menubar.addAction(self.menuDegree.menuAction())

        # Help Menu
        agHelp = QtGui.QActionGroup(MainWindow)

        self.dev = agHelp.addAction(QtGui.QAction(MainWindow))
        self.dev.setChecked(True)
        # self.dev.triggered.connect(self.help)
        self.dev.setObjectName(_fromUtf8("Developers"))

        self.about = agHelp.addAction(QtGui.QAction(MainWindow))
        self.about.setObjectName(_fromUtf8("About"))

        self.menuHelp.addAction(self.dev)
        self.menuHelp.addAction(self.about)

        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow",
                                             "United States Air Force Realtime Drone Air Defense System Client- Made by Team TAKEDOWN",
                                             None))
        self.recordButton.setText(_translate("MainWindow", "Record(F3)", None))
        self.stopButton.setText(_translate("MainWindow", "Stop(F2)", None))
        self.analyzeButton.setText(_translate("MainWindow", "Analyze(F1)", None))

        self.savexls.setText(_translate("MainWindow", "Save Stacked", None))
        self.clrqueue.setText(_translate("MainWindow", "Clear Stack", None))

        # leftBoundary_1 etc
        self.leftBoundary_1.setText(_translate("MainWindow", "1st Minimum Frequency", None))
        self.rightBoundary_1.setText(_translate("MainWindow", "1st Maximum Frequency", None))
        self.threshold_1.setText(_translate("MainWindow", "1st Threshold", None))
        self.leftBoundary_2.setText(_translate("MainWindow", "2nd Minimum Frequency", None))
        self.rightBoundary_2.setText(_translate("MainWindow", "2nd Maximum Frequency", None))
        self.threshold_2.setText(_translate("MainWindow", "2nd Threshold", None))
        self.leftBoundary_3.setText(_translate("MainWindow", "3rd Minimum Frequency", None))
        self.rightBoundary_3.setText(_translate("MainWindow", "3rd Maximum Frequency", None))
        self.threshold_3.setText(_translate("MainWindow", "3rd Threshold", None))

        self.menuML.setTitle(_translate("MainWindow", "Machine Learning", None))
        self.autopilot.setText(_translate("MainWindow", "Self Learn", None))
        self.supervise.setText(_translate("MainWindow", "Validation", None))
        self.thonly.setText(_translate("MainWindow", "Deactivate", None))

        self.menuCapture.setTitle(_translate("MainWindow", "Record", None))
        self.scr.setText(_translate("MainWindow", "Plot.png Only", None))
        self.rec.setText(_translate("MainWindow", "Record.wav Only", None))
        self.scrnrec.setText(_translate("MainWindow", "Plot.png+Record.wav", None))

        self.menuThreshold.setTitle(_translate("MainWindow", "Threshold", None))
        self.fir.setText(_translate("MainWindow", "First", None))
        self.sec.setText(_translate("MainWindow", "Second", None))
        self.thi.setText(_translate("MainWindow", "Third", None))
        self.legend.setText(_translate("MainWindow", "Legend", None))

        self.menuConnection.setTitle(_translate("MainWindow", "Connection", None))
        self.con.setText(_translate("MainWindow", "Connect", None))
        #self.discon.setText(_translate("MainWindow", "Disconnect", None))
        #
        self.menuRegress.setTitle(_translate("MainWindow", "Regression", None))
        self.regressDap.setText(_translate("MainWindow", "Linear Plot DAP", None))
        #self.regressNDap.setText(_translate("MainWindow", "Linear Plot Non DAP", None))
        #SVM
        self.menuSVM.setTitle(_translate("MainWindow", "PIL&&KNN", None))
        self.fSVM.setText(_translate("MainWindow", "PIL", None))
        self.sSVM.setText(_translate("MainWindow", "KNN", None))

        self.menuDegree.setTitle(_translate("MainWindow", "Degree", None))
        self.zero.setText(_translate("MainWindow", "0º", None))
        self.sixty.setText(_translate("MainWindow", "60º", None))
        self.d120.setText(_translate("MainWindow", "120º", None))
        self.d180.setText(_translate("MainWindow", "180º", None))
        self.d240.setText(_translate("MainWindow", "240º", None))
        self.d300.setText(_translate("MainWindow", "300º", None))

        self.menuHelp.setTitle(_translate("MainWindow", "Help", None))
        self.dev.setText(_translate("MainWindow", "Developers", None))
        self.about.setText(_translate("MainWindow", "About", None))

    def tick(self):
        global dgr
        global clstatus
        global generalresult
        global mlresult
        global dapstat
        now = datetime.datetime.now()
        minutes, seconds = divmod((now - self.present).total_seconds(), 60)
        self.displayTime = QtCore.QTime(0, minutes, round(seconds))
        self.lcdNumber.display(self.displayTime.toString('mm:ss'))
        #To server
        clstatus="ONLINE-"+str(self.displayTime.toString('mm:ss'))+"\nCollected Drone:"+str(self.cntPD)+"\nCollected Non-Drone:"+str(self.cntNonPD)
        if len(self.chunks) > 0:
            X = self.chunks.pop(0)
            self.data = scipy.array(struct.unpack("%dB" % (self.buffer * 2), X))

            # print "RECORDED",len(self.data)/float(self.rate),"SEC"
            # ffty = scipy.fftpack.fft(self.data)
            # fftx = scipy.fftpack.rfftfreq(self.buffer * 2, 1.0 / self.rate)

            spectrum = scipy.fftpack.fft(self.data)
            freq = scipy.fftpack.fftfreq(len(self.data), d=0.5 / self.rate)
            #if self.mlFlag is 0:
            ax2 = self.figure.add_subplot(111)

            if self.legend.isChecked():
                ax2.plot(self.llbnd1, self.y1r, 'r', self.rrbnd1, self.y1r, 'r', self.x1r, self.tth1, 'r', self.llbnd2, self.y2r, 'g', self.rrbnd2, self.y2r, 'g', self.x2r, self.tth2, 'g', self.llbnd3, self.y3r,'b', self.rrbnd3, self.y3r, 'b', self.x3r, self.tth3, 'b', freq, abs(spectrum), 'k')
                plt.legend(['th1lbnd','th1rbnd','th1','th2lbnd','th2rbnd','th2','th3lbnd','th3rbnd','th3'], loc='upper right')
            else:
                ax2.plot(freq, abs(spectrum), 'k')

            if self.fir.isChecked():
                l1 = self.lbnd1.value() * self.buffer/self.rate
                r1 = self.rbnd1.value() * self.buffer/self.rate
                max1 = np.amax(abs(spectrum[l1:r1]))
                for index, xy in enumerate(zip(freq, abs(spectrum))):
                    if xy[1] == max1:
                        plt.annotate('(%s, %s)' % (int(xy[0]), int(xy[1])), xy=xy)
                        #if over threshold
                        if max1>=self.th1.value() and xy[0]>0:
                            temp=self.capFlag
                            self.capFlag=-1
                            self.save()
                            self.dapper[0]=(max1-self.th1.value())/self.th1.value()*100
                            self.capFlag = temp
                        #not over threshold
                        elif max1<self.th1.value() and xy[0]>0:
                            self.dapper[0] = 0.00


            if self.sec.isChecked():
                l2 = self.lbnd2.value() * self.buffer / self.rate
                r2 = self.rbnd2.value() * self.buffer / self.rate
                max2 = np.amax(abs(spectrum[l2:r2]))
                for index, xy in enumerate(zip(freq, abs(spectrum))):
                    if xy[1] == max2:
                        plt.annotate('(%s, %s)' % (int(xy[0]), int(xy[1])), xy=xy)
                        if max2>=self.th2.value() and xy[0]>0:
                            temp=self.capFlag
                            self.capFlag=-1
                            self.save()
                            # if not in Machine learning Stage
                            #self.lineEdit.append(u'드론모드 th2 검출:')
                            self.dapper[1]=(max2-self.th2.value())/self.th2.value()*100
                            self.capFlag = temp
                        #not over threshold
                        elif max2<self.th2.value() and xy[0]>0:
                            self.dapper[1] = 0.00

            if self.thi.isChecked():
                l3 = self.lbnd3.value() * self.buffer / self.rate
                r3 = self.rbnd3.value() * self.buffer / self.rate
                max3 = np.amax(abs(spectrum[l3:r3]))
                for index, xy in enumerate(zip(freq, abs(spectrum))):
                    if xy[1] == max3:
                        plt.annotate('(%s, %s)' % (int(xy[0]), int(xy[1])), xy=xy)
                        if max3 >= self.th3.value() and xy[0]>0:
                            temp=self.capFlag
                            self.capFlag=-1
                            self.save()
                            # if not in Machine learning Stage
                            self.dapper[2]=(max3-self.th3.value())/self.th3.value()*100
                            self.capFlag=temp
                    elif max3 < self.th3.value() and xy[0] > 0:
                        self.dapper[2] = 0.00

            self.calcdap()
            self.calcndap()

            # if not in Machine learning Stage
            #if in drone detection mode
            #if Dap Percent>0
            if self.Dapp.value()>0.00:
                #and currently not in detect-recording stage
                if self.detectFlag is False:
                    # set detection Flag in detect-recording stage
                    self.detectFlag=True
                    #print start recording
                self.detectChunks.append([self.data,self.avgper,freq,abs(spectrum),self.savename])
                mlresult="DETECTION ALERT!\nRECORD IN PROGRESS"
            #or either finished and not detected yet
            else:
                #if was in detecting stage end the append add the item result
                if self.detectFlag is True:
                    #print recording done
                    #chk if detec-recording stage chunks' length
                    if len(self.detectChunks)>0:
                        #find out it has lengthy chunk >= current millisecs detect threshold
                        reclengthsec=(len(self.detectChunks[0][0]) / (float(self.rate)*2))*len(self.detectChunks)
                        recpersum=0.00
                        if reclengthsec*1000>self.thmillisec.value():
                            mlresult = "RECORDED! MACHINE\nLEARNING NOW"
                            for elem in self.detectChunks:
                                recpersum+=elem[1]
                            #self.lineEdit.append("--------------------------------")
                            #self.lineEdit.append("Drone Found")
                            #self.lineEdit.append("Avg DAP Percent Report on Batch Process")
                            #self.lineEdit.append(str(recpersum/len(self.detectChunks))+"%")
                            #self.lineEdit.append("Whole Detected Chunks' Recorded Seconds")
                            #self.lineEdit.append(str(reclengthsec)+"(s)")
                            #self.lineEdit.append("Saved sample index/out of total recorded chunks' length")
                            #self.lineEdit.append(str(int(len(self.detectChunks) / 2))+"/"+str(len(self.detectChunks)))
                            #self.lineEdit.append("--------------------------------\n")

                            mid=self.detectChunks[int(len(self.detectChunks) / 2)]

                            l1 = self.lbnd1.value() * self.buffer / self.rate
                            r1 = self.rbnd1.value() * self.buffer / self.rate
                            l2 = self.lbnd2.value() * self.buffer / self.rate
                            r2 = self.rbnd2.value() * self.buffer / self.rate
                            l3 = self.lbnd3.value() * self.buffer / self.rate
                            r3 = self.rbnd3.value() * self.buffer / self.rate

                            max1 = np.amax(mid[3][l1:r1])
                            max2 = np.amax(mid[3][l2:r2])
                            max3 = np.amax(mid[3][l3:r3])

                            ranking=[]
                            ranking.append([self.lbnd1.value() ,self.rbnd1.value() ,max1])
                            ranking.append([self.lbnd2.value() ,self.rbnd2.value(),max2])
                            ranking.append([self.lbnd3.value() ,self.rbnd3.value(),max3])
                            result=sorted(ranking,key=operator.itemgetter(2),reverse=True)
                            x=result[0][0]
                            for index, xy in enumerate(zip(mid[2], mid[3])):
                                if int(xy[0])>=result[0][0] and int(xy[0])<=result[0][1]:
                                    if xy[1]==result[0][2]:
                                        x=xy[0]
                                        self.regx.append(xy[0])
                                        self.regy.append(xy[1])
                                        break
                            fg=plt.figure()
                            sav=fg.add_subplot(1,1,1)
                            sav.plot(mid[2],mid[3],'k')
                            sav.set_xlim(x-100, x+100)
                            sav.set_ylim(0, 1000000)
                            sav.fill(mid[2],mid[3],facecolor='black')
                            extent = sav.get_window_extent().transformed(fg.dpi_scale_trans.inverted())
                            fg.savefig("%s.png" % mid[4], bbox_inches=extent)
                            fg.savefig("%s.jpg" % mid[4], bbox_inches='tight')
                            if self.mlFlag==2:
                                self.cntPD+=1
                            self.CntLcd.display("%s:%s"%(str(self.cntPD),str(self.cntNonPD)))
                            self.itemadd(rtime=reclengthsec,percent=(recpersum / len(self.detectChunks)),chunk=mid)


                            # pop out the middle to add item stack
                            #plot(self.detectChunks[int(len(self.detectChunks) / 2)])
                        #clear chunks for further use
                        self.detectChunks=[]
                    #end recording
                    self.detectFlag=False

            #print np.alen(abs(spectrum))
            #print np.alen(freq)
            #for xy in zip(freq, abs(spectrum)):
             #   if maxamplitude == xy[1]:
              #      plt.annotate('(%s, %s)' % xy, xy=xy, textcoords='data')
            ax2.set_xlim(0, self.xlimit)
            ax2.set_ylim(0, self.ylimit)
            ax2.set_xlabel("frequency [Hz]")
            #ax2.fill_between(freq, 0, abs(spectrum), where=abs(spectrum) > 0, facecolor='green', interpolate=True)
            #ax2.set_title("Recorded Chunk Sec: " + str(len(self.data) / float(self.rate)))
            # ax2.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.1e'))
            ax2.grid(True)
            ax2.hold(False)
            plt.title("Recorded Chunk Sec: " + str(len(self.data) / float(self.rate)))
            self.canvas.draw()



            #elif self.mlFlag is 1 and self.namePre:

        '''
        data = [random.random() for i in range(10)]
        # create an axis
        ax = self.figure.add_subplot(111)
        # discards the old graph
        ax.hold(True)
        # plot data
        ax.plot(data, '*-')
        # refresh canvas
        self.canvas.draw()
        '''

    def start(self):
        global  generalresult
        if self.timer is None:
            self.recThread = threading.Thread(target=self.record)
            self.recThread.start()
            self.present = datetime.datetime.now()
            self.timer = QtCore.QTimer()
            self.timer.timeout.connect(self.tick)
            self.timer.start(10)
            self.chunksize.setDisabled(True)
            self.statusbar.showMessage("Analyzing Started")
            generalresult = "ANALYZING"

    def stop(self):
        global generalresult
        if self.timer is not None:
            self.statusbar.showMessage("Analyzing Stopped")
            self.timer.stop()
            self.timer = None
            self.addThread = None
            self.recThread = None
            self.inStream = None
            self.chunks = []
            self.chunksize.setEnabled(True)
            generalresult = "ANALYZING STOPPED!"

    def plotitem(self, item):
        index = self.lineEdit.currentRow()
        cmd=str(itemdatalist[index][4])+".jpg"
        os.system(cmd)

    def save(self):
        if self.figure:
            now = datetime.datetime.now()
            self.savename = now.isoformat().replace("T", "-").replace(":", "-") + "+" + self.displayTime.toString('mm-ss')
            if self.capFlag is 0:
                if self.displayTime:
                    self.figure.savefig("%s.png" % self.savename)
                    self.statusbar.showMessage(self.savename + ".png Saved on Current Directory")
            elif self.capFlag is 1:
                if self.data is not None:
                    scipy.io.wavfile.write("%s.wav" % self.savename, self.rate, self.data)
                    self.statusbar.showMessage(self.savename + ".wav Saved on Current Directory")
            elif self.capFlag is 2:
                if self.data is not None and self.displayTime:
                    self.figure.savefig("%s.png" % self.savename)
                    scipy.io.wavfile.write("%s.wav" % self.savename, self.rate, self.data)
                    self.statusbar.showMessage(self.savename + ".png and " + self.savename + ".wav Saved on Current Directory")


    def intchanged(self):
        self.buffer = 2 ** self.chunksize.value()
        self.statusbar.showMessage(
            "Current Buffer Size Changed: " + str(self.buffer * 2) + " Change will be affected on further analysis ")

    def degree(self):
        global dgr
        if self.zero.isChecked():
            dgr = 0
        elif self.sixty.isChecked():
            dgr=60
        elif self.d120.isChecked():
            dgr = 120
        elif self.d180.isChecked():
            dgr = 180
        elif self.d240.isChecked():
            dgr = 240
        elif self.d300.isChecked():
            dgr = 300
        ipaddress.addr.setText("192.168..:" + str(6000 + dgr))
        self.statusbar.showMessage("Client Position Changed to "+str(dgr)+" degree")

    def red(self):
        self.linecolor = "red"
        self.statusbar.showMessage("Fast Fourier Transform Mode Changed to Others")

    def hsvhandler(self, value):
        self.xlimit = self.horizontalSlider.value()
        self.statusbar.showMessage("X-limit Changed to: " + str(self.xlimit))

    def vsvhandler(self, value):
        self.ylimit = self.verticallSlider.value()
        self.statusbar.showMessage("Y-limit Changed to: " + str(self.ylimit))

    def scrmode(self):
        self.capFlag = 0
        self.statusbar.showMessage("Recording Mode Changed to Plot Only")

    def recmode(self):
        self.capFlag = 1
        self.statusbar.showMessage("Recording Mode Changed to Wave Only")

    def scrnrecmode(self):
        self.capFlag = 2
        self.statusbar.showMessage("Recording Mode Changed to Plot+Wave")

    def automode(self):
        if self.autopilot.isChecked():
            self.mlFlag=0
            self.statusbar.showMessage("Machine Learning Mode Changed to Autopilot")
    def manualmode(self):
        if self.supervise.isChecked():
            self.mlFlag=1
            self.statusbar.showMessage("Machine Learning Mode Changed to Manual")
            #name = QtGui.QFileDialog.getOpenself.savenames(None, u'녹음 파일 선택 - wav확장자를 가진 파일 하나를 열어주세요',QtGui.QDesktopServices.storageLocation(QtGui.QDesktopServices.MusicLocation),"Record (*.wav)");
            #name = QtGui.QFileDialog.getOpenself.savenames(None, u'녹음 파일 선택 - wav확장자를 가진 파일 하나를 열어주세요',"./","Record (*.wav)");
    '''
        if not name:
            return
        else:
            self.namePre=name[0]
            self.ratePre, X = scipy.io.wavfile.read(self.namePre)
            fnarray=self.namePre.split("\\")
            self.namePre=fnarray[len(fnarray)-1]
            self.spectrumPre = scipy.fftpack.fft(X)
            self.freqPre=scipy.fftpack.fftfreq(len(X), d=1.0 / self.ratePre)
            self.nsamPre=X.shape[0]
    '''

    def xlswrite(self):
        pixmap = QtGui.QPixmap.grabWidget(self.lineEdit)
        pixmap.save("Result.jpg")
        self.statusbar.showMessage("All Detected Items Stacked Were Saved In Result.jpg ")

    def queueclear(self):
        self.lineEdit.clear()
        itemdatalist=[]
        self.statusbar.showMessage("All Detected Items Stacked Were Cleared ")

    def thmode(self):
        '''
        for file in os.listdir("./X"):
            if file.endswith(".wav"):
                fnarray = file.split("/")
                tt=fnarray[len(fnarray) - 1]
                self.ratePre, X = scipy.io.wavfile.read("./X/"+file)
                self.spectrumPre = scipy.fftpack.fft(X)
                self.freqPre = scipy.fftpack.fftfreq(len(X), d=1.0 / self.ratePre)
                ax2 = self.figure.add_subplot(111)
                ax2.plot(self.freqPre, abs(self.spectrumPre), color=self.linecolor)
                ax2.set_xlim(1000, self.xlimit)
                ax2.set_ylim(0, 10000000)
                ax2.set_xlabel("frequency [Hz]")
                # ax2.set_title("Recorded Chunk Sec: " + str(len(self.data) / float(self.rate)))
                # ax2.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.1e'))
                ax2.set_title(tt)
                ax2.grid(True)
                #self.canvas.draw()
                print tt
                plt.savefig("%s.png" % tt, bbox_inches='tight')

            '''
        if self.thonly.isChecked():
            self.mlFlag = 2
            self.statusbar.showMessage("Machine Learning Mode Deactivated. Using Preset Threshold")

    def chkfir(self):
        if self.fir.isChecked()==False:
            self.lbnd1.setEnabled(False)
            self.rbnd1.setEnabled(False)
            self.th1.setEnabled(False)
        else:
            self.lbnd1.setEnabled(True)
            self.rbnd1.setEnabled(True)
            self.th1.setEnabled(True)

    def chksec(self):
        if self.sec.isChecked() == False:
            self.lbnd2.setEnabled(False)
            self.rbnd2.setEnabled(False)
            self.th2.setEnabled(False)
        else:
            self.lbnd2.setEnabled(True)
            self.rbnd2.setEnabled(True)
            self.th2.setEnabled(True)

    def chkthi(self):
        if self.thi.isChecked() == False:
            self.lbnd3.setEnabled(False)
            self.rbnd3.setEnabled(False)
            self.th3.setEnabled(False)
        else:
            self.lbnd3.setEnabled(True)
            self.rbnd3.setEnabled(True)
            self.th3.setEnabled(True)

    def lbnd1f(self):
        self.leftBoundary_1.setEnabled(False)
        self.leftBoundary_2.setEnabled(True)
        self.leftBoundary_3.setEnabled(True)
        self.rightBoundary_1.setEnabled(True)
        self.rightBoundary_2.setEnabled(True)
        self.rightBoundary_3.setEnabled(True)
        self.threshold_1.setEnabled(True)
        self.threshold_2.setEnabled(True)
        self.threshold_3.setEnabled(True)
        self.lbnd1.setFocus(True)
    def lbnd2f(self):
        self.leftBoundary_1.setEnabled(True)
        self.leftBoundary_2.setEnabled(False)
        self.leftBoundary_3.setEnabled(True)
        self.rightBoundary_1.setEnabled(True)
        self.rightBoundary_2.setEnabled(True)
        self.rightBoundary_3.setEnabled(True)
        self.threshold_1.setEnabled(True)
        self.threshold_2.setEnabled(True)
        self.threshold_3.setEnabled(True)
        self.lbnd2.setFocus(True)
    def lbnd3f(self):
        self.leftBoundary_1.setEnabled(True)
        self.leftBoundary_2.setEnabled(True)
        self.leftBoundary_3.setEnabled(False)
        self.rightBoundary_1.setEnabled(True)
        self.rightBoundary_2.setEnabled(True)
        self.rightBoundary_3.setEnabled(True)
        self.threshold_1.setEnabled(True)
        self.threshold_2.setEnabled(True)
        self.threshold_3.setEnabled(True)
        self.lbnd3.setFocus(True)


    def rbnd1f(self):
        self.leftBoundary_1.setEnabled(True)
        self.leftBoundary_2.setEnabled(True)
        self.leftBoundary_3.setEnabled(True)
        self.rightBoundary_1.setEnabled(False)
        self.rightBoundary_2.setEnabled(True)
        self.rightBoundary_3.setEnabled(True)
        self.threshold_1.setEnabled(True)
        self.threshold_2.setEnabled(True)
        self.threshold_3.setEnabled(True)
        self.rbnd1.setFocus(True)

    def rbnd2f(self):
        self.leftBoundary_1.setEnabled(True)
        self.leftBoundary_2.setEnabled(True)
        self.leftBoundary_3.setEnabled(True)
        self.rightBoundary_1.setEnabled(True)
        self.rightBoundary_2.setEnabled(False)
        self.rightBoundary_3.setEnabled(True)
        self.threshold_1.setEnabled(True)
        self.threshold_2.setEnabled(True)
        self.threshold_3.setEnabled(True)
        self.rbnd2.setFocus(True)
    def rbnd3f(self):
        self.leftBoundary_1.setEnabled(True)
        self.leftBoundary_2.setEnabled(True)
        self.leftBoundary_3.setEnabled(True)
        self.rightBoundary_1.setEnabled(True)
        self.rightBoundary_2.setEnabled(True)
        self.rightBoundary_3.setEnabled(False)
        self.threshold_1.setEnabled(True)
        self.threshold_2.setEnabled(True)
        self.threshold_3.setEnabled(True)
        self.rbnd3.setFocus(True)
    def th1f(self):
        self.leftBoundary_1.setEnabled(True)
        self.leftBoundary_2.setEnabled(True)
        self.leftBoundary_3.setEnabled(True)
        self.rightBoundary_1.setEnabled(True)
        self.rightBoundary_2.setEnabled(True)
        self.rightBoundary_3.setEnabled(True)
        self.threshold_1.setEnabled(False)
        self.threshold_2.setEnabled(True)
        self.threshold_3.setEnabled(True)
        self.th1.setFocus(True)
    def th2f(self):
        self.leftBoundary_1.setEnabled(True)
        self.leftBoundary_2.setEnabled(True)
        self.leftBoundary_3.setEnabled(True)
        self.rightBoundary_1.setEnabled(True)
        self.rightBoundary_2.setEnabled(True)
        self.rightBoundary_3.setEnabled(True)
        self.threshold_1.setEnabled(True)
        self.threshold_2.setEnabled(False)
        self.threshold_3.setEnabled(True)
        self.th2.setFocus(True)
    def th3f(self):
        self.leftBoundary_1.setEnabled(True)
        self.leftBoundary_2.setEnabled(True)
        self.leftBoundary_3.setEnabled(True)
        self.rightBoundary_1.setEnabled(True)
        self.rightBoundary_2.setEnabled(True)
        self.rightBoundary_3.setEnabled(True)
        self.threshold_1.setEnabled(True)
        self.threshold_2.setEnabled(True)
        self.threshold_3.setEnabled(False)
        self.th3.setFocus(True)

    def calcdap(self):
        global dapstat
        nzerocnt=0
        avgdap=0.00
        for per in self.dapper:
            if per>0:
                nzerocnt+=1
                avgdap+=per
        if nzerocnt>0:
            self.avgper=avgdap/float(nzerocnt)
            self.Dapp.display(self.avgper)
            dapstat=self.avgper
        else:
            self.Dapp.display(0.00)
            dapstat=0.00


    def calcndap(self):
        nzerocnt = 0
        avgndap = 0.00
        for per in self.ndapper:
            if per > 0:
                nzerocnt += 1
                avgndap += per
        #if nzerocnt > 0:
            #self.navgper = avgndap / float(nzerocnt)
            #self.nDapp.display(self.navgper)
        #else:
            #self.nDapp.display(0.00)

    def plotClick(self,value):
        if not str(value).__contains__("(None,None)"):
            arr=str(value).split("=")[2].lstrip("(").replace(") button","").split(",")
            xflt=float(arr[0])
            x=int(xflt)
            yflt=float(arr[1])
            y = int(yflt)
            if self.leftBoundary_1.isEnabled() is False:
                if x<self.rbnd1.value():
                    self.lbnd1.setValue(x)
                    self.leftBoundary_1.setEnabled(True)
            elif self.leftBoundary_2.isEnabled() is False:
                if x<self.rbnd2.value():
                    self.lbnd2.setValue(x)
                    self.leftBoundary_2.setEnabled(True)
            elif self.leftBoundary_3.isEnabled() is False:
                if x<self.rbnd3.value():
                    self.lbnd3.setValue(x)
                    self.leftBoundary_3.setEnabled(True)
            elif self.rightBoundary_1.isEnabled() is False:
                if x>self.lbnd1.value():
                    self.rbnd1.setValue(x)
                    self.rightBoundary_1.setEnabled(True)
            elif self.rightBoundary_2.isEnabled() is False:
                if x>self.lbnd2.value():
                    self.rbnd2.setValue(x)
                    self.rightBoundary_2.setEnabled(True)
            elif self.rightBoundary_3.isEnabled() is False:
                if x>self.lbnd3.value():
                    self.rbnd3.setValue(x)
                    self.rightBoundary_3.setEnabled(True)
            elif self.threshold_1.isEnabled() is False:
                self.th1.setValue(y)
                self.threshold_1.setEnabled(True)
            elif self.threshold_2.isEnabled() is False:
                self.th2.setValue(y)
                self.threshold_2.setEnabled(True)
            elif self.threshold_3.isEnabled() is False:
                self.th3.setValue(y)
                self.threshold_3.setEnabled(True)

            if self.legend.isChecked():
                self.x1r = range(self.lbnd1.value(), self.rbnd1.value())
                self.y1r = range(0, self.th1.value())
                self.llbnd1 = [self.lbnd1.value() for v in self.y1r]
                self.rrbnd1 = [self.rbnd1.value() for v in self.y1r]

                self.tth1 = [self.th1.value() for v in self.x1r]

                self.x2r = range(self.lbnd2.value(), self.rbnd2.value())
                self.y2r = range(0, self.th2.value())
                self.llbnd2 = [self.lbnd2.value() for v in self.y2r]
                self.rrbnd2 = [self.rbnd2.value() for v in self.y2r]
                self.tth2 = [self.th2.value() for v in self.x2r]

                self.x3r = range(self.lbnd3.value(), self.rbnd3.value())
                self.y3r = range(0, self.th3.value())
                self.llbnd3 = [self.lbnd3.value() for v in self.y3r]
                self.rrbnd3 = [self.rbnd3.value() for v in self.y3r]
                self.tth3 = [self.th3.value() for v in self.x3r]

    def mlsim(self,name):
        avgperO=0.0
        avgperX=0.0
        src=str(name)+".png"
        testImgBW = cv2.imread(src, cv2.CV_LOAD_IMAGE_GRAYSCALE)
        testImg = cv2.imread(src)
        imgarrO=[]
        imgarrX = []
        OcombinedImgAndSsim = {}
        OcombinedImgs = []
        XcombinedImgAndSsim = {}
        XcombinedImgs = []
        if not os.path.exists("./ML/"+str(name)):
            os.makedirs("./ML/"+str(name))
        if not os.path.exists("./ML/"+str(name)+"/O"):
            os.makedirs("./ML/"+str(name)+"/O")
        if not os.path.exists("./ML/"+str(name)+"/X"):
            os.makedirs("./ML/"+str(name)+"/X")
        for file in os.listdir("./O"):
            if file.endswith(".png"):
                imgarrO.append(file)
        for file in os.listdir("./X"):
            if file.endswith(".png"):
                imgarrX.append(file)

        for fname in imgarrO:
            ImgBW = cv2.imread("./O/" + fname, cv2.CV_LOAD_IMAGE_GRAYSCALE)
            Img = cv2.imread("./O/" + fname)
            sim = -ssim(testImgBW, ImgBW).__float__()  # similarity function
            combinedImg = cv2.addWeighted(Img, 0.5, testImg, 0.5, 0)  # combine two graph
            OcombinedImgAndSsim[sim] = combinedImg

        OsimList = OcombinedImgAndSsim.keys()
        for sim in OsimList:
            cv2.imwrite("./ML/"+str(name)+"/O/" + (-sim).__str__()[0:5] + ".png", OcombinedImgAndSsim[sim])
            avgperO+=sim
        avgperO/=len(OsimList)

        for fname in imgarrX:
            ImgBW = cv2.imread("./X/" + fname, cv2.CV_LOAD_IMAGE_GRAYSCALE)
            Img = cv2.imread("./X/" + fname)
            sim = -ssim(testImgBW, ImgBW).__float__()  # similarity function
            combinedImg = cv2.addWeighted(Img, 0.5, testImg, 0.5, 0)  # combine two graph
            XcombinedImgAndSsim[sim] = combinedImg

        XsimList = XcombinedImgAndSsim.keys()
        for sim in XsimList:
            cv2.imwrite("./ML/" + str(name) + "/X/" + (-sim).__str__()[0:5] + ".png", XcombinedImgAndSsim[sim])
            avgperX += sim
        avgperX /= len(OsimList)
        OorX=None
        if -avgperO>-avgperX:
            OorX="O"
        else:
            OorX = "X"
        rst=[-avgperO*100,-avgperX*100,OorX]
        return rst


    def itemadd(self,rtime,percent,chunk):
        global clstatus
        global generalresult
        global mlresult
        wid = animItemWidget(name=chunk[4])
        narr=self.savename.split("+")
        #wid.pixMap01.setText()
        wid.label_4.setText(narr[0])
        wid.label_2.setText(str(rtime)+" sec length")
        if self.mlFlag is not 2:
            rst=self.mlsim(name=chunk[4])
            if rst[2]=="O":
                pixmap02txt = "OML:" + str(round(rst[0], 2)) + "vs" + str(round(rst[1], 2)) + "\nThAvgDAP:" + str(
                    round(percent,2)) + "%"
                wid.pixMap02.setText(pixmap02txt)
            else:
                pixmap02txt = "XML:" + str(round(rst[1], 2)) + "vs" + str(round(rst[0], 2)) + "\nThAvgDAP:" + str(
                    round(percent,2)) + "%"
                wid.pixMap02.setText(pixmap02txt)
            if self.mlFlag is 0:
                if rst[2] == "O":
                    oldpath = "./" + chunk[4] + ".png"
                    newpath = "./O/" + chunk[4] + ".png"
                    shutil.move(oldpath, newpath)
                    self.cntPD+=1
                    wid.pixMap01.setText("OM")
                    pixmap02txt="OML:"+str(round(rst[0],2))+"vs"+str(round(rst[1],2))+"\nThAvgDAP:"+str(round(percent,2))+"%"
                    wid.pixMap02.setText(pixmap02txt)
                else:
                    oldpath = "./" + chunk[4] + ".png"
                    newpath = "./X/" + chunk[4] + ".png"
                    shutil.move(oldpath, newpath)
                    self.cntNonPD += 1
                    wid.pixMap01.setText("XM")
                    pixmap02txt = "XML:" + str(round(rst[1], 2)) + "vs" + str(round(rst[0], 2)) + "\nThAvgDAP:" + str(
                        round(percent,2)) + "%"
                    wid.pixMap02.setText(pixmap02txt)
                wid.button01.setEnabled(False)
                wid.button02.setEnabled(False)
                wid.button04.setEnabled(False)
            self.CntLcd.display("%s:%s" % (str(self.cntPD), str(self.cntNonPD)))
            # send result
            clstatus = "ONLINE\n" + str(self.displayTime.toString('mm:ss')) + "\nCollected Drone:" + str(
                self.cntPD) + "\nCollected Non-Drone:"+str(self.cntNonPD)
            self.nDapp.display("%s:%s" % (str(int(rst[0])), str(int(rst[1]))))
        else:
            wid.pixMap02.setText(str(percent)+"%")
        wid.label.setText("UAV-"+narr[1].replace("-",":"))
        #send result
        generalresult="Detection:"+str(wid.label.text())+"\nDetected Length:"+str(wid.label_2.text())+"\nEstimated DAP:"+str(wid.pixMap02.text())
        mlresult="Last Learning\n"+str(wid.pixMap01.text())+"\n@"+str(chunk[4])
        itemdatalist.append(chunk)
        wid2 = QtGui.QListWidgetItem()
        wid2.setSizeHint(QtCore.QSize(100, 55))
        self.lineEdit.addItem(wid2)
        self.lineEdit.setItemWidget(wid2, wid)
        self.lineEdit.scrollTo(self.lineEdit.model().index(len(itemdatalist)))
    def regasync(self):
        if len(self.regx)>1:
            xi = np.array(self.regx)
            # linearly generated sequence
            y = self.regy[:]
            # return the least-squares solution to a linear matrix equation.
            slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(xi, y)
            line = slope * xi + intercept
            content = 'R:' + str(r_value) + ' P:' + str(p_value) + '\nSTDdeviation:' + str(std_err)
            title = "Count:" + str(len(y)) + ' [Y]=' + str(slope) + '[X]+' + str(intercept)
            fig = plt.figure()
            fig.canvas.set_window_title(content)
            plt.title(title + '\n' + content)
            for index, xy in enumerate(zip(xi, y)):
                plt.annotate('(%s, %s)' % (int(xy[0]), int(xy[1])), xy=xy)
            plt.plot(xi, line, 'r-', xi, y, 'o')
            fig.savefig("LRegressDAPresult.png",bbox_inches='tight')
            os.system("LRegressDAPresult.png")
        else:
            self.statusbar.showMessage("At least 2 item has to be added to perform DAP Linear Regression")


    @QtCore.pyqtSlot()
    def destinate(self):
        self.statusbar.showMessage("0º=port 6000,60º=port 6060,120º=port 6120,180º=port 6180,240º=port 6240,300º=port 6300")
        ipaddress.conbtn.setEnabled(True)
        ipaddress.conbtn.setText("Connect")
        ipaddress.exec_()


class animItemWidget(QtGui.QWidget):

    def __init__(self,name ,parent=None):
        super(animItemWidget, self).__init__()
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self)
        self.horizontalLayout_4.setSpacing(2)
        self.horizontalLayout_4.setMargin(0)
        self.horizontalLayout_4.setObjectName(QtCore.QString.fromUtf8("horizontalLayout_4"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(QtCore.QString.fromUtf8("verticalLayout_2"))
        self.label = QtGui.QLabel(self)
        self.name=name

        fontLabel = QtGui.QFont()
        fontLabel.setPointSize(11)
        fontLabel.setWeight(75)
        fontLabel.setBold(True)

        fontMisc = QtGui.QFont()
        fontMisc.setPointSize(8)

        self.label.setFont(fontLabel)
        self.label.setObjectName(QtCore.QString.fromUtf8("label"))
        self.verticalLayout_2.addWidget(self.label)

        self.pixMap02 = QtGui.QLabel(self)
        #self.pixMap02.setText(QtCore.QString.fromUtf8("locaaaaaaaaa"))
        self.pixMap02.setObjectName(QtCore.QString.fromUtf8("pixMap02"))

        self.verticalLayout_2.addWidget(self.pixMap02)
        self.horizontalLayout_4.addLayout(self.verticalLayout_2)

        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(QtCore.QString.fromUtf8("verticalLayout"))

        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setObjectName(QtCore.QString.fromUtf8("horizontalLayout"))

        self.pixMap01 = QtGui.QLabel(self)
        #self.pixMap01.setText(QtCore.QString.fromUtf8("caaaaa"))
        self.pixMap01.setObjectName(QtCore.QString.fromUtf8("pixMap01"))
        self.horizontalLayout.addWidget(self.pixMap01)

        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)

        self.button02 = QtGui.QPushButton(self)
        self.button02.setMaximumSize(QtCore.QSize(30, 30))
        self.button02.setText(QtCore.QString.fromUtf8("No"))
        self.button02.setObjectName(QtCore.QString.fromUtf8("Ignore"))
        self.horizontalLayout.addWidget(self.button02)

        self.button01 = QtGui.QPushButton(self)
        self.button01.setMaximumSize(QtCore.QSize(30, 30))
        self.button01.setText(QtCore.QString.fromUtf8("O"))
        self.button01.setObjectName(QtCore.QString.fromUtf8("confirmPositive"))
        self.horizontalLayout.addWidget(self.button01)

        self.button04 = QtGui.QPushButton(self)
        self.button04.setMaximumSize(QtCore.QSize(30, 30))
        self.button04.setText(QtCore.QString.fromUtf8("X"))
        self.button04.setObjectName(QtCore.QString.fromUtf8("confirmNegative"))
        self.horizontalLayout.addWidget(self.button04)

        self.button03 = QtGui.QPushButton(self)
        self.button03.setMaximumSize(QtCore.QSize(30, 30))
        self.button03.setText(QtCore.QString.fromUtf8("pO"))
        self.button03.setObjectName(QtCore.QString.fromUtf8("galleryO"))
        self.horizontalLayout.addWidget(self.button03)

        self.button05 = QtGui.QPushButton(self)
        self.button05.setMaximumSize(QtCore.QSize(30, 30))
        self.button05.setText(QtCore.QString.fromUtf8("pX"))
        self.button05.setObjectName(QtCore.QString.fromUtf8("galleryX"))
        self.horizontalLayout.addWidget(self.button05)

        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(QtCore.QString.fromUtf8("horizontalLayout_3"))
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(QtCore.QString.fromUtf8("horizontalLayout_5"))

        self.label_2 = QtGui.QLabel(self)
        self.label_2.setFont(fontMisc)
        self.label_2.setObjectName(QtCore.QString.fromUtf8("label_2"))

        self.label_4 = QtGui.QLabel(self)
        self.label_4.setFont(fontMisc)
        self.label_4.setObjectName(QtCore.QString.fromUtf8("label_4"))

        self.horizontalLayout_3.addWidget(self.label_2)
        self.horizontalLayout_5.addWidget(self.label_4)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_4.addLayout(self.verticalLayout)

        self.connect(self.button02, QtCore.SIGNAL("clicked()"), self.deactivate)
        self.connect(self.button01, QtCore.SIGNAL("clicked()"), self.positive)
        self.connect(self.button04, QtCore.SIGNAL("clicked()"), self.negative)
        self.connect(self.button03, QtCore.SIGNAL("clicked()"), self.proofo)
        self.connect(self.button05, QtCore.SIGNAL("clicked()"), self.proofx)

    def deactivate(self):
        cmd="del "+str(self.name)+".png"
        os.system(cmd)
        self.setDisabled(True)
        self.pixMap01.setText("Del")
        self.pixMap02.setText("Deleted")
    def positive(self):
        global mlresult
        oldpath="./"+self.name+".png"
        newpath = "./O/" + self.name + ".png"
        shutil.move(oldpath,newpath)
        self.button01.setEnabled(False)
        self.button02.setEnabled(False)
        self.button04.setEnabled(False)
        if ui.mlFlag==2:
            self.pixMap01.setText("O-S")
            self.pixMap02.setText("O-Supervised")
        elif ui.mlFlag == 1:
            self.pixMap01.setText("O-S")
            ui.cntPD+=1
            ui.CntLcd.display("%s:%s" % (str(ui.cntPD), str(ui.cntNonPD)))
        mlresult="New Machine Learnt Case Report: "+str(self.pixMap01.text())+"\n"+str(ui.CntLcd.value)
    def negative(self):
        global mlresult
        oldpath="./"+self.name+".png"
        newpath = "./X/" + self.name + ".png"
        shutil.move(oldpath,newpath)
        self.button01.setEnabled(False)
        self.button02.setEnabled(False)
        self.button04.setEnabled(False)
        if ui.mlFlag==2:
            self.pixMap01.setText("X-S")
            self.pixMap02.setText("X-Supervised")
        elif ui.mlFlag==1:
            self.pixMap01.setText("X-S")
            ui.cntNonPD+=1
            ui.CntLcd.display("%s:%s" % (str(ui.cntPD), str(ui.cntNonPD)))
        mlresult = "New Machine Learnt Case Report: " + str(self.pixMap01.text()) + "\n" + str(ui.CntLcd.value)
    def proofo(self):
        if ui.mlFlag==2:
            os.startfile(os.getcwd()+"\\O")
        else:
            os.startfile(os.getcwd() + "\\ML\\"+str(self.name)+"\\O")
    def proofx(self):
        if ui.mlFlag==2:
            os.startfile(os.getcwd()+"\\X")
        else:
            os.startfile(os.getcwd() + "\\ML\\"+str(self.name)+"\\X")



if __name__ == "__main__":
    import sys

    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    ipaddress = destIPdiag()
    sys.exit(app.exec_())