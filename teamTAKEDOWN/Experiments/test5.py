# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'fft.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!
import datetime
import struct
import threading
import atexit
import pyaudio
import numpy as np
import random
import matplotlib
import scipy
import scipy.fftpack
import scipy.io.wavfile
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
# matplotlib.use("TkAgg")
from matplotlib import figure
from PyQt4 import QtCore, QtGui
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar

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


class Ui_MainWindow(object):
    # plot visualization variable
    present = None
    timer = None
    buffer = 16384
    linecolor = "green"
    # setting for pyaudio

    rate = 44100
    p = pyaudio.PyAudio()
    chunks = []
    inStream = None
    recThread = None
    addThread = None

    xlimit = 10000
    ylimit = 1000000

    displayTime = None
    data = None
    capFlag = 0

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
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1024, 768)
        MainWindow.setMinimumSize(QtCore.QSize(1024, 768))
        MainWindow.setMaximumSize(QtCore.QSize(1024, 768))

        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))

        self.plotlayout = QtGui.QVBoxLayout(self.centralwidget)
        # a figure instance to plot on
        self.figure = plt.figure()
        # this is the Canvas Widget that displays the `figure`
        self.canvas = FigureCanvas(self.figure)
        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self.centralwidget)
        self.plotlayout.addWidget(self.canvas)
        self.plotlayout.addWidget(self.toolbar)
        self.plotlayout.setObjectName(_fromUtf8("plotdisplay"))
        # self.centralwidget.setLayout(self.plotlayout)

        palettegl = QtGui.QPalette()
        palettegl.setBrush(QtGui.QPalette.Light, QtCore.Qt.black)

        self.lcdNumber = QtGui.QLCDNumber(self.centralwidget)
        self.lcdNumber.setGeometry(QtCore.QRect(340, 668, 91, 38))
        self.lcdNumber.setObjectName(_fromUtf8("lcdNumber"))
        self.lcdNumber.setPalette(palettegl)
        self.lcdNumber.display("00:00")

        self.chunksize = QtGui.QSpinBox(self.centralwidget)
        self.chunksize.setRange(10, 17)
        self.chunksize.setValue(14)
        self.chunksize.setGeometry(QtCore.QRect(740, 668, 55, 38))
        self.chunksize.setObjectName(_fromUtf8("chunksize"))
        self.chunksize.valueChanged.connect(self.intchanged)

        self.pushButton_4 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(640, 668, 91, 38))
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
        self.pushButton_4.clicked.connect(self.save)
        self.pushButton_4.connect(QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_F3), self.centralwidget),
                                  QtCore.SIGNAL('activated()'), self.save)

        self.pushButton_5 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(540, 668, 91, 38))
        self.pushButton_5.setObjectName(_fromUtf8("pushButton_5"))
        self.pushButton_5.clicked.connect(self.stop)
        self.pushButton_5.connect(QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_F2), self.centralwidget),
                                  QtCore.SIGNAL('activated()'), self.stop)

        self.pushButton_6 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_6.setGeometry(QtCore.QRect(440, 668, 91, 38))
        self.pushButton_6.setObjectName(_fromUtf8("pushButton_6"))
        self.pushButton_6.clicked.connect(self.start)
        self.pushButton_6.connect(QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_F1), self.centralwidget),
                                  QtCore.SIGNAL('activated()'), self.start)

        self.horizontalSlider = QtGui.QSlider(self.centralwidget)
        self.horizontalSlider.setRange(200, 20000)
        self.horizontalSlider.setValue(10000)
        self.horizontalSlider.valueChanged.connect(self.hsvhandler)
        self.horizontalSlider.setGeometry(QtCore.QRect(800, 668, 71, 38))
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName(_fromUtf8("horizontalSlider"))

        self.verticallSlider = QtGui.QSlider(self.centralwidget)
        self.verticallSlider.setRange(1000000, 5000000)
        self.verticallSlider.setValue(1000000)
        self.verticallSlider.valueChanged.connect(self.vsvhandler)
        self.verticallSlider.setGeometry(QtCore.QRect(880, 668, 71, 38))
        self.verticallSlider.setOrientation(QtCore.Qt.Vertical)
        self.verticallSlider.setObjectName(_fromUtf8("verticalSlider"))

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1024, 26))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFFT_Mode = QtGui.QMenu(self.menubar)
        self.menuFFT_Mode.setObjectName(_fromUtf8("menuDegree"))
        self.menuCapture = QtGui.QMenu(self.menubar)
        self.menuCapture.setObjectName(_fromUtf8("menuCapture"))

        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))

        MainWindow.setStatusBar(self.statusbar)
        ag = QtGui.QActionGroup(MainWindow, exclusive=True)
        self.actionDrone = ag.addAction(QtGui.QAction(MainWindow, checkable=True))
        self.actionDrone.setChecked(True)
        self.actionDrone.triggered.connect(self.green)
        self.actionDrone.setObjectName(_fromUtf8("zero"))
        self.actionOthers = ag.addAction(QtGui.QAction(MainWindow, checkable=True))
        self.actionOthers.triggered.connect(self.red)
        self.actionOthers.setObjectName(_fromUtf8("sixty"))
        self.menuFFT_Mode.addAction(self.actionDrone)
        self.menuFFT_Mode.addAction(self.actionOthers)
        self.menubar.addAction(self.menuFFT_Mode.menuAction())

        ag2 = QtGui.QActionGroup(MainWindow, exclusive=True)
        self.scr = ag2.addAction(QtGui.QAction(MainWindow, checkable=True))
        self.scr.setChecked(True)
        self.scr.triggered.connect(self.scrmode)
        self.scr.setObjectName(_fromUtf8("scrOnly"))
        self.rec = ag2.addAction(QtGui.QAction(MainWindow, checkable=True))
        self.rec.triggered.connect(self.recmode)
        self.rec.setObjectName(_fromUtf8("recOnly"))
        self.scrnrec = ag2.addAction(QtGui.QAction(MainWindow, checkable=True))
        self.scrnrec.triggered.connect(self.scrnrecmode)
        self.scrnrec.setObjectName(_fromUtf8("scrNrec"))
        self.menuCapture.addAction(self.scr)
        self.menuCapture.addAction(self.rec)
        self.menuCapture.addAction(self.scrnrec)
        self.menubar.addAction(self.menuCapture.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow",
                                             "Realtime Fast Fourier Transform Analyzer For Caputuring Payloaded Drone Frequency-Made by Kiefer Kim",
                                             None))
        self.pushButton_4.setText(_translate("MainWindow", "Record(F3)", None))
        self.pushButton_5.setText(_translate("MainWindow", "Stop(F2)", None))
        self.pushButton_6.setText(_translate("MainWindow", "Analyze(F1)", None))
        self.menuFFT_Mode.setTitle(_translate("MainWindow", "FFT Type", None))
        self.actionDrone.setText(_translate("MainWindow", "Payloaded Drone", None))
        self.actionOthers.setText(_translate("MainWindow", "Others", None))
        self.menuCapture.setTitle(_translate("MainWindow", "Record Mode", None))
        self.scr.setText(_translate("MainWindow", "Plot.png Only", None))
        self.rec.setText(_translate("MainWindow", "Record.wav Only", None))
        self.scrnrec.setText(_translate("MainWindow", "Plot.png+Record.wav", None))

    def tick(self):
        now = datetime.datetime.now()
        minutes, seconds = divmod((now - self.present).total_seconds(), 60)
        self.displayTime = QtCore.QTime(0, minutes, round(seconds))
        self.lcdNumber.display(self.displayTime.toString('mm:ss'))
        if len(self.chunks) > 0:
            X = self.chunks.pop(0)
            self.data = scipy.array(struct.unpack("%dB" % (self.buffer * 2), X))

            # print "RECORDED",len(self.data)/float(self.rate),"SEC"
            # ffty = scipy.fftpack.fft(self.data)
            # fftx = scipy.fftpack.rfftfreq(self.buffer * 2, 1.0 / self.rate)

            spectrum = scipy.fftpack.fft(self.data)
            freq = scipy.fftpack.fftfreq(len(self.data), d=0.5 / self.rate)

            ax2 = self.figure.add_subplot(111)
            ax2.plot(freq, abs(spectrum), color=self.linecolor)
            ax2.set_xlim(0, self.xlimit)
            ax2.set_ylim(0, self.ylimit)
            ax2.set_xlabel("frequency [Hz]")
            ax2.set_title("Recorded Chunk Sec: " + str(len(self.data) / float(self.rate)))
            # ax2.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.1e'))
            ax2.grid(True)
            ax2.hold(False)
            self.canvas.draw()

            # print data

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
        if self.timer is None:
            self.recThread = threading.Thread(target=self.record)
            self.recThread.start()
            self.present = datetime.datetime.now()
            self.timer = QtCore.QTimer()
            self.timer.timeout.connect(self.tick)
            self.timer.start(10)
            self.chunksize.setDisabled(True)
            self.statusbar.showMessage("Analyzing Started")

    def stop(self):
        if self.timer is not None:
            self.statusbar.showMessage("Analyzing Stopped")
            self.timer.stop()
            self.timer = None
            self.addThread = None
            self.recThread = None
            self.inStream = None
            self.chunks = []
            self.chunksize.setEnabled(True)

    def save(self):
        if self.figure:
            now = datetime.datetime.now()
            filename = now.isoformat().replace("T", "-").replace(":", "-") + "+" + self.displayTime.toString('mm-ss')
            if self.capFlag is 0:
                if self.displayTime:
                    self.figure.savefig("%s.png" % filename, bbox_inches='tight')
                    self.statusbar.showMessage(filename + ".png Saved on Current Directory")
            elif self.capFlag is 1:
                if self.data is not None:
                    scipy.io.wavfile.write("%s.wav" % filename, self.rate, self.data)
                    self.statusbar.showMessage(filename + ".wav Saved on Current Directory")
            elif self.capFlag is 2:
                if self.data is not None and self.displayTime:
                    self.figure.savefig("%s.png" % filename, bbox_inches='tight')
                    scipy.io.wavfile.write("%s.wav" % filename, self.rate, self.data)
                    self.statusbar.showMessage(filename + ".png and " + filename + ".wav Saved on Current Directory")

    def intchanged(self):
        self.buffer = 2 ** self.chunksize.value()
        self.statusbar.showMessage(
            "Current Buffer Size Changed: " + str(self.buffer * 2) + " Change will be affected on further analysis ")

    def green(self):
        self.linecolor = "green"
        self.statusbar.showMessage("Fast Fourier Transform Mode Changed to Payloaded Drone")

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


if __name__ == "__main__":
    import sys

    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())