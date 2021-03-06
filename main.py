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
    ui.updateStatus = True
    print("\nStarting Update.")
    ui.statusLabel.setText("Starting Update.")
    updater.calculateDiffer()
    ui.updateStatus = False
    time.sleep(0.5)
    print("\nUpdate Completed.")
    ui.statusLabel.setText("Update Completed.")

def scanFiles():
    ui.updateStatus = True
    print("\nStarting Scan.")
    ui.statusLabel.setText("Starting Scan.") 
    updater.downloadEntirePath()
    ui.updateStatus = False
    time.sleep(0.5)
    print("\nScan Completed.")
    ui.statusLabel.setText("Scan Completed.")    

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
        updaterThread.start()
    except:
        ui.updateButton.setEnabled(True)
        ui.scanButton.setEnabled(True)
        print("Error: unable to start updater thread")

def startScanThread():
    ui.updateButton.setEnabled(False)
    ui.scanButton.setEnabled(False)
    try:
        scanFilesThread.start()
    except:
        ui.updateButton.setEnabled(True)
        ui.scanButton.setEnabled(True)
        print("Error: unable to start scanner thread")

def checkDiffer():
    if updater.checkDiffer():
        ui.updateStatus = False
        time.sleep(0.5)
        print("New updates avaliable.")
        ui.statusLabel.setText("New updates avaliable.")
    else:
        ui.updateStatus = False
        time.sleep(0.5)
        print("No updates avaliable.")
        ui.statusLabel.setText("No updates avaliable.")
    ui.updateButton.setEnabled(True)
    ui.scanButton.setEnabled(True)

def destructor():
    app.exec_()
    if not updaterThread.isAlive() and not scanFilesThread.isAlive():
        updater.close()
    return 0

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('server-config.cfg')

    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)

    updater = updater(ui)
    loginResponse = updater.login(config)

    QtCore.QObject.connect(ui.updateButton, QtCore.SIGNAL("clicked()"), startUpdaterThread)
    QtCore.QObject.connect(ui.scanButton, QtCore.SIGNAL("clicked()"), startScanThread)

    Form.show()

    checkDifferThread = threading.Thread( target=checkDiffer, args=( ) )
    statusThread = threading.Thread( target=ui.labelStatus, args=( ) )
    updaterThread = threading.Thread( target=updateFiles, args=( ) )
    scanFilesThread = threading.Thread( target=scanFiles , args=( ) )
    checkDifferThread.setDaemon(True)
    statusThread.setDaemon(True)
    updaterThread.setDaemon(True)
    scanFilesThread.setDaemon(True)

    if loginResponse != 0:
        try:
            statusThread.start()
            checkDifferThread.start()
        except:
            print("Error: unable to start status thread")

    sys.exit(destructor()) 
