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

import os
import socket
import threading
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QPushButton
from PyQt4 import QtCore, QtGui

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

data=None
content=''
rdp0 = None
rdp60 = None
rdp120 = None
rdp180 = None
rdp240 = None
rdp300 = None
class Ui_MainWindow(object):
    work0 = None
    work60 = None
    work120 = None
    work180 = None
    work240 = None
    work300 = None

    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.setMinimumSize(QtCore.QSize(640, 0))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout_2 = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setContentsMargins(0, -1, -1, -1)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setStyleSheet(_fromUtf8("QLabel { background-color : yellow; font-weight: bold}"))
        self.label_3.setFrameShape(QtGui.QFrame.NoFrame)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout.addWidget(self.label_3)

        self.lcdNumber = QtGui.QLCDNumber(self.centralwidget)
        self.lcdNumber.setObjectName(_fromUtf8("lcdNumber"))
        self.verticalLayout.addWidget(self.lcdNumber)

        self.gridLayout.addLayout(self.verticalLayout, 0, 2, 1, 1)
        self.verticalLayout_9 = QtGui.QVBoxLayout()
        self.verticalLayout_9.setObjectName(_fromUtf8("verticalLayout_9"))
        self.label_16 = QtGui.QLabel(self.centralwidget)
        self.label_16.setStyleSheet(_fromUtf8("QLabel { background-color : pink; font-weight: bold;}"))
        self.label_16.setAlignment(QtCore.Qt.AlignCenter)
        self.label_16.setObjectName(_fromUtf8("label_16"))
        self.verticalLayout_9.addWidget(self.label_16)

        self.lcdNumber_6 = QtGui.QLCDNumber(self.centralwidget)
        self.lcdNumber_6.setObjectName(_fromUtf8("lcdNumber_6"))
        self.verticalLayout_9.addWidget(self.lcdNumber_6)

        self.gridLayout.addLayout(self.verticalLayout_9, 3, 0, 1, 1)
        self.verticalLayout_10 = QtGui.QVBoxLayout()
        self.verticalLayout_10.setObjectName(_fromUtf8("verticalLayout_10"))
        self.label_6 = QtGui.QLabel(self.centralwidget)
        self.label_6.setStyleSheet(_fromUtf8("QLabel { background-color : red; color:white; font-weight: bold}\n"
""))
        self.label_6.setFrameShape(QtGui.QFrame.NoFrame)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.verticalLayout_10.addWidget(self.label_6)

        self.lcdNumber_7 = QtGui.QLCDNumber(self.centralwidget)
        self.lcdNumber_7.setObjectName(_fromUtf8("lcdNumber_7"))
        self.verticalLayout_10.addWidget(self.lcdNumber_7)

        self.gridLayout.addLayout(self.verticalLayout_10, 1, 0, 1, 1)
        self.verticalLayout_7 = QtGui.QVBoxLayout()
        self.verticalLayout_7.setObjectName(_fromUtf8("verticalLayout_7"))
        self.label_20 = QtGui.QLabel(self.centralwidget)
        self.label_20.setStyleSheet(_fromUtf8("QLabel { background-color : orange; font-weight: bold;}\n"
""))
        self.label_20.setAlignment(QtCore.Qt.AlignCenter)
        self.label_20.setObjectName(_fromUtf8("label_20"))
        self.verticalLayout_7.addWidget(self.label_20)

        self.lcdNumber_4 = QtGui.QLCDNumber(self.centralwidget)
        self.lcdNumber_4.setObjectName(_fromUtf8("lcdNumber_4"))

        self.verticalLayout_7.addWidget(self.lcdNumber_4)
        self.gridLayout.addLayout(self.verticalLayout_7, 3, 4, 1, 1)
        self.verticalLayout_6 = QtGui.QVBoxLayout()
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.label_10 = QtGui.QLabel(self.centralwidget)
        self.label_10.setStyleSheet(_fromUtf8("QLabel { background-color : green; color:white; font-weight: bold; }"))
        self.label_10.setAlignment(QtCore.Qt.AlignCenter)
        self.label_10.setWordWrap(False)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.verticalLayout_6.addWidget(self.label_10)

        self.lcdNumber_3 = QtGui.QLCDNumber(self.centralwidget)
        self.lcdNumber_3.setObjectName(_fromUtf8("lcdNumber_3"))

        self.verticalLayout_6.addWidget(self.lcdNumber_3)
        self.gridLayout.addLayout(self.verticalLayout_6, 1, 4, 1, 1)
        self.verticalLayout_8 = QtGui.QVBoxLayout()
        self.verticalLayout_8.setObjectName(_fromUtf8("verticalLayout_8"))
        self.label_23 = QtGui.QLabel(self.centralwidget)
        self.label_23.setStyleSheet(_fromUtf8("QLabel { background-color : blue; color:white ;font-weight: bold; }"))
        self.label_23.setAlignment(QtCore.Qt.AlignCenter)
        self.label_23.setObjectName(_fromUtf8("label_23"))
        self.verticalLayout_8.addWidget(self.label_23)

        self.lcdNumber_5 = QtGui.QLCDNumber(self.centralwidget)
        self.lcdNumber_5.setObjectName(_fromUtf8("lcdNumber_5"))
        self.verticalLayout_8.addWidget(self.lcdNumber_5)
        self.gridLayout.addLayout(self.verticalLayout_8, 4, 2, 1, 1)
        self.verticalLayout_4 = QtGui.QVBoxLayout()
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.label_13 = QtGui.QLabel(self.centralwidget)
        self.label_13.setStyleSheet(_fromUtf8("QLabel { background-color : black; color : white; font-weight: bold;}"))
        self.label_13.setAlignment(QtCore.Qt.AlignCenter)
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.verticalLayout_4.addWidget(self.label_13)
        self.lcdNumber_2 = QtGui.QLCDNumber(self.centralwidget)
        self.lcdNumber_2.setObjectName(_fromUtf8("lcdNumber_2"))
        self.verticalLayout_4.addWidget(self.lcdNumber_2)
        self.gridLayout.addLayout(self.verticalLayout_4, 2, 2, 1, 1)
        self.label_4 = QtGui.QLabel(self.centralwidget)
        self.label_4.setStyleSheet(_fromUtf8("QLabel { background-color : yellow;}"))
        self.label_4.setFrameShape(QtGui.QFrame.NoFrame)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 0, 3, 1, 1)
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setStyleSheet(_fromUtf8("QLabel { background-color : yellow;}"))
        self.label_2.setFrameShape(QtGui.QFrame.NoFrame)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)
        self.label_5 = QtGui.QLabel(self.centralwidget)
        self.label_5.setStyleSheet(_fromUtf8("QLabel { background-color : green; color:white; }"))
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 0, 4, 1, 1)
        self.label_7 = QtGui.QLabel(self.centralwidget)
        self.label_7.setStyleSheet(_fromUtf8("QLabel { background-color : red; color:white; }"))
        self.label_7.setFrameShape(QtGui.QFrame.NoFrame)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout.addWidget(self.label_7, 1, 1, 1, 1)
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setStyleSheet(_fromUtf8("QLabel { background-color : red; color:white; }"))
        self.label.setFrameShape(QtGui.QFrame.NoFrame)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_8 = QtGui.QLabel(self.centralwidget)
        self.label_8.setStyleSheet(_fromUtf8("QLabel { background-color : yellow;}"))
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout.addWidget(self.label_8, 1, 2, 1, 1)
        self.label_9 = QtGui.QLabel(self.centralwidget)
        self.label_9.setStyleSheet(_fromUtf8("QLabel { background-color : green; color:white; }"))
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.gridLayout.addWidget(self.label_9, 1, 3, 1, 1)
        self.label_17 = QtGui.QLabel(self.centralwidget)
        self.label_17.setStyleSheet(_fromUtf8("QLabel { background-color : pink;}"))
        self.label_17.setAlignment(QtCore.Qt.AlignCenter)
        self.label_17.setObjectName(_fromUtf8("label_17"))
        self.gridLayout.addWidget(self.label_17, 3, 1, 1, 1)
        self.label_18 = QtGui.QLabel(self.centralwidget)
        self.label_18.setStyleSheet(_fromUtf8("QLabel { background-color : blue; color: white }"))
        self.label_18.setAlignment(QtCore.Qt.AlignCenter)
        self.label_18.setObjectName(_fromUtf8("label_18"))
        self.gridLayout.addWidget(self.label_18, 3, 2, 1, 1)
        self.label_19 = QtGui.QLabel(self.centralwidget)
        self.label_19.setStyleSheet(_fromUtf8("QLabel { background-color : orange;}"))
        self.label_19.setAlignment(QtCore.Qt.AlignCenter)
        self.label_19.setObjectName(_fromUtf8("label_19"))
        self.gridLayout.addWidget(self.label_19, 3, 3, 1, 1)
        self.label_15 = QtGui.QLabel(self.centralwidget)
        self.label_15.setStyleSheet(_fromUtf8("QLabel { background-color : green; color:white; }"))
        self.label_15.setFrameShape(QtGui.QFrame.NoFrame)
        self.label_15.setLineWidth(1)
        self.label_15.setAlignment(QtCore.Qt.AlignCenter)
        self.label_15.setObjectName(_fromUtf8("label_15"))
        self.gridLayout.addWidget(self.label_15, 2, 4, 1, 1)
        self.label_21 = QtGui.QLabel(self.centralwidget)
        self.label_21.setStyleSheet(_fromUtf8("QLabel { background-color : pink;}"))
        self.label_21.setAlignment(QtCore.Qt.AlignCenter)
        self.label_21.setObjectName(_fromUtf8("label_21"))
        self.gridLayout.addWidget(self.label_21, 4, 0, 1, 1)
        self.label_11 = QtGui.QLabel(self.centralwidget)
        self.label_11.setStyleSheet(_fromUtf8("QLabel { background-color : red; color:white; }"))
        self.label_11.setFrameShape(QtGui.QFrame.NoFrame)
        self.label_11.setAlignment(QtCore.Qt.AlignCenter)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.gridLayout.addWidget(self.label_11, 2, 0, 1, 1)
        self.label_22 = QtGui.QLabel(self.centralwidget)
        self.label_22.setStyleSheet(_fromUtf8("QLabel { background-color : blue;color: white }"))
        self.label_22.setAlignment(QtCore.Qt.AlignCenter)
        self.label_22.setObjectName(_fromUtf8("label_22"))
        self.gridLayout.addWidget(self.label_22, 4, 1, 1, 1)
        self.label_12 = QtGui.QLabel(self.centralwidget)
        self.label_12.setStyleSheet(_fromUtf8("QLabel { background-color : pink;}"))
        self.label_12.setAlignment(QtCore.Qt.AlignCenter)
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.gridLayout.addWidget(self.label_12, 2, 1, 1, 1)
        self.label_24 = QtGui.QLabel(self.centralwidget)
        self.label_24.setStyleSheet(_fromUtf8("QLabel { background-color : blue;color: white }"))
        self.label_24.setAlignment(QtCore.Qt.AlignCenter)
        self.label_24.setObjectName(_fromUtf8("label_24"))
        self.gridLayout.addWidget(self.label_24, 4, 3, 1, 1)
        self.label_14 = QtGui.QLabel(self.centralwidget)
        self.label_14.setStyleSheet(_fromUtf8("QLabel { background-color : orange;}"))
        self.label_14.setAlignment(QtCore.Qt.AlignCenter)
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.gridLayout.addWidget(self.label_14, 2, 3, 1, 1)
        self.label_25 = QtGui.QLabel(self.centralwidget)
        self.label_25.setStyleSheet(_fromUtf8("QLabel { background-color : orange;}"))
        self.label_25.setAlignment(QtCore.Qt.AlignCenter)
        self.label_25.setObjectName(_fromUtf8("label_25"))
        self.gridLayout.addWidget(self.label_25, 4, 4, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        #timer
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.tick)
        self.timer.start(0)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 640, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuActivate = QtGui.QMenu(self.menubar)
        self.menuActivate.setObjectName(_fromUtf8("menuActivate"))
        self.menuRC = QtGui.QMenu(self.menubar)
        self.menuRC.setObjectName(_fromUtf8("menuRC"))

        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))

        MainWindow.setStatusBar(self.statusbar)
        self.action0 = QtGui.QAction(MainWindow)
        self.action0.setObjectName(_fromUtf8("action0"))

        self.action60 = QtGui.QAction(MainWindow)
        self.action60.setObjectName(_fromUtf8("action60"))

        self.action120 = QtGui.QAction(MainWindow)
        self.action120.setObjectName(_fromUtf8("action120"))

        self.action180 = QtGui.QAction(MainWindow)
        self.action180.setObjectName(_fromUtf8("action180"))

        self.action240 = QtGui.QAction(MainWindow)
        self.action240.setObjectName(_fromUtf8("action240"))

        self.action300 = QtGui.QAction(MainWindow)
        self.action300.setObjectName(_fromUtf8("action300"))

        self.action0_2 = QtGui.QAction(MainWindow)
        self.action0_2.setObjectName(_fromUtf8("action0_2"))

        self.action60_2 = QtGui.QAction(MainWindow)
        self.action60_2.setObjectName(_fromUtf8("action60_2"))

        self.action120_2 = QtGui.QAction(MainWindow)
        self.action120_2.setObjectName(_fromUtf8("action120_2"))

        self.action180_2 = QtGui.QAction(MainWindow)
        self.action180_2.setObjectName(_fromUtf8("action180_2"))

        self.action240_2 = QtGui.QAction(MainWindow)
        self.action240_2.setObjectName(_fromUtf8("action240_2"))

        self.action300_2 = QtGui.QAction(MainWindow)
        self.action300_2.setObjectName(_fromUtf8("action300_2"))

        agO = QtGui.QActionGroup(MainWindow, exclusive=False)
        self.action0= agO.addAction(QtGui.QAction(MainWindow, checkable=True))
        self.action0.triggered.connect(self.port0)

        self.action60 = agO.addAction(QtGui.QAction(MainWindow, checkable=True))
        self.action60.triggered.connect(self.port60)

        self.action120 = agO.addAction(QtGui.QAction(MainWindow, checkable=True))
        self.action120.triggered.connect(self.port120)

        self.action180 = agO.addAction(QtGui.QAction(MainWindow, checkable=True))
        self.action180.triggered.connect(self.port180)

        self.action240 = agO.addAction(QtGui.QAction(MainWindow, checkable=True))
        self.action240.triggered.connect(self.port240)

        self.action300 = agO.addAction(QtGui.QAction(MainWindow, checkable=True))
        self.action300.triggered.connect(self.port300)

        self.action0.setChecked(True)
        self.action60.setChecked(True)
        self.action120.setChecked(True)
        self.action180.setChecked(True)
        self.action240.setChecked(True)
        self.action300.setChecked(True)

        agX = QtGui.QActionGroup(MainWindow, exclusive=True)
        self.action0_2 = agX.addAction(QtGui.QAction(MainWindow, checkable=True))
        self.action60_2 = agX.addAction(QtGui.QAction(MainWindow, checkable=True))
        self.action120_2 = agX.addAction(QtGui.QAction(MainWindow, checkable=True))
        self.action180_2 = agX.addAction(QtGui.QAction(MainWindow, checkable=True))
        self.action240_2 = agX.addAction(QtGui.QAction(MainWindow, checkable=True))
        self.action300_2 = agX.addAction(QtGui.QAction(MainWindow, checkable=True))

        self.action0_2.triggered.connect(self.mstsc0)
        self.action60_2.triggered.connect(self.mstsc0)
        self.action120_2.triggered.connect(self.mstsc0)
        self.action180_2.triggered.connect(self.mstsc0)
        self.action240_2.triggered.connect(self.mstsc0)
        self.action300_2.triggered.connect(self.mstsc0)

        self.menuActivate.addAction(self.action0)
        self.menuActivate.addAction(self.action60)
        self.menuActivate.addAction(self.action120)
        self.menuActivate.addAction(self.action180)
        self.menuActivate.addAction(self.action240)
        self.menuActivate.addAction(self.action300)

        self.menuRC.addAction(self.action0_2)
        self.menuRC.addAction(self.action60_2)
        self.menuRC.addAction(self.action120_2)
        self.menuRC.addAction(self.action180_2)
        self.menuRC.addAction(self.action240_2)
        self.menuRC.addAction(self.action300_2)

        self.menubar.addAction(self.menuActivate.menuAction())
        self.menubar.addAction(self.menuRC.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def tick(self):
        global data
        global content
        if data is not None:
            arr=['','','','','']
            try:
                if data.split("#")[0] !=data:
                    arr[0]=data.split("#")[1]
                if data.split("$")[0] !=data:
                    arr[1]=data.split("$")[1]
                if data.split("^")[0] !=data:
                    arr[2]=data.split("^")[1]
                if data.split("&")[0] !=data:
                    arr[3]=data.split("&")[1]
                if data.split("*")[0] !=data:
                    arr[4]=data.split("*")[1]
            except:
                if content=='':
                    content+=data
                    return
                else:
                    data=content+data
                    content=''
                    if data.split("#")[0] !=data:
                        arr[0]=data.split("#")[1]
                    if data.split("$")[0] !=data:
                        arr[1]=data.split("$")[1]
                    if data.split("^")[0] !=data:
                        arr[2]=data.split("^")[1]
                    if data.split("&")[0] !=data:
                        arr[3]=data.split("&")[1]
                    if data.split("*")[0] !=data:
                        arr[4]=data.split("*")[1]
            if arr[0]!='':
                if arr[0]=="0":
                    self.lcdNumber.display(arr[1])
                    self.label_2.setText(u'0º General Report\n'+arr[2])
                    self.label_8.setText(u'0º Client Status\n' + arr[3])
                    self.label_4.setText(u'0º Machine Learnt\n' + arr[4])
                elif arr[0]=="60":
                    self.lcdNumber_3.display(arr[1])
                    self.label_5.setText(u'60º General Report\n'+arr[2])
                    self.label_9.setText(u'60º Client Status\n' + arr[3])
                    self.label_15.setText(u'60º Machine Learnt\n' + arr[4])
                elif arr[0]=="120":
                    self.lcdNumber_4.display(arr[1])
                    self.label_14.setText(u'120º General Report\n'+arr[2])
                    self.label_19.setText(u'120º Client Status\n' + arr[3])
                    self.label_25.setText(u'120º Machine Learnt\n'+ arr[4])
                elif arr[0]=="180":
                    self.lcdNumber_5.display(arr[1])
                    self.label_22.setText(u'180º General Report\n'+arr[2])
                    self.label_18.setText(u'180º Client Status\n' + arr[3])
                    self.label_24.setText(u'180º Machine Learnt\n' + arr[4])
                elif arr[0] == "240":
                    self.lcdNumber_6.display(arr[1])
                    self.label_12.setText(u'240º General Report\n' + arr[2])
                    self.label_17.setText(u'240º Client Status\n' + arr[3])
                    self.label_21.setText(u'240º Machine Learnt\n'+ arr[4])
                elif arr[0] == "300":
                    self.lcdNumber_7.display(arr[1])
                    self.label.setText(u'300º General Report\n'+ arr[2])
                    self.label_7.setText(u'300º Client Status\n' + arr[3])
                    self.label_11.setText(u'300º Machine Learnt\n'+ arr[4])

        sum=(float(self.lcdNumber.value()) + float(self.lcdNumber_3.value()) + float(
                    self.lcdNumber_4.value()) + float(self.lcdNumber_5.value()) + float(
                    self.lcdNumber_6.value()) + float(self.lcdNumber_7.value()))
        if round(sum,3)==0.000 or round(sum,3)==0.00 or round(sum,3)==0.0 or round(sum,3)==0:
                self.lcdNumber_2.display("-----")
        else:
            dap0=float(self.lcdNumber.value())
            dap60=float(self.lcdNumber_3.value())
            dap120=float(self.lcdNumber_4.value())
            dap180=float(self.lcdNumber_5.value())
            dap240=float(self.lcdNumber_6.value())
            dap300=float(self.lcdNumber_7.value())
            if dap0>0 and dap0>dap60 and dap0>dap120 and dap0>dap180 and dap0>dap240 and dap0>dap300:
                if dap60>0 and dap60>dap300:
                    dgr=((dap0/(dap0+dap60))*60)
                    stdgr=str(dgr)+"'"
                    self.lcdNumber_2.display(stdgr)
                elif dap300>0 and dap300>dap60:
                    dgr = 300+((dap300 / (dap300 + dap0)) * 60)
                    stdgr = str(dgr) + "'"
                    self.lcdNumber_2.display(stdgr)
                else:
                    self.lcdNumber_2.display("0'")
            elif dap60 > 0 and dap60 > dap0 and dap60 > dap120 and dap60 > dap180 and dap60 > dap240 and dap60 > dap300:
                if dap0>0 and dap0>dap120:
                    dgr=((dap0/(dap0+dap60))*60)
                    stdgr=str(dgr)+"'"
                    self.lcdNumber_2.display(stdgr)
                elif dap120>0 and dap120>dap0:
                    dgr = 60+((dap60 / (dap120 + dap60)) * 60)
                    stdgr = str(dgr) + "'"
                    self.lcdNumber_2.display(stdgr)
                else:
                    self.lcdNumber_2.display("60'")
            elif dap120 > 0 and dap120 > dap60 and dap120 > dap0 and dap120 > dap180 and dap120 > dap240 and dap120 > dap300:
                if dap60>0 and dap60>dap180:
                    dgr=60+((dap60/(dap60+dap120))*60)
                    stdgr=str(dgr)+"'"
                    self.lcdNumber_2.display(stdgr)
                elif dap180>0 and dap180>dap60:
                    dgr = 120+((dap120 / (dap120 + dap180)) * 60)
                    stdgr = str(dgr) + "'"
                    self.lcdNumber_2.display(stdgr)
                else:
                    self.lcdNumber_2.display("120'")
            elif dap180 > 0 and dap180 > dap60 and dap180 > dap120 and dap180 > dap240 and dap180 > dap300 and dap180 > dap0:
                if dap120>0 and dap120>dap240:
                    dgr=120+((dap120/(dap120+dap180))*60)
                    stdgr=str(dgr)+"'"
                    self.lcdNumber_2.display(stdgr)
                elif dap240>0 and dap240>dap120:
                    dgr = 180+((dap180 / (dap240 + dap180)) * 60)
                    stdgr = str(dgr) + "'"
                    self.lcdNumber_2.display(stdgr)
                else:
                    self.lcdNumber_2.display("180'")
            elif dap240 > 0 and dap240 > dap60 and dap240 > dap120 and dap240 > dap180 and dap240 > dap0 and dap240 > dap300:
                if dap180>0 and dap180>dap300:
                    dgr=180+((dap180/(dap180+dap240))*60)
                    stdgr=str(dgr)+"'"
                    self.lcdNumber_2.display(stdgr)
                elif dap300>0 and dap300>dap180:
                    dgr = 240+((dap240 / (dap300 + dap240)) * 60)
                    stdgr = str(dgr) + "'"
                    self.lcdNumber_2.display(stdgr)
                else:
                    self.lcdNumber_2.display("240'")
            elif  dap300>0 and dap300>dap60 and dap300>dap120 and dap300>dap180 and dap300>dap240 and dap300>dap0:
                if dap240>0 and dap240>dap0:
                    dgr=240+((dap240/(dap240+dap300))*60)
                    stdgr=str(dgr)+"'"
                    self.lcdNumber_2.display(stdgr)
                elif dap0>0 and dap0>dap240:
                    dgr = 300+((dap300 / (dap300 + dap0)) * 60)
                    stdgr = str(dgr) + "'"
                    self.lcdNumber_2.display(stdgr)
                else:
                    self.lcdNumber_2.display("300'")
    def mstsc0(self):
        global rdp0
        global rdp60
        global rdp120
        global rdp180
        global rdp240
        global rdp300
        cmd="mstsc /admin /v "
        if self.action0_2.isChecked() and rdp0 is not None:
            print cmd+rdp0
            os.system(cmd+rdp0)
        elif self.action60_2.isChecked() and rdp60 is not None:
            os.system(cmd + rdp60)
        elif self.action120_2.isChecked() and rdp120 is not None:
            os.system(cmd + rdp120)
        elif self.action180_2.isChecked() and rdp180 is not None:
            os.system(cmd + rdp180)
        elif self.action240_2.isChecked() and rdp240 is not None:
            os.system(cmd + rdp240)
        elif self.action300_2.isChecked() and rdp300 is not None:
            os.system(cmd + rdp300)

    def port0(self):
        if self.action0.isChecked():
            if self.work0 is None:
                PORT = 6000
                self.work0=ThreadedServer('', PORT)
                threading.Thread(target=self.work0.listen).start()
        else:
            self.work0=None
    def port60(self):
        if self.action60.isChecked():
            if self.work60 is None:
                PORT = 6060
                self.work60 = ThreadedServer('', PORT)
                threading.Thread(target=self.work60.listen).start()
            else:
                self.work60 = None
    def port120(self):
        if self.action120.isChecked():
            if self.work120 is None:
                PORT = 6120
                self.work120 = ThreadedServer('', PORT)
                threading.Thread(target=self.work120.listen).start()
            else:
                self.work120 = None
    def port180(self):
        if self.action180.isChecked():
            if self.work180 is None:
                PORT = 6180
                self.work180 = ThreadedServer('', PORT)
                threading.Thread(target=self.work180.listen).start()
            else:
                self.work180 = None
    def port240(self):
        if self.action240.isChecked():
            if self.work240 is None:
                PORT = 6240
                self.work240 = ThreadedServer('', PORT)
                threading.Thread(target=self.work240.listen).start()
            else:
                self.work240 = None
    def port300(self):
        if self.action300.isChecked():
            if self.work300 is None:
                PORT = 6300
                self.work300 = ThreadedServer('', PORT)
                threading.Thread(target=self.work300.listen).start()
            else:
                self.work300 = None

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "United States Air Force Realtime Drone Air Defense Control(Radar) System Server- Made by Team TAKEDOWN", None))
        self.label_3.setText(_translate("MainWindow", "0º", None))
        self.label_16.setText(_translate("MainWindow", "240º", None))
        self.label_6.setText(_translate("MainWindow", "300º", None))
        self.label_20.setText(_translate("MainWindow", "120º", None))
        self.label_10.setText(_translate("MainWindow", "60º", None))
        self.label_23.setText(_translate("MainWindow", "180º", None))
        self.label_13.setText(_translate("MainWindow", "Degree", None))

        self.label_2.setText(_translate("MainWindow", "0º General Report\nWaiting Client", None))
        self.label_8.setText(_translate("MainWindow", "0º Client Status\nWaiting Client", None))
        self.label_4.setText(_translate("MainWindow", "0º Machine Learnt\nWaiting Client", None))

        self.label_5.setText(_translate("MainWindow", "60º General Report\nWaiting Client", None))
        self.label_9.setText(_translate("MainWindow", "60º Client Status\nWaiting Client", None))
        self.label_15.setText(_translate("MainWindow", "60º Machine Learnt\nWaiting Client", None))

        self.label_14.setText(_translate("MainWindow", "120º General Report\nWaiting Client", None))
        self.label_19.setText(_translate("MainWindow", "120º Client Status\nWaiting Client", None))
        self.label_25.setText(_translate("MainWindow", "120º Machine Learnt\nWaiting Client", None))

        self.label_22.setText(_translate("MainWindow", "180º General Report\nWaiting Client", None))
        self.label_18.setText(_translate("MainWindow", "180º Client Status\nWaiting Client", None))
        self.label_24.setText(_translate("MainWindow", "180º Machine Learnt\nWaiting Client", None))

        self.label_12.setText(_translate("MainWindow", "240º General Report\nWaiting Client", None))
        self.label_17.setText(_translate("MainWindow", "240º Client Status\nWaiting Client", None))
        self.label_21.setText(_translate("MainWindow", "240º Machine Learnt\nWaiting Client", None))

        self.label.setText(_translate("MainWindow", "300º General Report\nWaiting Client", None))
        self.label_7.setText(_translate("MainWindow", "300º Client Status\nWaiting Client", None))
        self.label_11.setText(_translate("MainWindow", "300º Machine Learnt\nWaiting Client", None))

        self.menuActivate.setTitle(_translate("MainWindow", "Activate", None))
        self.menuRC.setTitle(_translate("MainWindow", "RemoteCTRL", None))
        self.action0.setText(_translate("MainWindow", "0", None))
        self.action60.setText(_translate("MainWindow", "60", None))
        self.action120.setText(_translate("MainWindow", "120", None))
        self.action180.setText(_translate("MainWindow", "180", None))
        self.action240.setText(_translate("MainWindow", "240", None))
        self.action300.setText(_translate("MainWindow", "300", None))
        self.action0_2.setText(_translate("MainWindow", "0", None))
        self.action60_2.setText(_translate("MainWindow", "60", None))
        self.action120_2.setText(_translate("MainWindow", "120", None))
        self.action180_2.setText(_translate("MainWindow", "180", None))
        self.action240_2.setText(_translate("MainWindow", "240", None))
        self.action300_2.setText(_translate("MainWindow", "300", None))
        #initial trigger
        self.port0()
        self.port60()
        self.port120()
        self.port180()
        self.port240()
        self.port300()
        #initial timer


class ThreadedServer(object):
    def __init__(self, host, port):
        global rdp0
        global rdp60
        global rdp120
        global rdp180
        global rdp240
        global rdp300
        self.host = host
        print host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((host, port))
        dgr=port-6000
        if dgr is 0:
            rdp0=host
        elif dgr is 60:
            rdp60 = host
        elif dgr is 120:
            rdp120 = host
        elif dgr is 180:
            rdp180 = host
        elif dgr is 240:
            rdp240 = host
        elif dgr is 300:
            rdp300 = host

    def listen(self):
        self.sock.listen(5)
        while True:
            client, address = self.sock.accept()
            #client.settimeout(30)
            threading.Thread(target = self.listenToClient,args = (client,address)).start()

    def listenToClient(self, client, address):
        size = 99999
        while True:
            try:
                global data
                data = client.recv(size)
                if data:
                    response = str(DAP)
                    client.send(response)
                else:
                    raise
            except:
                client.close()
                return False


if __name__ == "__main__":
    import sys
    global DAP
    DAP= 81

    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

    #PORT = input("Port? ")
    #ThreadedServer('', PORT).listen()

