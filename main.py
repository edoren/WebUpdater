#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Python native libraries
import os
import sys
import time
import configparser
import threading

# External libraries
from updater import updater # import updater from updater.py
from ui import Ui_Form # Call Ui_Form method from ui.py
from PyQt4 import QtCore, QtGui 

def updateFiles():
    try:
        updater.login(config)
        updater.calculateDiffer()
    except Exception as exc:
        raise(exc)
    finally:
        ui.updateStatus = False
        time.sleep(0.5)
        print("Update Complete.")
        ui.statusLabel.setText("Update Complete.")

        updater.close()
        print("\nConection Closed")

def scanFiles():
    try:
        updater.login(config)
        updater.downloadEntirePath()
    except Exception as exc:
        raise(exc)
    finally:
        ui.updateStatus = False
        time.sleep(0.5)
        print("Update Complete.")
        ui.statusLabel.setText("Update Complete.")

        updater.close()
        print("\nConection Closed")

def generateConfig():
    config = configparser.ConfigParser()

    config['FTP_Server'] = {'Server': '',
                     'Username': '',
                     'Password': '',
                     'ServerFolder': '',
                     'HashPath': ''}

    config['DEFAULT'] = {'DownloadPath': ''}

    with open('server-config.cfg', 'w') as configfile:
        config.write(configfile)

def startUpdaterThread():
    ui.updateButton.setEnabled(False)
    ui.scanButton.setEnabled(False)
    try:
        checkUpdatesThread.start()
    except:
        ui.updateButton.setEnabled(True)
        ui.scanButton.setEnabled(True)
        print("Error: unable to start updater thread")

def startScannThread():
    ui.updateButton.setEnabled(False)
    ui.scanButton.setEnabled(False)
    try:
        scanFilesThread.start()
    except:
        ui.updateButton.setEnabled(True)
        ui.scanButton.setEnabled(True)
        print("Error: unable to start scanner thread")

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('server-config.cfg')

    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    QtCore.QObject.connect(ui.updateButton, QtCore.SIGNAL("clicked()"), startUpdaterThread)
    QtCore.QObject.connect(ui.scanButton, QtCore.SIGNAL("clicked()"), startScanThread)
    updater = updater(ui)
    Form.show()

    statusThread = threading.Thread( target=ui.labelStatus, args=( ) )
    checkUpdatesThread = threading.Thread( target=updateFiles, args=( ) )
    scanFilesThread = threading.Thread( target=scanFiles , args=( ) )
    statusThread.setDaemon(True)
    checkUpdatesThread.setDaemon(True)
    scanFilesThread.setDaemon(True)

    try:
        statusThread.start()
    except:
        print("Error: unable to start status thread")

    sys.exit(app.exec_())
