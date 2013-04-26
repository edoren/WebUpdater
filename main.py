#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Python native libraries
import os
import sys
import hashgen
import configparser
import threading

# External libraries
from updater import updater # import updater from updater.py
from ui import Ui_Form # Call Ui_Form method from ui.py
from PyQt4 import QtCore, QtGui 

def updateFiles():
    try:
        updater.login(config)
        updater.downloadFiles(config['FTP_Server']['ServerFolder'])
        updater.close()
    except:
        ui.updateStatus = False
        print("Login authentication failed")
        ui.statusLabel2.setText("Login authentication failed")

def generateConfig():
    config = configparser.ConfigParser()

    config['FTP_Server'] = {'Server': '',
                     'Username': '',
                     'Password': '',
                     'ServerFolder': ''}

    config['DEFAULT'] = {'DownloadPath': ''}

    with open('server-config.cfg', 'w') as configfile:
        config.write(configfile)

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('server-config.cfg')

    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    updater = updater(ui)
    Form.show()

    os.chdir(config['DEFAULT']['DownloadPath'])

    statusThread = threading.Thread( target=ui.labelStatus, args=( ) )
    checkHashThread = threading.Thread( target=updateFiles, args=( ) )

    try:
        statusThread.setDaemon(True)
        checkHashThread.setDaemon(True)
        statusThread.start()
        checkHashThread.start()
    except:
        print("Error: unable to start thread")

    sys.exit(app.exec_())
