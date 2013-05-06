# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
import time

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class downloadProgress(QtCore.QThread):
    partDone = QtCore.pyqtSignal(int)
    def Start(self, actualstatus):
        self.end = False
        self.actualstatus = actualstatus
        self.start()

    def run(self):
        while not self.end:
            time.sleep(0.05)
            self.partDone.emit(self.actualstatus.get())

class Ui_Form(object):
    def __init__(self):
        super(Ui_Form, self).__init__()
        self.statusText = "Checking for updates"
        self.statusCount = 0
        self.updateStatus = True

    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.setWindowModality(QtCore.Qt.WindowModal)
        Form.resize(350, 110)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())

        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QtCore.QSize(350, 110))
        Form.setMaximumSize(QtCore.QSize(9999, 9999))

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("")), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        Form.setWindowIcon(icon)

        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setMargin(8)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))

        self.statusLabel = QtGui.QLabel(Form)
        self.statusLabel.setObjectName(_fromUtf8("statusLabel"))

        self.gridLayout.addWidget(self.statusLabel, 0, 0, 1, 1)

        self.statusLabel2 = QtGui.QLabel(Form)
        self.statusLabel2.setText(_fromUtf8(""))
        self.statusLabel2.setObjectName(_fromUtf8("statusLabel2"))

        self.gridLayout.addWidget(self.statusLabel2, 1, 0, 1, 1)

        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(3)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))

        self.progressBarLayout = QtGui.QVBoxLayout()
        self.progressBarLayout.setObjectName(_fromUtf8("progressBarLayout"))

        self.progressBar = QtGui.QProgressBar(Form)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))

        self.progressBarLayout.addWidget(self.progressBar)

        self.progressBar2 = QtGui.QProgressBar(Form)
        self.progressBar2.setProperty("value", 0)
        self.progressBar2.setObjectName(_fromUtf8("progressBar2"))

        self.progressBarLayout.addWidget(self.progressBar2)

        self.horizontalLayout.addLayout(self.progressBarLayout)

        self.buttonsLayout = QtGui.QVBoxLayout()
        self.buttonsLayout.setSpacing(1)
        self.buttonsLayout.setObjectName(_fromUtf8("buttonsLayout"))

        self.updateButton = QtGui.QPushButton(Form)
        self.updateButton.setEnabled(False)
        self.updateButton.setInputMethodHints(QtCore.Qt.ImhNone)
        self.updateButton.setObjectName(_fromUtf8("updateButton"))

        self.buttonsLayout.addWidget(self.updateButton)

        self.scanButton = QtGui.QPushButton(Form)
        self.scanButton.setEnabled(False)
        self.scanButton.setObjectName(_fromUtf8("scanButton"))

        self.buttonsLayout.addWidget(self.scanButton)

        self.horizontalLayout.addLayout(self.buttonsLayout)

        self.gridLayout.addLayout(self.horizontalLayout, 2, 0, 1, 1)

        self.pBarThread = downloadProgress()
        self.pBarThread.partDone.connect(self.updatePBar)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def startPBar(self, pBarVar):
        self.pBarThread.Start(pBarVar)

    def stopPBar(self):
        self.pBarThread.end = True

    def updatePBar(self, val):
        self.progressBar.setValue(val)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Updater", None, QtGui.QApplication.UnicodeUTF8))
        self.statusLabel.setText(QtGui.QApplication.translate("Form", "Checking for updates", None, QtGui.QApplication.UnicodeUTF8))
        self.updateButton.setText(QtGui.QApplication.translate("Form", "Update", None, QtGui.QApplication.UnicodeUTF8))
        self.scanButton.setText(QtGui.QApplication.translate("Form", "Scan", None, QtGui.QApplication.UnicodeUTF8))

    def labelStatus(self):
        while True:
            time.sleep(0.5)
            if self.updateStatus == True:
                if self.statusCount < 3:
                    self.statusCount += 1
                else:
                    self.statusCount = 0
                self.statusLabel.setText(self.statusText + "."*self.statusCount)
