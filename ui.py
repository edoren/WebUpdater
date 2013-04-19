# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
import time

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Form(object):
    def __init__(self):
        super(Ui_Form, self).__init__()
        self.statText = "Checking for updates"
        self.statusCount = 0
        self.updateStatus = True

    def statusText(self, text):
        self.statText = text
        self.statusCount = 0

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
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("Minecraft.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Form.setWindowIcon(icon)
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.statusLabel = QtGui.QLabel(Form)
        self.statusLabel.setObjectName(_fromUtf8("statusLabel"))
        self.gridLayout.addWidget(self.statusLabel, 0, 0, 1, 1)
        self.label = QtGui.QLabel(Form)
        self.label.setText(_fromUtf8(""))
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.progressBar = QtGui.QProgressBar(Form)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.verticalLayout.addWidget(self.progressBar)
        self.progressBar2 = QtGui.QProgressBar(Form)
        self.progressBar2.setProperty("value", 0)
        self.progressBar2.setObjectName(_fromUtf8("progressBar2"))
        self.verticalLayout.addWidget(self.progressBar2)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.updateButtonWidget = QtGui.QWidget(Form)
        self.updateButtonWidget.setObjectName(_fromUtf8("updateButtonWidget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.updateButtonWidget)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.updateButton = QtGui.QPushButton(self.updateButtonWidget)
        self.updateButton.setInputMethodHints(QtCore.Qt.ImhNone)
        self.updateButton.setObjectName(_fromUtf8("updateButton"))
        self.verticalLayout_2.addWidget(self.updateButton)
        self.horizontalLayout.addWidget(self.updateButtonWidget)
        self.gridLayout.addLayout(self.horizontalLayout, 2, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Updater", None, QtGui.QApplication.UnicodeUTF8))
        self.statusLabel.setText(QtGui.QApplication.translate("Form", "Checking for updates", None, QtGui.QApplication.UnicodeUTF8))
        self.updateButton.setText(QtGui.QApplication.translate("Form", "Update", None, QtGui.QApplication.UnicodeUTF8))

    def windowStatus(self):
        while self.updateStatus == True:
            time.sleep(0.5)
            if self.statusCount < 3:
                self.statusCount += 1
                self.statText += "."
            else:
                self.statText = self.statText[:-self.statusCount]
                self.statusCount = 0
            self.statusLabel.setText(self.statText)

