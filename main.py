#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Python native libraries
import os
import sys
import configparser
import threading
import hashlib
import pickle

# External libraries
from updater import updater # import updater from updater.py
from ui import Ui_Form # Call Ui_Form method from ui.py
from PyQt4 import QtCore, QtGui 

def sha1_hash(filepath):
    sha1 = hashlib.sha1()
    f = open(filepath, 'rb')
    try:
        sha1.update(f.read())
    finally:
        f.close()
    return sha1.hexdigest()

def getHash():
	hashDict = {}

	for dirname, dirnames, filenames in os.walk(config['DEFAULT']['Path']):
		# for subdirname in dirnames:
		# 		print(os.path.join(dirname, subdirname).split(config['DEFAULT']['Path'])[1])
		for filename in filenames:
			hashDict[os.path.join(dirname, filename).split(config['DEFAULT']['Path'])[1]] = sha1_hash(os.path.join(dirname, filename))
			print(os.path.join(dirname, filename).split(config['DEFAULT']['Path'])[1])
	
	hash_file = open('updater.dat', 'wb')
	pickle.dump(hashDict, hash_file)
	hash_file.close()

	# pkl_file = open('hash.dat', 'rb')
	# mydict2 = pickle.load(pkl_file)
	# pkl_file.close()

	print(hashDict)

def checkHash():
	updater.login(config)
	updater.downloadFolderFiles('')
	updater.quit()

def generateConfig():
	config = configparser.ConfigParser()

	config['FTP'] = {'Server': '',
	                 'Username': '',
	                 'Password': ''}

	config['DEFAULT'] = {'Path': ''}

	with open('server-config.cfg', 'w') as configfile:
		config.write(configfile)

if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	Form = QtGui.QWidget()
	ui = Ui_Form()
	ui.setupUi(Form)
	updater = updater(ui)
	Form.show()

	dl_file_size = 0

	config = configparser.ConfigParser()
	config.read('server-config.cfg')

	statusThread = threading.Thread( target=ui.labelStatus, args=( ) )
	checkHashThread = threading.Thread( target=checkHash, args=( ) )

	try:
		statusThread.setDaemon(True)
		checkHashThread.setDaemon(True)
		statusThread.start()
		checkHashThread.start()
	except:
		print("Error: unable to start thread")

	sys.exit(app.exec_())
